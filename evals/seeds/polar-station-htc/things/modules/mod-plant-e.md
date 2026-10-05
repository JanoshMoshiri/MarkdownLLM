---
id: mod-plant-e
type: module
status: operational
created: '2026-01-15'
title: Plant E
use: plant
occupants: 0
equipment_w: 3940
volume_m3: 304
hrv_class: H1
hrv_commissioned: '2025-09-01'
elements:
- name: north wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 20
  windward: true
- name: south wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 20
  windward: false
- name: west wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 14
  windward: false
- name: east party wall
  kind: party
  assembly: asm-party
  area_m2: 14
  neighbour: mod-medical-d
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 39
- name: floor
  kind: floor
  assembly: asm-floor-raised
  area_m2: 36
  ice_coupled: false
---

# Plant E

Module record. Element areas are net areas in m²; glazing is listed as its own element.
