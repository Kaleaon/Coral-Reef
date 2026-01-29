# Coral-Reef

Multi-TPU computing platform for A.I. development, designed to host multiple AI minds on Google Coral M.2 TPU accelerators in a thermally-optimized column architecture.

## Overview

Coral-Reef is an open hardware design for a high-density AI inference server featuring the **One Mind Per Layer** architecture. Each physical layer hosts a complete AI persona with 16 dedicated TPUs, enabling 6 distinct AI personalities to operate simultaneously at full speed.

```
    THE CORAL-REEF MIND STACK

    ┌─────────────────────────────────────┐
    │           EXHAUST                   │
    ╠═════════════════════════════════════╣
    │  LAYER 6: "FRANK" - The Analyst     │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │  LAYER 5: "EVE" - The Creative      │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │  LAYER 4: "DAVE" - The Engineer     │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │  LAYER 3: "CAROL" - The Teacher     │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │  LAYER 2: "BOB" - The Companion     │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │  LAYER 1: "ALICE" - The Assistant   │  ← 16 TPUs = 1 Mind
    ╠═════════════════════════════════════╣
    │           FILTERED INTAKE           │
    └─────────────────────────────────────┘

    6 Layers × 16 TPUs = 96 TPUs Total
    Each mind has dedicated: Language, Vision, Audio, Memory modules
```

## Key Features

- **One Mind Per Layer**: Each AI persona gets dedicated hardware - no resource contention
- **Split Attention Architecture**: 16 TPUs per layer divided into Language (10), Perception (3), Memory (2), Reserve (1)
- **Hot-Swappable Minds**: Remove a tray to "transplant" an AI to another system
- **Parallel Operation**: All 6 minds think simultaneously at full speed
- **Efficient Cooling**: Central chimney airflow design with radial heat dissipation
- **Filtered Intake**: MERV 8-13 filtration protects components from dust
- **Landseek Integration**: Designed as a backend for multi-persona AI chat applications

## Design Documents

### Hardware Design
| Document | Description |
|----------|-------------|
| [DESIGN.md](designs/column-tpu-tower/DESIGN.md) | Main hardware design with physical architecture |
| [SPECIFICATIONS.md](designs/column-tpu-tower/SPECIFICATIONS.md) | Detailed technical specifications |
| [AIRFLOW.md](designs/column-tpu-tower/AIRFLOW.md) | Airflow system design and thermal management |

### Software & System Architecture
| Document | Description |
|----------|-------------|
| [ONE_MIND_PER_LAYER.md](designs/column-tpu-tower/ONE_MIND_PER_LAYER.md) | **Core architecture** - TPU allocation, split attention, mind transplant |
| [SOFTWARE_ARCHITECTURE.md](designs/column-tpu-tower/SOFTWARE_ARCHITECTURE.md) | Inference orchestration, RAG, memory systems, APIs |
| [STORAGE_SUBSYSTEM.md](designs/column-tpu-tower/STORAGE_SUBSYSTEM.md) | NVMe storage, vector databases, model caching |
| [NETWORK_ARCHITECTURE.md](designs/column-tpu-tower/NETWORK_ARCHITECTURE.md) | Deployment modes, P2P sync, security |

## TPU Allocation Per Mind

Each 16-TPU layer is functionally split:

```
╔═══════════════════════════════════════════════════════════╗
║  LANGUAGE MODULE (10 TPUs)                                ║
║  Primary thinking - text generation & understanding       ║
║  Supports pipeline parallel for 7B models                 ║
║  OR batch parallel for 5 concurrent 2B streams           ║
╠═══════════════════════════════════════════════════════════╣
║  PERCEPTION (3 TPUs)    ║  MEMORY (2 TPUs)               ║
║  Vision encoder/decoder  ║  Embedding generation          ║
║  Audio transcription     ║  RAG retrieval                 ║
╠══════════════════════════╩═══════════════════════════════╣
║  RESERVE (1 TPU) - Failover, burst capacity, tools       ║
╚═══════════════════════════════════════════════════════════╝
```

## Specifications Summary

| Parameter | Value |
|-----------|-------|
| Form Factor | Cylindrical Column |
| Dimensions | 300mm dia × 680mm H |
| AI Minds | 6 (one per layer) |
| TPUs per Mind | 16 |
| Total TPUs | 96 |
| Power | 200-400W typical |
| Airflow | 150-300 CFM |
| Noise | <45 dBA |

## Target Use Cases

- **[Landseek](https://github.com/Kaleaon/Landseek) Backend**: Multi-persona AI chat with dedicated hardware per personality
- **AI Development**: Test and develop multiple AI agents in parallel
- **Home AI Server**: Family AI assistant with distinct personalities
- **Edge AI Cluster**: High-throughput inference for IoT/robotics

## Status

**Current Version**: 0.2 (Design Phase)

- [x] Initial concept design
- [x] Airflow architecture
- [x] Technical specifications
- [x] One-mind-per-layer architecture
- [x] Software architecture
- [x] Storage subsystem design
- [x] Network architecture
- [ ] PCB schematics
- [x] [3D CAD models](designs/column-tpu-tower/3d-models)
- [ ] Prototype build
- [ ] Thermal validation

## License

TBD

## Contributing

This project is in early design phase. Contributions and feedback welcome via issues and pull requests.
