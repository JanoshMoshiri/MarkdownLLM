---
id: mod-living-f
type: module
status: operational
created: '2026-01-15'
title: Living F
use: living
occupants: 4
equipment_w: 900
volume_m3: 350
hrv_class: H2
hrv_commissioned: '2026-03-01'
elements:
- name: north wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 22
  windward: true
- name: south wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 22
  windward: false
- name: east wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 16
  windward: false
- name: west wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 16
  windward: false
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 48
- name: floor
  kind: floor
  assembly: asm-floor-ice
  area_m2: 48
  ice_coupled: true
- name: south glazing
  kind: glazing
  glazing_type: QG-4
  area_m2: 7
---

# Living F

Module record. Element areas are net areas in m²; glazing is listed as its own element.
