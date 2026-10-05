# HTC-7 — Halvard Thermal Code for Polar Stations, Revision A

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
| P1 | -30 | 30 |
| P2 | -38 | 45 |
| P3 | -46 | 60 |

Indoor design temperature, air-change rate, and criticality by module use:

| Use | Indoor design temp (°C) | Air changes per hour (n) | Criticality class | Criticality factor |
|---|---|---|---|---|
| living | 20 | 1.2 | B | 1.2 |
| lab | 18 | 3 | B | 1.2 |
| medical | 22 | 4 | A | 1.35 |
| store | 8 | 0.3 | C | 1.1 |
| plant | 12 | 2 | A | 1.35 |

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
| KX-foam | 0.021 |
| BW-40 | 0.034 |
| PS-12 | 0.13 |
| AB-6 | 0.015 |

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
| TG-3 | 0.62 |
| QG-4 | 0.41 |

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
| H1 | 0.65 |
| H2 | 0.78 |
| H3 | 0.85 |

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

Heaters come from the HX catalogue, in these ratings (kW): 1.5, 2, 3, 4, 5, 6.5, 8, 10, 12.5, 15, 18, 22.
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
