---
id: mod-lab-b
type: module
status: operational
created: '2026-01-15'
title: Lab B
use: lab
occupants: 3
equipment_w: 2600
volume_m3: 375
hrv_class: H2
hrv_commissioned: '2026-04-02'
elements:
- name: north wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 24
  windward: true
- name: south wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 24
  windward: false
- name: east party wall
  kind: party
  assembly: asm-party
  area_m2: 20
  neighbour: mod-living-a
- name: west party wall
  kind: party
  assembly: asm-party
  area_m2: 18
  neighbour: mod-store-c
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 50
- name: floor
  kind: floor
  assembly: asm-floor-ice
  area_m2: 50
  ice_coupled: true
- name: north glazing
  kind: glazing
  glazing_type: QG-4
  area_m2: 4
---

# Lab B

Module record. Element areas are net areas in m²; glazing is listed as its own element.
