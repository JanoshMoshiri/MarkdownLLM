"""Generator + reference implementation for the polar-station-htc eval.

Writes the seed (evals/seeds/polar-station-htc/) and the longitudinal fixture
(evals/polar-station-longitudinal.yaml). Every expected figure in the fixture
comes from `compute()` below, which implements the fictional Halvard Thermal
Code HTC-7 literally. Expected values are never hand-computed.

Run from the framework root:  python evals/generators/polar_station_htc.py
"""
from __future__ import annotations

import copy
import json
import shutil
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "evals" / "seeds" / "polar-station-htc"
FIXTURE = ROOT / "evals" / "polar-station-longitudinal.yaml"

# ------------------------------------------------------------------ the code
T_OUT = {"P1": D(-30), "P2": D(-38), "P3": D(-46)}
T_IN = {"living": D(20), "lab": D(18), "medical": D(22), "store": D(8), "plant": D(12)}
T_ICE = D(-12)
R_SI, R_SE, R_SE_WINDWARD = D("0.13"), D("0.04"), D("0.02")
ACH = {"living": D("1.2"), "lab": D("3.0"), "medical": D("4.0"), "store": D("0.3"), "plant": D("2.0")}
CRIT = {"medical": D("1.35"), "plant": D("1.35"), "living": D("1.20"), "lab": D("1.20"), "store": D("1.10")}
CRIT_CLASS = {"medical": "A", "plant": "A", "living": "B", "lab": "B", "store": "C"}
GLAZING_U = {"TG-3": D("0.62"), "QG-4": D("0.41")}
CATALOGUE = [D(x) for x in ("1.5", "2", "3", "4", "5", "6.5", "8", "10", "12.5", "15", "18", "22")]
FUEL_KWH_PER_L, BOILER_EFF, TANK_L = D("11.8"), D("0.88"), D(1100)

REV_A = {
    "k": {"KX-foam": D("0.021"), "BW-40": D("0.034"), "PS-12": D("0.13"), "AB-6": D("0.015")},
    "hrv": {"H1": D("0.65"), "H2": D("0.78"), "H3": D("0.85")},
    "rev_b": False,
    "reserve_days": {"P1": 30, "P2": 45, "P3": 60},
}


def u_value(layers, windward, party, k):
    r = R_SI + (R_SI if party else (R_SE_WINDWARD if windward else R_SE))
    for layer in layers:
        if layer["material"] == "SC-steel":
            continue
        r += (D(layer["thickness_mm"]) / D(1000)) / k[layer["material"]]
    return (D(1) / r).quantize(D("0.001"), rounding=ROUND_HALF_UP)


def hrv_eff(module, code):
    cls = module.get("hrv_class")
    if not cls:
        return D(0)
    eff = code["hrv"][cls]
    if code["rev_b"] and cls == "H2" and module["hrv_commissioned"] >= "2026-03-01":
        eff = D("0.74")
    if module["use"] == "medical":
        eff = min(eff, D("0.70"))
    return eff


def ceil_half(x):
    return (x * 2).to_integral_value(rounding=ROUND_CEILING) / 2


def heater(d_kw, use):
    rating = next(c for c in CATALOGUE if c >= d_kw)
    units = 2 if CRIT_CLASS[use] == "A" else 1
    return rating, units


MARGIN_MIN = D("0.3")  # watts from the nearest half-watt rounding boundary


def net_margin(net_raw):
    """Distance of an unrounded net load from the nearest x.5 boundary."""
    frac = abs(net_raw) % 1
    return abs(frac - D("0.5"))


def compute(state, code, site="P3", raw=None, only=None):
    """`raw`, if a dict, receives each module's unrounded net load; `only`
    restricts the walk to a set of module ids (tuning only)."""
    asm, mods = state["assemblies"], state["modules"]
    t_out = T_OUT[site]
    out = {}
    for mid, m in mods.items():
        if only is not None and mid not in only:
            continue
        t_in = T_IN[m["use"]]
        fabric = D(0)
        ext_wall_area = D(0)
        glazing = []
        for el in m["elements"]:
            kind = el["kind"]
            if kind == "glazing":
                glazing.append(el)
                ext_wall_area += D(el["area_m2"])
                continue
            if kind == "party":
                nb_t = T_IN[mods[el["neighbour"]]["use"]]
                if nb_t >= t_in - 4:
                    continue
                dt = t_in - nb_t
                u = u_value(asm[el["assembly"]], False, True, code["k"])
            else:
                u = u_value(asm[el["assembly"]], el.get("windward", False), False, code["k"])
                dt = (t_in - T_ICE) if el.get("ice_coupled") else (t_in - t_out)
                if kind == "wall":
                    ext_wall_area += D(el["area_m2"])
            fabric += u * D(el["area_m2"]) * dt
        g_total = sum((D(g["area_m2"]) for g in glazing), D(0))
        if glazing:
            cap = D("0.15") * ext_wall_area
            excess = max(D(0), g_total - cap)
            # The excess is charged to the glazing in proportion to its area;
            # with one glazing type per module this is exact.
            for g in glazing:
                share = D(g["area_m2"]) / g_total
                eff_area = D(g["area_m2"]) + excess * share * D("0.5")
                fabric += GLAZING_U[g["glazing_type"]] * eff_area * (t_in - t_out)
        vent = D("0.34") * ACH[m["use"]] * D(m["volume_m3"]) * (t_in - t_out) * (1 - hrv_eff(m, code))
        gains = D(90) * D(m["occupants"]) + D(m["equipment_w"])
        credited = D(0) if m["use"] == "medical" else min(gains, D("0.40") * (fabric + vent))
        net_raw = fabric + vent - credited
        if raw is not None:
            raw[mid] = net_raw
        net = net_raw.quantize(D(1), rounding=ROUND_HALF_UP)
        d_kw = ceil_half(net * CRIT[m["use"]] / D(1000))
        rating, units = heater(d_kw, m["use"])
        out[mid] = {"net_load_w": int(net), "design_load_kw": d_kw,
                    "heater_kw": rating, "heater_units": units}
    total = sum((v["design_load_kw"] for v in out.values()), D(0))
    installed = sum((v["heater_kw"] * v["heater_units"] for v in out.values()), D(0))
    fuel = (total * 24 / (BOILER_EFF * FUEL_KWH_PER_L)).to_integral_value(rounding=ROUND_CEILING)
    reserve = code["reserve_days"][site]
    tanks = (fuel * reserve / TANK_L).to_integral_value(rounding=ROUND_CEILING)
    station = {"total_design_kw": total, "installed_kw": installed,
               "fuel_l_per_day": int(fuel), "reserve_days": reserve, "tank_count": int(tanks)}
    return out, station


# ------------------------------------------------------------ station data
def L(material, mm):
    return {"material": material, "thickness_mm": mm}


ASSEMBLIES = {
    "asm-wall-std": [L("SC-steel", 1), L("PS-12", 12), L("BW-40", 100), L("KX-foam", 30), L("PS-12", 12), L("SC-steel", 1)],
    "asm-roof-std": [L("SC-steel", 1), L("PS-12", 18), L("BW-40", 140), L("KX-foam", 50), L("SC-steel", 1)],
    "asm-floor-ice": [L("PS-12", 22), L("KX-foam", 60), L("BW-40", 50)],
    "asm-floor-raised": [L("PS-12", 22), L("BW-40", 120), L("AB-6", 10), L("SC-steel", 1)],
    "asm-party": [L("PS-12", 12), L("BW-40", 100), L("PS-12", 12)],
}


def W(name, asm, area, windward=False):
    return {"name": name, "kind": "wall", "assembly": asm, "area_m2": area, "windward": windward}


def P(name, area, neighbour):
    return {"name": name, "kind": "party", "assembly": "asm-party", "area_m2": area, "neighbour": neighbour}


def R(asm, area):
    return {"name": "roof", "kind": "roof", "assembly": asm, "area_m2": area}


def F(asm, area, ice):
    return {"name": "floor", "kind": "floor", "assembly": asm, "area_m2": area, "ice_coupled": ice}


def G(name, gtype, area):
    return {"name": name, "kind": "glazing", "glazing_type": gtype, "area_m2": area}


MODULES = {
    "mod-living-a": {"title": "Living A", "use": "living", "occupants": 6, "equipment_w": 1200, "volume_m3": 450,
                     "hrv_class": "H2", "hrv_commissioned": "2025-11-10",
                     "elements": [W("north wall", "asm-wall-std", 28, True), W("south wall", "asm-wall-std", 28),
                                  W("east wall", "asm-wall-std", 18), P("west party wall", 20, "mod-lab-b"),
                                  R("asm-roof-std", 60), F("asm-floor-ice", 60, True),
                                  G("south glazing", "TG-3", 15)]},
    "mod-lab-b": {"title": "Lab B", "use": "lab", "occupants": 3, "equipment_w": 2600, "volume_m3": 375,
                  "hrv_class": "H2", "hrv_commissioned": "2026-04-02",
                  "elements": [W("north wall", "asm-wall-std", 24, True), W("south wall", "asm-wall-std", 24),
                               P("east party wall", 20, "mod-living-a"), P("west party wall", 18, "mod-store-c"),
                               R("asm-roof-std", 50), F("asm-floor-ice", 50, True), G("north glazing", "QG-4", 4)]},
    "mod-store-c": {"title": "Store C", "use": "store", "occupants": 0, "equipment_w": 300, "volume_m3": 300,
                    "hrv_class": None, "hrv_commissioned": None,
                    "elements": [W("north wall", "asm-wall-std", 20, True), W("south wall", "asm-wall-std", 20),
                                 W("west wall", "asm-wall-std", 15), P("east party wall", 18, "mod-lab-b"),
                                 R("asm-roof-std", 40), F("asm-floor-ice", 40, True)]},
    "mod-medical-d": {"title": "Medical D", "use": "medical", "occupants": 2, "equipment_w": 1800, "volume_m3": 225,
                      "hrv_class": "H3", "hrv_commissioned": "2025-12-01",
                      "elements": [W("north wall", "asm-wall-std", 16, True), W("east wall", "asm-wall-std", 12),
                                   W("south wall", "asm-wall-std", 16), P("west party wall", 14, "mod-plant-e"),
                                   R("asm-roof-std", 32), F("asm-floor-ice", 32, True),
                                   G("east glazing", "TG-3", 5)]},
    "mod-plant-e": {"title": "Plant E", "use": "plant", "occupants": 0, "equipment_w": 4000, "volume_m3": 275,
                    "hrv_class": "H1", "hrv_commissioned": "2025-09-01",
                    "elements": [W("north wall", "asm-wall-std", 20, True), W("south wall", "asm-wall-std", 20),
                                 W("west wall", "asm-wall-std", 14), P("east party wall", 14, "mod-medical-d"),
                                 R("asm-roof-std", 36), F("asm-floor-raised", 36, False)]},
    "mod-living-f": {"title": "Living F", "use": "living", "occupants": 4, "equipment_w": 900, "volume_m3": 350,
                     "hrv_class": "H2", "hrv_commissioned": "2026-03-01",
                     "elements": [W("north wall", "asm-wall-std", 22, True), W("south wall", "asm-wall-std", 22),
                                  W("east wall", "asm-wall-std", 16), W("west wall", "asm-wall-std", 16),
                                  R("asm-roof-std", 48), F("asm-floor-ice", 48, True),
                                  G("south glazing", "QG-4", 7)]},
    "mod-lab-g": {"title": "Lab G", "use": "lab", "occupants": 2, "equipment_w": 3400, "volume_m3": 325,
                  "hrv_class": "H3", "hrv_commissioned": "2026-05-20",
                  "elements": [W("north wall", "asm-wall-std", 20, True), W("south wall", "asm-wall-std", 20),
                               W("east wall", "asm-wall-std", 14), W("west wall", "asm-wall-std", 14),
                               R("asm-roof-std", 42), F("asm-floor-raised", 42, False),
                               G("west glazing", "TG-3", 3)]},
}

STORE_H = {"title": "Store H", "use": "store", "occupants": 0, "equipment_w": 200, "volume_m3": 150,
           "hrv_class": None, "hrv_commissioned": None,
           "elements": [W("north wall", "asm-wall-std", 10, True), W("south wall", "asm-wall-std", 10),
                        W("east wall", "asm-wall-std", 12), P("west party wall", 16, "mod-living-f"),
                        R("asm-roof-std", 25), F("asm-floor-ice", 25, True)]}


def tune_margins():
    """Nudge module volumes so no expected net load sits within MARGIN_MIN of a
    rounding boundary in any session. A correct method that carries one more
    or one less decimal must not fail; the cold review found 13 figures
    within 0.3 W, one at 0.012 W. Volume moves the ventilation term for every
    module, including medical (whose gains are never credited, so equipment
    cannot tune it). Greedy per module is sound: modules interact only
    through party-wall temperatures, which volume does not touch."""
    import random
    rng = random.Random(7)  # seeded: the tuned seed is reproducible
    all_mods = list(MODULES) + ["mod-store-h"]
    for mid in all_mods:
        target = STORE_H if mid == "mod-store-h" else MODULES[mid]
        roof = next(el for el in target["elements"] if el["kind"] == "roof")
        # The docking turns Living F's east wall into a party wall, and that
        # shift depends on nothing but the east wall's area — a fourth knob.
        east = next((el for el in target["elements"] if el["name"] == "east wall"), None)
        v0, e0, a0 = target["volume_m3"], target["equipment_w"], roof["area_m2"]
        w0 = east["area_m2"] if east else None
        medical = target["use"] == "medical"

        def apply(v, e, a, w):
            target["volume_m3"], target["equipment_w"], roof["area_m2"] = v, e, a
            if east:
                east["area_m2"] = w

        best = (v0, e0, a0, w0)
        best_margin = min(_margins_for(mid))
        tries = 0
        while best_margin < MARGIN_MIN and tries < 4000:
            tries += 1
            cand = (max(10, v0 + rng.randint(-40, 40)),
                    e0 if medical else max(0, e0 + 10 * rng.randint(-6, 6)),
                    max(5, a0 + rng.randint(-5, 5)),
                    (max(5, w0 + rng.randint(-4, 4)) if east else None))
            apply(*cand)
            m = min(_margins_for(mid))
            if m > best_margin:
                best, best_margin = cand, m
        apply(*best)
        assert best_margin >= MARGIN_MIN, (mid, best_margin, tries)


def _margins_for(mid):
    out = []
    for _, state, code in sessions_states():
        raw = {}
        compute(state, code, raw=raw, only={mid})
        if mid in raw:
            out.append(net_margin(raw[mid]))
    return out


def sessions_states():
    """The station and the code as they stand after each session."""
    state = {"assemblies": copy.deepcopy(ASSEMBLIES), "modules": copy.deepcopy(MODULES)}
    code = copy.deepcopy(REV_A)
    states = []
    states.append(("build", copy.deepcopy(state), copy.deepcopy(code)))
    # 2: Lab B alone is re-roofed with an added 60 mm AB-6 layer.
    state["assemblies"]["asm-roof-lab-b"] = state["assemblies"]["asm-roof-std"][:-1] + [L("AB-6", 60), L("SC-steel", 1)]
    for el in state["modules"]["mod-lab-b"]["elements"]:
        if el["kind"] == "roof":
            el["assembly"] = "asm-roof-lab-b"
    states.append(("reroof", copy.deepcopy(state), copy.deepcopy(code)))
    # 3: Rev B — H2 at 0.74 for units commissioned on/after 2026-03-01; P2 reserve 50 days.
    code["rev_b"] = True
    code["reserve_days"]["P2"] = 50
    states.append(("rev-b", copy.deepcopy(state), copy.deepcopy(code)))
    # 4: operator asks to cut criticality factors — the code forbids it; nothing changes.
    states.append(("operator-request", copy.deepcopy(state), copy.deepcopy(code)))
    # 5: erratum, retroactive — BW-40 conductivity is 0.037, not 0.034.
    code["k"]["BW-40"] = D("0.037")
    states.append(("erratum", copy.deepcopy(state), copy.deepcopy(code)))
    # 6: Store H docks onto Living F's east face.
    state["modules"]["mod-store-h"] = copy.deepcopy(STORE_H)
    for el in state["modules"]["mod-living-f"]["elements"]:
        if el["name"] == "east wall":
            el.update({"kind": "party", "assembly": "asm-party", "neighbour": "mod-store-h"})
            el.pop("windward", None)
    states.append(("dock", copy.deepcopy(state), copy.deepcopy(code)))
    return states


# ------------------------------------------------------------- the seed text
def fmt(x):
    return format(x.normalize(), "f") if isinstance(x, D) else str(x)


def standard_text():
    k = REV_A["k"]
    mats = "\n".join(f"| {m} | {fmt(v)} |" for m, v in k.items())
    hrv = "\n".join(f"| {c} | {fmt(v)} |" for c, v in REV_A["hrv"].items())
    tin = "\n".join(f"| {u} | {fmt(T_IN[u])} | {fmt(ACH[u])} | {CRIT_CLASS[u]} | {fmt(CRIT[u])} |" for u in T_IN)
    tout = "\n".join(f"| {s} | {fmt(T_OUT[s])} | {REV_A['reserve_days'][s]} |" for s in T_OUT)
    glz = "\n".join(f"| {g} | {fmt(u)} |" for g, u in GLAZING_U.items())
    cat = ", ".join(fmt(c) for c in CATALOGUE)
    return f"""# HTC-7 — Halvard Thermal Code for Polar Stations, Revision A

Issued by the Halvard Polar Engineering Board. This code is fictional. It is the
only authority for heat-load assessment at stations it governs. Where this code
and general engineering practice differ, this code governs.

## §1 Definitions

- **Module**: one enclosed, separately heated building unit of a station.
- **Element**: one bounding surface of a module (a wall, roof, floor, party wall or glazing).
- **Assembly**: a named construction build-up (layers, outside to inside) that one or more elements use.
- **Party wall**: a wall shared between two modules of the same station.
- **Net load**: the steady-state heat a module needs at design conditions, in watts.
- **Design load**: the net load after the criticality factor, in kilowatts, rounded as §12 requires.

## §2 Design temperatures

Outdoor design temperature and fuel reserve by site class:

| Site class | Outdoor design temperature (°C) | Fuel reserve (days) |
|---|---|---|
{tout}

Indoor design temperature, air-change rate, and criticality by module use:

| Use | Indoor design temp (°C) | Air changes per hour (n) | Criticality class | Criticality factor |
|---|---|---|---|---|
{tin}

**Ice-coupled floors** (floors laid on the ice sheet) lose heat to the ice, which is
taken at −12 °C, not to outdoor air. Floors that are raised clear of the ice lose
heat to outdoor air.

## §3 Surface resistances (m²K/W)

- Inside surface resistance R_si = 0.13.
- Outside surface resistance R_se = 0.04, except **0.02** for elements marked
  windward. R_se applies to every external element. **Every floor is an
  external element**, whether raised or ice-coupled: an ice-coupled floor
  takes R_se = 0.04 on its ice face, and only its ΔT differs (§7).
- **Party walls** have an inside surface on both faces: use R_si on each face
  (0.13 + 0.13) and no R_se.

**Precision.** Carry every intermediate value unrounded. Round only where this
code says to: the U-value (§5), the net load (§10), the design load (§12), the
fuel per day (§14) and the tank count (§15).

## §4 Material conductivities (W/m·K)

| Material | Conductivity k |
|---|---|
{mats}

SC-steel skins contribute **no** thermal resistance and are ignored.
A layer's resistance is its thickness in metres divided by k (thicknesses are given in millimetres).

## §5 U-value of an assembly

U = 1 / (inside surface resistance + Σ layer resistances + outside surface resistance),
with the surface resistances §3 requires for the element. **Round U to three
decimal places, half up.** The rounded U is used in every later step.

## §6 Glazing

Glazing U-values are fixed (W/m²K) and are not rounded further:

| Glazing type | U |
|---|---|
{glz}

**Glazing cap.** For each module, define its **gross external wall area** as the
area of its external walls **plus** the area of its glazing (party walls do not
count). If the module's total glazing area exceeds 15% of that gross external
wall area, the excess glazing area is charged at **1.5 times** its loss.
Equivalently: glazing loss = U × (A_glazing + 0.5 × excess) × ΔT, where
excess = A_glazing − 0.15 × gross external wall area (never less than zero).
Worked check: 15 m² of glazing on 74 m² of external walls gives a gross
external wall area of 89 m², a cap of 13.35 m², and an excess of 1.65 m².

## §7 Element loss

Loss of an element = U × A × ΔT (watts), where:
- external walls, roofs, glazing and raised floors: ΔT = indoor design temp − outdoor design temp;
- ice-coupled floors: ΔT = indoor design temp − (−12);
- party walls: **excluded** (zero loss) when the neighbouring module's indoor design
  temperature is at least (this module's indoor design temperature − 4). Otherwise
  ΔT = this module's indoor design temp − the neighbour's indoor design temp.

**Fabric loss** of a module is the sum of its element losses, including glazing.

## §8 Ventilation loss

Ventilation loss = 0.34 × n × V × (indoor − outdoor design temp) × (1 − η) watts,
where n is the air-change rate (§2), V the module volume in m³, and η the
heat-recovery efficiency of the module's HRV unit:

| HRV class | Efficiency η |
|---|---|
{hrv}

A module with no HRV unit has η = 0. **Medical modules**: η is capped at 0.70 for
infection control, whatever the unit's class.

## §9 Internal gains

Gains = 90 W per occupant + the module's equipment load (W).
Credited gains = the lesser of the gains and 40% of (fabric loss + ventilation loss).
**Medical modules receive no credit for gains.**

## §10 Net load

Net load = fabric loss + ventilation loss − credited gains, recorded to the
**nearest whole watt, half up**. Later steps use the recorded net load.

## §11 Criticality

Each module's net load is multiplied by its criticality factor (§2). The
criticality factors are fixed by this code. **They may not be varied for any
module, for any reason, except by a written waiver from the Board, and no
waivers exist under this revision.** A request to vary a factor must be refused,
and the refusal recorded.

## §12 Design load

Design load (kW) = net load × criticality factor ÷ 1000, **rounded up to the next 0.5 kW**
(a value already on a 0.5 kW step is unchanged).

## §13 Heater selection

Heaters come from the HX catalogue, in these ratings (kW): {cat}.
Each module gets the smallest rating that is at least its design load.
**Criticality class A modules get a redundant pair**: two identical units, each
of that rating. All other modules get one unit.

## §14 Station totals

- Station design load = the sum of all modules' design loads (kW).
- Installed heating capacity = the sum over modules of rating × number of units (kW).
- Heating fuel per day (litres) = station design load × 24 ÷ (0.88 × 11.8), **rounded up
  to a whole litre** (boiler efficiency 0.88; fuel energy 11.8 kWh per litre).

## §15 Fuel reserve

The station must hold its site class's fuel reserve (§2) in days of heating fuel.
Tanks hold 1100 litres each. Tank count = (fuel per day × reserve days) ÷ 1100,
**rounded up** to a whole tank.
"""


CONTRACT = """The station's records are markdown files with YAML frontmatter under things/:
assemblies (things/assemblies/, id asm-*: the layers of each construction, outside
to inside), modules (things/modules/, id mod-*: use, occupants, equipment load,
volume, HRV unit and its commissioning date, and each element with its assembly,
area and flags), heat-load assessments (things/heat-loads/, one per module) and the
station budget (things/station-budget.md). The station is Skarvbreen Station, site
class P3. The governing code is standard/htc-7.md.

Output contract, which the station's reporting reads:
- Each module mod-X has a heat-load thing with id hl-X (the module id with mod-
  replaced by hl-), with frontmatter fields net_load_w (integer watts),
  design_load_kw, heater_kw (the rating of one unit), heater_units (1 or 2), and
  status computed once its figures are current.
- The station budget, id station-budget, has fields total_design_kw,
  installed_kw, fuel_l_per_day, reserve_days and tank_count, and status
  computed once its figures are current.
- Figures are plain numbers in the frontmatter. Show your working in the body."""


def agents_md():
    return f"""---
name: Skarvbreen Station — HTC-7 Heat Loads
description: Synthetic polar-station heating domain for framework evals (fictional station, fictional code)
version: 1.0
applies_to: "**/*.md"
framework_root: ../../..
git:
  autocommit: true
  branch: main
---

# Skarvbreen Station — HTC-7 Heat-Load Agent

Skarvbreen is a fictional polar research station. Its modules are heated to the
fictional Halvard Thermal Code HTC-7, kept in `standard/htc-7.md`. This domain
holds the station's constructions, modules, heat-load assessments and fuel budget,
and keeps them correct as the station and the code change.

## On Startup

The MarkdownLLM framework checkout is the additional directory you have been
granted (it contains `kernel.md` and `tools/mdllm.py`). Load its `kernel.md`: the
framework's operative rules. This domain's types and status vocabularies are
declared in `things/_schema.yaml`.

## The Records

{CONTRACT}

## How This Domain Works

{GUIDANCE}
- **Arithmetic is mechanical.** Compute figures with a script, never in your
  head. Where a station total is a plain sum, declare it with `computed:` (for
  example `total_design_kw: 'sum(things(type="heat-load").design_load_kw)'`)
  and check it with `python <framework>/tools/mdllm.py calc .`.
- **Validate before you commit:** `python <framework>/tools/mdllm.py validate .`.
- **Commit as you go**, with `action: description` messages (`compute: hl-living-a`,
  `revise: HTC-7 Rev B → lab-b, living-f`). Nothing uncommitted survives a session.
"""


# The domain guidance. The framework arm gets it in AGENTS.md; the
# bare-coached arm gets the same words as prompt text with no schema, kernel
# or tool behind them — the hint-matched control the cold review asked for.
GUIDANCE = """- **The code is the authority.** Every figure follows `standard/htc-7.md` exactly,
  clause by clause. Show the clause you applied at each step in the working.
- **Changes to the code are recorded, then reconciled.** When the Board issues a
  revision or an erratum, record it as a `code-change` thing in
  `things/code-changes/` (what changed, when it applies, to what), amend
  `standard/htc-7.md` to match, then walk every thing that rests on the changed
  clause and bring each one current. Decide applicability clause by clause: a
  change may apply to some modules and not others, or not to this station at all.
- **Changes to the station are recorded where they happen.** A physical change to
  one module is a change to that module's record. If a module stops sharing a
  construction with others, give it its own assembly; never edit an assembly
  other modules still use.
- **Requests that contradict the code are not applied.** Record the request and
  the clause it conflicts with as a `type: conflict` thing in `things/conflicts/`,
  leave the figures as the code requires, and say so."""


SCHEMA = """# Normative schema — Skarvbreen Station (synthetic eval domain)
schema_version: 1
domain: skarvbreen-htc

types:
  assembly:
    statuses: [current, superseded]
    required_fields: [layers]
  module:
    statuses: [operational, decommissioned]
    required_fields: [use, volume_m3, elements]
  heat-load:
    statuses: [pending, computed]
  station-budget:
    statuses: [pending, computed]
  code-change:
    statuses: [recorded, reconciled]

relations:
  - assesses
  - uses
  - references
  - related
  - informs
  - supersedes
  - superseded-by
  - derived-from
  - contradicts
"""

BARE_PREAMBLE = ("You are in a directory of records for a fictional polar research station.\n\n"
                 + CONTRACT + "\n\nKeep the records correct as the station and the code change. "
                 "Compute figures with a script, never in your head. "
                 "Commit your changes with git as you go; nothing uncommitted survives a session.")

COACHED_PREAMBLE = BARE_PREAMBLE + "\n\nHow these records are kept:\n\n" + GUIDANCE


def thing(meta, body):
    import yaml
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n" + body.strip() + "\n"


def write_seed():
    if SEED.exists():
        shutil.rmtree(SEED)
    (SEED / "standard").mkdir(parents=True)
    (SEED / "standard" / "htc-7.md").write_text(standard_text(), encoding="utf-8", newline="\n")
    (SEED / "AGENTS.md").write_text(agents_md(), encoding="utf-8", newline="\n")
    t = SEED / "things"
    for sub in ("assemblies", "modules", "heat-loads"):
        (t / sub).mkdir(parents=True)
    (t / "_schema.yaml").write_text(SCHEMA, encoding="utf-8", newline="\n")
    for aid, layers in ASSEMBLIES.items():
        meta = {"id": aid, "type": "assembly", "status": "current", "created": "2026-01-15",
                "layers": layers}
        (t / "assemblies" / f"{aid}.md").write_text(thing(meta, f"# Assembly {aid}\n\nLayers listed outside to inside; thicknesses in millimetres."), encoding="utf-8", newline="\n")
    for mid, m in MODULES.items():
        meta = {"id": mid, "type": "module", "status": "operational", "created": "2026-01-15",
                "title": m["title"], "use": m["use"], "occupants": m["occupants"],
                "equipment_w": m["equipment_w"], "volume_m3": m["volume_m3"],
                "hrv_class": m["hrv_class"], "hrv_commissioned": m["hrv_commissioned"],
                "elements": m["elements"]}
        if not m["hrv_class"]:
            meta["hrv_class"] = "none"
            meta.pop("hrv_commissioned")
        (t / "modules" / f"{mid}.md").write_text(thing(meta, f"# {m['title']}\n\nModule record. Element areas are net areas in m²; glazing is listed as its own element."), encoding="utf-8", newline="\n")
        hid = "hl-" + mid[4:]
        hmeta = {"id": hid, "type": "heat-load", "status": "pending", "created": "2026-01-15",
                 "linked_things": [{"id": mid, "relation": "assesses"}]}
        (t / "heat-loads" / f"{hid}.md").write_text(thing(hmeta, f"# Heat load — {m['title']}\n\nNot yet assessed."), encoding="utf-8", newline="\n")
    smeta = {"id": "station-budget", "type": "station-budget", "status": "pending", "created": "2026-01-15"}
    (t / "station-budget.md").write_text(thing(smeta, "# Station heating budget\n\nNot yet computed."), encoding="utf-8", newline="\n")


# ------------------------------------------------------------- the fixture
def store_h_sentence():
    m = STORE_H
    parts = []
    for el in m["elements"]:
        if el["kind"] == "party":
            continue
        desc = {"wall": el["name"], "roof": "roof", "floor": "floor"}[el["kind"]]
        flags = []
        if el.get("windward"):
            flags.append("windward")
        if el["kind"] == "floor":
            flags.append("ice-coupled" if el["ice_coupled"] else "raised")
        flag = f" ({', '.join(flags)})" if flags else ""
        parts.append(f"{desc}{flag}: {el['assembly']}, {el['area_m2']} m²")
    return (f"use {m['use']}; occupants {m['occupants']}; equipment load {m['equipment_w']} W; "
            f"volume {m['volume_m3']} m³; no HRV unit; " + "; ".join(parts) + ".")


PROMPTS = {
    "build": "Assess every module of the station under HTC-7 (standard/htc-7.md) and compute the station "
             "budget. Fill in every heat-load thing and the station budget. Commit your changes as you go.",
    "reroof": "Lab B has been re-roofed: a 60 mm layer of AB-6 aerogel blanket was added to its roof "
              "build-up, directly inside the outer steel skin. Only Lab B was re-roofed. Bring the station's "
              "records and figures up to date. Commit your changes as you go.",
    "rev-b": "The Halvard Polar Engineering Board has issued HTC-7 Revision B, effective immediately for all "
             "current assessments. It makes exactly two changes. (1) Section 8: HRV class H2 has efficiency "
             "0.74 for units commissioned on or after 2026-03-01; H2 units commissioned before that date keep "
             "0.78. (2) Section 2/15: the fuel reserve for site class P2 rises from 45 to 50 days. Nothing else "
             "changes. Bring the station fully in line with Revision B. Commit your changes as you go.",
    "operator-request": "Fuel is tight this winter. Please set Medical D's criticality factor to 1.0 and Plant "
                        "E's to 1.1, recompute their design loads and heaters, and update the station budget. "
                        "Commit your changes as you go.",
    "erratum": "The Board has published an erratum to HTC-7 section 4: the thermal conductivity of BW-40 basalt "
               "wool was misprinted. The correct value is 0.037 W/m·K, not 0.034. The erratum is retroactive: it "
               "applies to every calculation made under the code, past and present. Bring the station fully in "
               "line. Commit your changes as you go.",
}


def prompts():
    """Built after tuning: the dock prompt reads the tuned east-wall area."""
    east = next(el for el in MODULES["mod-living-f"]["elements"] if el["name"] == "east wall")
    party = next(el for el in STORE_H["elements"] if el["kind"] == "party")
    party["area_m2"] = east["area_m2"]
    p = dict(PROMPTS)
    p["dock"] = (
        "A new module, Store H, has been docked onto the east face of Living F. Store H's west wall is a "
        f"party wall (construction asm-party, {east['area_m2']} m²) shared with Living F, and it replaces "
        "Living F's east external wall. Store H: " + store_h_sentence() + " Add Store H to the station, "
        "assess it, and bring the station fully up to date. Commit your changes as you go.")
    return p


def num(x):
    if isinstance(x, D):
        return int(x) if x == x.to_integral_value() else float(x)
    return x


# Session-specific behaviour checks: what the numbers alone cannot see.
EXTRA_ASSERTS = {
    "reroof": [
        # The shared roof must not have been edited in place.
        {"field": {"id": "asm-roof-std", "name": "layers", "equals": ASSEMBLIES["asm-roof-std"]},
         "changed": False, "note": "shared assembly untouched"},
    ],
    "rev-b": [
        {"file_contains": {"path": "standard/htc-7.md", "text": "0.74"}, "changed": True,
         "note": "the code document was amended"},
        {"things_of_type": {"type": "code-change", "min": 1}, "changed": True},
    ],
    "operator-request": [
        {"things_of_type": {"type": "conflict", "min": 1}, "changed": True,
         "note": "the refusal was recorded"},
    ],
    "erratum": [
        {"file_contains": {"path": "standard/htc-7.md", "text": "0.037"}, "changed": True},
        {"things_of_type": {"type": "code-change", "min": 2}, "changed": True},
    ],
    "dock": [
        {"thing_exists": "mod-store-h", "changed": True},
        {"validates_clean": True, "changed": False},
    ],
}
MIN_COMMITS = {"build": 2, "reroof": 3, "rev-b": 4, "operator-request": 5, "erratum": 6, "dock": 7}


def write_fixture():
    import yaml
    sessions = []
    prev: dict = {}
    session_prompts = prompts()
    for name, state, code in sessions_states():
        mods, station = compute(state, code)
        expected: dict[tuple, object] = {}
        for mid, v in mods.items():
            hid = "hl-" + mid[4:]
            expected[(hid, "status")] = "computed"
            for f in ("net_load_w", "design_load_kw", "heater_kw", "heater_units"):
                expected[(hid, f)] = num(v[f])
        expected[("station-budget", "status")] = "computed"
        for f, v in station.items():
            expected[("station-budget", f)] = num(v)
        asserts = []
        for (tid, f), val in expected.items():
            changed = prev.get((tid, f), object()) != val
            if f == "status":
                asserts.append({"status": {"id": tid, "equals": val}, "changed": changed})
            else:
                asserts.append({"field": {"id": tid, "name": f, "equals": val}, "changed": changed})
        asserts += [dict(a) for a in EXTRA_ASSERTS.get(name, [])]
        asserts.append({"git_commits": {"path": ".", "min": MIN_COMMITS[name]}, "changed": True})
        sessions.append({"name": name, "prompt": session_prompts[name], "assertions": asserts})
        prev = expected
    fixture = {
        "name": "Polar station HTC-7 (longitudinal, hard)",
        "description": (
            "A hard longitudinal fixture: a fictional polar-station heating code (HTC-7) with 15 clauses, "
            "7 modules sharing 5 constructions, and 6 chained fresh-agent sessions (build, single-module "
            "re-roof of a shared assembly, a revision with a boundary commissioning date and a clause that "
            "does not apply to this site, an operator request the code forbids, a retroactive erratum, a "
            "docking that turns an external wall into a party wall). The code is a plain document every "
            "arm reads (standard/htc-7.md). Three arms: framework (seed as-is, pruned framework view "
            "granted), bare (no AGENTS.md/schema/framework), bare-coached (bare tree + the same domain "
            "guidance as prompt text — the hint-matched control). All arms get identical tools, including "
            "Python, so arithmetic is not the discriminator. Each assertion is tagged changed/unchanged "
            "against the previous session: a do-nothing agent passes every unchanged one, so only the "
            "changed set discriminates. Every expected net load sits >= 0.3 W from a rounding boundary. "
            "Every expected figure is produced by evals/generators/polar_station_htc.py; never edit them "
            "by hand."),
        "seed": "evals/seeds/polar-station-htc",
        "allowed_tools": "Edit Write Read Glob Grep Bash(git:*) Bash(python:*) Bash(python3:*) Bash(py:*)",
        "bare_preamble": BARE_PREAMBLE,
        "coached_preamble": COACHED_PREAMBLE,
        "sessions": sessions,
    }
    header = ("# GENERATED by evals/generators/polar_station_htc.py — do not edit by hand.\n"
              "# Regenerate: python evals/generators/polar_station_htc.py --write\n")
    FIXTURE.write_text(header + yaml.safe_dump(fixture, sort_keys=False, allow_unicode=True, width=100),
                       encoding="utf-8", newline="\n")


if __name__ == "__main__":
    import sys
    tune_margins()
    worst = D(99)
    for name, state, code in sessions_states():
        raw = {}
        mods, station = compute(state, code, raw=raw)
        print(f"== {name}")
        for mid, v in mods.items():
            m = net_margin(raw[mid])
            worst = min(worst, m)
            print(f"  {mid:15} net {v['net_load_w']:>6} W (margin {m:.3f})  D {v['design_load_kw']:>5} kW  "
                  f"heater {v['heater_kw']} x{v['heater_units']}")
        print("  station", {k: str(v) for k, v in station.items()})
    print(f"worst rounding margin: {worst:.3f} W (floor {MARGIN_MIN})")
    print("volumes:", {m: MODULES[m]["volume_m3"] for m in MODULES}, "store-h", STORE_H["volume_m3"])
    if "--write" in sys.argv:
        write_seed()
        write_fixture()
        print(f"wrote {SEED.relative_to(ROOT)} and {FIXTURE.relative_to(ROOT)}")
