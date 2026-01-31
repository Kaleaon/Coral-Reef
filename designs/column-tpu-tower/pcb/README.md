# PCB Design: 16-TPU Carrier Board with Compute Cluster

## Overview

This directory contains the design files and specifications for the custom carrier board used in the Coral-Reef Column TPU Tower. Each board acts as a self-contained "Mind" layer, hosting not just the AI accelerators but also a local compute cluster to drive them.

## Architecture

The carrier board implements a hybrid architecture combining a high-density PCIe switch fabric with a local cluster of 4 powerful CPU modules. This ensures "full/complete computation" capabilities on each disc, minimizing reliance on external hosts.

### Key Components

1.  **Compute Cluster (4x CPU Units)**
    *   **Type:** System-on-Module (SOM) (e.g., RK3588, CM4-variant, or equivalent high-perf ARM/RISC-V).
    *   **Function:** Host operating system, model orchestration, data preprocessing, and general logic.
    *   **Interface:** PCIe 3.0 x4 per CPU module to the central switch.
    *   **Power:** Dedicated power rails (approx 10-15W per module).

2.  **PCIe Packet Switch (PEX 8748/8749)**
    *   **Fabric:** Connects the 4 CPU units and 16 M.2 TPUs in a non-blocking fabric.
    *   **Configuration:**
        *   4x Ports (x4 width) -> CPU Modules.
        *   16x Ports (x1 width) -> M.2 TPU Sockets.
        *   1x Port (x4/x8) -> Optional Inter-layer Uplink.
    *   **Features:** DMA, Peer-to-Peer transfer (TPU <-> TPU, CPU <-> TPU).

3.  **M.2 Sockets (16x)**
    *   **Type:** M.2 Key E (2230) or Key B+M (2280).
    *   **Interface:** PCIe x1 Gen 2.0 per socket.
    *   **Power:** 3.3V supply (max 3A per socket).

4.  **Power Distribution Network (PDN)**
    *   **Input:** 12V DC (Main Bus).
    *   **Regulation:**
        *   Buck Converters for CPU Cluster (5V/4A per module or custom rails).
        *   Buck Converters for TPUs (3.3V, Total ~60W).
        *   Management MCU power.
    *   **Total Power:** ~120W-150W peak per layer (requires active cooling).

5.  **Management MCU (ESP32-S3)**
    *   **Function:** Thermal monitoring, fan control, power sequencing, cluster health check.
    *   **Interface:** I2C/SMBus.

## Netlist Generation

The schematic connectivity is defined programmatically using the Python script `scripts/generate_pcb_netlist.py`. This script acts as the "Schematic-as-Code" source of truth.

To regenerate the netlist:

```bash
python3 scripts/generate_pcb_netlist.py
```

The output file `netlist.csv` contains the full connectivity map (Net Name, Ref Des, Pin Number, Pin Name).

## Design Considerations

*   **Signal Integrity:** High-speed PCIe routing is critical. 4x CPUs + 16x TPUs creates a dense routing challenge in the central area.
*   **Thermal Management:** The addition of 4 CPU modules significantly increases thermal density. The "Chimney" airflow must be unobstructed by the taller CPU components.
*   **Placement:** CPU modules likely placed in the quadrants between TPU banks to distribute heat.
