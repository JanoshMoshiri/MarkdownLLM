---
id: mod-medical-d
type: module
status: operational
created: '2026-01-15'
title: Medical D
use: medical
occupants: 2
equipment_w: 1800
volume_m3: 263
hrv_class: H3
hrv_commissioned: '2025-12-01'
elements:
- name: north wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 16
  windward: true
- name: east wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 10
  windward: false
- name: south wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 16
  windward: false
- name: west party wall
  kind: party
  assembly: asm-party
  area_m2: 14
  neighbour: mod-plant-e
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 33
- name: floor
  kind: floor
  assembly: asm-floor-ice
  area_m2: 32
  ice_coupled: true
- name: east glazing
  kind: glazing
  glazing_type: TG-3
  area_m2: 5
---

# Medical D

Module record. Element areas are net areas in m²; glazing is listed as its own element.
