---
id: mod-store-c
type: module
status: operational
created: '2026-01-15'
title: Store C
use: store
occupants: 0
equipment_w: 250
volume_m3: 263
hrv_class: none
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
  area_m2: 15
  windward: false
- name: east party wall
  kind: party
  assembly: asm-party
  area_m2: 18
  neighbour: mod-lab-b
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 38
- name: floor
  kind: floor
  assembly: asm-floor-ice
  area_m2: 40
  ice_coupled: true
---

# Store C

Module record. Element areas are net areas in m²; glazing is listed as its own element.
