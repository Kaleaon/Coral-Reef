# PCB Design: 16-TPU Carrier Board

## Overview

This directory contains the design files and specifications for the custom carrier board used in the Coral-Reef Column TPU Tower. Each board hosts 16 Google Coral M.2 Accelerators (Key E or Key B+M) and acts as a single "Mind" layer in the tower.

## Architecture

The carrier board implements a high-density PCIe switch fabric to connect 16 TPU modules to a single upstream PCIe x16 link.

### Key Components

1.  **PCIe Packet Switch (PEX 8748/8749)**
    *   **Upstream:** x16 PCIe Gen 3.0 interface to host (via edge connector or cable).
    *   **Downstream:** 16x PCIe Gen 2.0 x1 links to M.2 sockets.
    *   **Features:** Low latency, non-blocking architecture, peer-to-peer support.

2.  **M.2 Sockets (16x)**
    *   **Type:** M.2 Key E (2230) or Key B+M (2280).
    *   **Interface:** PCIe x1 Gen 2.0 per socket.
    *   **Power:** 3.3V supply (max 3A per socket for peak loads).

3.  **Power Distribution Network (PDN)**
    *   **Input:** 12V DC (from main PSU).
    *   **Regulation:**
        *   High-efficiency Buck Converters (12V -> 3.3V) for TPUs (Total ~60W).
        *   LDOs for clean analog supply (if needed).
        *   Power sequencing logic for soft-start.

4.  **Management MCU (ESP32-S3)**
    *   **Function:** Thermal monitoring, fan control, power telemetry.
    *   **Interface:** I2C/SMBus to PCIe switch and power regulators.
    *   **Connectivity:** USB-Serial for external management.

## Netlist Generation

The schematic connectivity is defined programmatically using the Python script `scripts/generate_pcb_netlist.py`. This script acts as the "Schematic-as-Code" source of truth.

To regenerate the netlist:

```bash
python3 scripts/generate_pcb_netlist.py
```

The output file `netlist.csv` contains the full connectivity map (Net Name, Ref Des, Pin Number, Pin Name).

## Design Considerations

*   **Signal Integrity:** PCIe traces must be impedance matched (85-100 ohm differential) and length-matched within pairs.
*   **Thermal Management:** The PCB requires heavy copper planes (2oz+) for heat dissipation and power delivery.
*   **Layer Stackup:** Recommended 6-layer or 8-layer stackup for proper signal isolation and power planes.
