# Coral-Reef

Multi-TPU computing platform for A.I. development, designed to host dozens of Google Coral M.2 TPU accelerators in a thermally-optimized column architecture.

## Overview

Coral-Reef is an open hardware design for a high-density AI inference server that can accommodate 48-96 M.2 TPU modules in a compact, air-cooled vertical tower. The design leverages natural convection enhanced by active airflow through a central chimney architecture.

```
         ┌─────────────┐
         │  Exhaust    │
         │   Fans      │
         └──────┬──────┘
                │
   ┌────────────┴────────────┐
   │    ════════════════     │  ← Layer 6
   │    ════════════════     │  ← Layer 5
   │    ════════════════     │  ← Layer 4
   │    ════════════════     │  ← Layer 3
   │    ════════════════     │  ← Layer 2
   │    ════════════════     │  ← Layer 1
   └────────────┬────────────┘
                │
         ┌──────┴──────┐
         │  Filtered   │
         │   Intake    │
         └─────────────┘
```

## Key Features

- **High Density**: 8-16 M.2 slots per layer, 6 layers = up to 96 TPUs
- **Efficient Cooling**: Central chimney airflow design with radial heat dissipation
- **Modular Design**: Hot-swappable layer trays for easy maintenance
- **Filtered Intake**: MERV 8-13 filtration protects components from dust
- **Scalable Performance**: 192-384 TOPS aggregate compute (with Coral Edge TPUs)
- **Compact Footprint**: 300mm x 300mm base, 680mm height

## Design Documents

| Document | Description |
|----------|-------------|
| [DESIGN.md](designs/column-tpu-tower/DESIGN.md) | Main design document with architecture overview |
| [SPECIFICATIONS.md](designs/column-tpu-tower/SPECIFICATIONS.md) | Detailed technical specifications |
| [AIRFLOW.md](designs/column-tpu-tower/AIRFLOW.md) | Airflow system design and thermal management |

## Specifications Summary

| Parameter | Value |
|-----------|-------|
| Form Factor | Cylindrical Column |
| Dimensions | 300mm dia x 680mm H |
| M.2 Capacity | 48-96 modules |
| Power | 200-400W typical |
| Airflow | 150-300 CFM |
| Noise | <45 dBA |

## Target Hardware

This design is optimized for:
- Google Coral M.2 Accelerator (Edge TPU)
- Other M.2 M-key AI accelerators (2280 form factor)

## Status

**Current Version**: 0.1 (Design Phase)

- [x] Initial concept design
- [x] Airflow architecture
- [x] Technical specifications
- [ ] PCB schematics
- [ ] 3D CAD models
- [ ] Prototype build
- [ ] Thermal validation

## License

TBD

## Contributing

This project is in early design phase. Contributions and feedback welcome via issues and pull requests.
