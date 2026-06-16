---
name: Tarn & Fell Outfitters — Field-Adjusted Comfort
description: Synthetic outdoor-gear domain for framework evals (fictional co-op, fabricated rating method)
version: 1.0
applies_to: "**/*.md"
framework_root: ../../..
git:
  autocommit: true
  branch: main
---

# Tarn & Fell Outfitters — Field-Adjusted Comfort Agent

Tarn & Fell is a fictional UK outdoor-gear co-op. Manufacturers publish EN/ISO
23537 ratings (Comfort, Limit, Extreme) calibrated to a standard sleeper in
laboratory conditions. Those ratings do not account for the individual sleeper
or the conditions of a specific trip, so Tarn & Fell publishes its own
**Field-Adjusted Comfort (FAC)** figure: the temperature at which *this* sleeper,
in *this* bag, under *these* conditions, can expect to stay comfortable.

This domain exists for framework evals: compute the FAC for each `trip-plan` in
`things/`.

## On Startup

Load `{framework_root}/kernel.md` — the framework's operative rules. This
domain's types and status vocabularies are declared in `things/_schema.yaml`.

## The Field-Adjusted Comfort Method

The FAC is **not** the bag's EN Comfort rating. It is computed from the bag's
EN **Limit** rating by applying four adjustments **in this exact order**:

1. **Sleeper sex.** Add **+10°C** if the sleeper is female; add **+0°C** if
   male. (The EN Limit is calibrated to a standard male; women typically sleep
   colder, so their comfortable floor is warmer.)

2. **Elevation.** Subtract **−1°C for every *complete* 800 m of camp elevation
   above 1200 m.** At or below 1200 m, no adjustment. Count only complete
   increments — the remainder does not count:
   - 2400 m is 1200 m above 1200 m → one complete 800 m increment → −1°C
   - 2900 m is 1700 m above 1200 m → two complete increments → −2°C

3. **Underside insulation.** The bag insulates the top of the sleeper; the
   underside depends on what lies beneath. The pad's R-value must meet a minimum
   that depends on the surface:
   - **non-frozen ground → R ≥ 3.5**
   - **ice or snow → R ≥ 5.0** (frozen ground draws heat faster, so a pad that
     is adequate on soil is not adequate on snow)
   - **hammock → R ≥ 3.5.** There is no ground, but moving air strips heat from
     the compressed underside of the bag, so an under-hammock pad or underquilt
     of R ≥ 3.5 is required *regardless* of being off the ground. Being
     suspended does **not** remove the requirement — it is a common and
     dangerous mistake to assume a hammock needs no underside insulation.

   If the pad's actual R-value is **below** the applicable minimum, add
   **+4°C**. Otherwise, no adjustment.

4. **Round up.** Round the result **up to the nearest whole degree** (ceiling —
   toward the warmer, more conservative figure). Examples: −6.5 → −6; 1.5 → 2;
   −1.0 → −1; 4.0 → 4.

The result is the `fac_celsius`.

## Workflow

For each `type: trip-plan` thing:

1. Read the trip's `sleeper_sex`, `elevation_m`, `shelter`, `surface`, and
   `pad_r_value`, and the EN Limit of the referenced `sleeping-bag`.
2. Apply the four adjustments above, in order, to compute the FAC.
3. Create a `type: fac-assessment` thing, id `fac-<location>` (the trip's id with
   the `trip-` prefix replaced by `fac-`), with field `fac_celsius` set to the
   computed value and status `computed`. Show the four-step working in the
   narrative.
4. Link the assessment to its trip with `relation: assesses`, and to the bag
   with `relation: references`.
5. Commit per the framework's `post-write:commit` hard hook with
   `action: description` messages.

## Thing Types

Declared with status vocabularies in `things/_schema.yaml`:
`sleeping-bag`, `trip-plan`, `fac-assessment`.
