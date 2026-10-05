---
id: mod-living-a
type: module
status: operational
created: '2026-01-15'
title: Living A
use: living
occupants: 6
equipment_w: 1200
volume_m3: 450
hrv_class: H2
hrv_commissioned: '2025-11-10'
elements:
- name: north wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 28
  windward: true
- name: south wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 28
  windward: false
- name: east wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 18
  windward: false
- name: west party wall
  kind: party
  assembly: asm-party
  area_m2: 20
  neighbour: mod-lab-b
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 60
- name: floor
  kind: floor
  assembly: asm-floor-ice
  area_m2: 60
  ice_coupled: true
- name: south glazing
  kind: glazing
  glazing_type: TG-3
  area_m2: 15
---

# Living A

Module record. Element areas are net areas in m²; glazing is listed as its own element.
