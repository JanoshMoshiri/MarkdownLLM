---
id: mod-lab-g
type: module
status: operational
created: '2026-01-15'
title: Lab G
use: lab
occupants: 2
equipment_w: 3400
volume_m3: 325
hrv_class: H3
hrv_commissioned: '2026-05-20'
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
- name: east wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 14
  windward: false
- name: west wall
  kind: wall
  assembly: asm-wall-std
  area_m2: 14
  windward: false
- name: roof
  kind: roof
  assembly: asm-roof-std
  area_m2: 42
- name: floor
  kind: floor
  assembly: asm-floor-raised
  area_m2: 42
  ice_coupled: false
- name: west glazing
  kind: glazing
  glazing_type: TG-3
  area_m2: 3
---

# Lab G

Module record. Element areas are net areas in m²; glazing is listed as its own element.
