# Coral-Reef Column TPU Tower Design

## Overview

The Coral-Reef Column TPU Tower is a vertically-oriented, air-cooled computing system designed to host 48-96 Google Coral M.2 TPU accelerators (or similar M.2 AI accelerators) across multiple layers. The design leverages natural convection enhanced by active airflow through a central chimney architecture.

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

## Design Philosophy

1. **Vertical Chimney Effect**: Hot air naturally rises; the column design harnesses this
2. **Radial Airflow**: Air enters center, flows outward across M.2 boards, exits at edges
3. **Modular Layers**: Each layer is a removable tray for easy maintenance
4. **Scalability**: Stack 4-8 layers depending on cooling and power requirements

---

## Specifications

| Parameter | Value |
|-----------|-------|
| Form Factor | Cylindrical Column |
| Outer Diameter | 300mm (11.8") |
| Inner Core Diameter | 80mm (3.15") |
| Height (6-layer config) | 600mm (23.6") |
| M.2 Slots per Layer | 8-16 (configurable) |
| Total TPU Capacity | 48-96 units |
| Power Consumption | 200-400W typical |
| Airflow Rate | 150-300 CFM |
| Operating Temp | 0-40°C ambient |
| Noise Level | <45 dBA at full load |

---

## Structural Design

### Overall Architecture

```
    TOP VIEW (Single Layer)

              N
              │
        ┌─────┴─────┐
       ╱             ╲
      │   ┌─────┐     │
    W─┤   │     │     ├─E
      │   │ AIR │     │
      │   │CORE │     │
       ╲  └─────┘    ╱
        └─────┬─────┘
              │
              S

    M.2 cards arranged radially
    pointing outward from center
```

### Column Frame Structure

The outer frame consists of:

1. **Base Platform** (60mm height)
   - Houses filtered intake system
   - Contains intake fans (3x 80mm or 2x 120mm)
   - Removable filter cartridge
   - Mounting feet with vibration dampening

2. **Central Core Tube** (80mm diameter)
   - Perforated aluminum or steel tube
   - Runs full height of unit
   - Provides structural support
   - Acts as air distribution plenum

3. **Layer Support Rails** (6-8 vertical rails)
   - Aluminum extrusion rails
   - Support and align each tray layer
   - Provide cable routing channels

4. **Outer Shell** (optional)
   - Perforated mesh cylinder
   - Provides dust protection
   - Aesthetic finish
   - Can be removed for maximum airflow

5. **Top Exhaust Assembly** (80mm height)
   - 2-3x 120mm exhaust fans
   - Optional chimney extension
   - Pull-type airflow for negative pressure

---

## Layer/Tray Design

### Tray Specifications

```
    SINGLE TRAY - TOP VIEW

                    300mm
         ←─────────────────────→

    ┌────────────────────────────┐  ─┬─
    │  ╔═══╗        ╔═══╗        │   │
    │  ║M.2║        ║M.2║        │   │
    │  ╚═══╝        ╚═══╝        │   │
    │        ┌────┐              │   │
    │ ╔═══╗  │    │  ╔═══╗      │   │ 300mm
    │ ║M.2║  │AIR │  ║M.2║      │   │
    │ ╚═══╝  │HOLE│  ╚═══╝      │   │
    │        └────┘              │   │
    │  ╔═══╗        ╔═══╗        │   │
    │  ║M.2║        ║M.2║        │   │
    │  ╚═══╝        ╚═══╝        │   │
    └────────────────────────────┘  ─┴─
```

### Tray Construction

Each tray consists of:

1. **Base Plate**: 3mm aluminum with thermal properties
   - Central 80mm air passage hole
   - Radial slot cutouts for airflow
   - M.2 mounting positions

2. **M.2 Carrier PCB**: Custom PCB for each M.2 position
   - M.2 M-key socket (2280 form factor)
   - PCIe signal routing to edge connector
   - Local power regulation (3.3V)
   - LED status indicators
   - Temperature sensor pad

3. **Heatsink Integration**
   - Each M.2 slot has dedicated heatsink
   - Finned aluminum, oriented for radial airflow
   - Thermal pad interface to M.2 module
   - 40x20x10mm per heatsink minimum

### M.2 Slot Configurations

**8-Slot Configuration** (Standard density)
```
         ┌───────────────┐
         │   [2]   [1]   │
         │               │
         │[3]  (AIR)  [8]│
         │               │
         │[4]        [7] │
         │               │
         │   [5]   [6]   │
         └───────────────┘

    Spacing: 45° between slots
    Clearance: Excellent
    Cooling: Optimal
```

**12-Slot Configuration** (Medium density)
```
         ┌───────────────┐
         │  [2] [1] [12] │
         │               │
         │[3]  (AIR)  [11]│
         │[4]        [10]│
         │               │
         │  [5] [6] [9]  │
         │      [7] [8]  │
         └───────────────┘

    Spacing: 30° between slots
    Clearance: Good
    Cooling: Good
```

**16-Slot Configuration** (High density)
```
         ┌───────────────┐
         │[2][1][16][15] │
         │               │
         │[3]  (AIR) [14]│
         │[4]       [13] │
         │[5]       [12] │
         │               │
         │[6][7][8][9][10]│
         │     [11]      │
         └───────────────┘

    Spacing: 22.5° between slots
    Clearance: Tight
    Cooling: Requires higher airflow
```

---

## Airflow System

### Primary Airflow Path

```
    SIDE CROSS-SECTION

    ═══════════════════════════════  ← Exhaust fans (PULL)
           ↑     ↑     ↑
    ┌──────┼─────┼─────┼──────┐
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 6
    ├──────┼─────┼─────┼──────┤
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 5
    ├──────┼─────┼─────┼──────┤
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 4
    ├──────┼─────┼─────┼──────┤
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 3
    ├──────┼─────┼─────┼──────┤
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 2
    ├──────┼─────┼─────┼──────┤
    │ →→→→ ↑ ←←← │ →→→ ↑ ←←← │  Layer 1
    └──────┼─────┼─────┼──────┘
           ↑     ↑     ↑
    ═══════════════════════════════  ← Filtered intake

    Legend:
    ↑ = Vertical airflow (up through center)
    → = Horizontal airflow (outward to M.2s)
    ← = Return air (edge channels)
```

### Airflow Mechanics

1. **Intake Stage**
   - Filtered air enters base through mesh filter
   - Intake fans pressurize lower plenum
   - Air velocity: 2-4 m/s

2. **Distribution Stage**
   - Air rises through central perforated core
   - Holes in core tube sized for even distribution
   - Larger holes at top to compensate for pressure drop

3. **Cooling Stage**
   - Air exits core holes horizontally
   - Flows radially outward across M.2 heatsinks
   - Each M.2 receives direct airflow

4. **Exhaust Stage**
   - Hot air collected at outer edges
   - Rises through vertical edge channels
   - Exhaust fans create negative pressure pull
   - Exit velocity: 3-5 m/s

### Fan Configuration

**Intake Fans (Base)**
- 3x 80mm high-static-pressure fans, OR
- 2x 120mm fans with shroud
- PWM controlled, 1500-3000 RPM range
- Total: 80-150 CFM push

**Exhaust Fans (Top)**
- 2x 140mm or 3x 120mm fans
- PWM controlled, 1000-2500 RPM range
- Total: 100-200 CFM pull

**Airflow Balance**
- Slight negative pressure preferred
- Exhaust CFM ~110% of intake CFM
- Prevents dust infiltration through gaps

---

## Air Filtration System

### Filter Assembly

```
    FILTER CARTRIDGE - EXPLODED VIEW

    ┌─────────────────────────┐
    │     Outer Grill         │  ← Removable protective grill
    ├─────────────────────────┤
    │  ░░░░░░░░░░░░░░░░░░░░  │  ← Pre-filter (washable mesh)
    ├─────────────────────────┤
    │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Main filter (MERV 8-13)
    ├─────────────────────────┤
    │     Filter Frame        │  ← Slide-out cartridge frame
    └─────────────────────────┘
```

### Filter Specifications

| Stage | Type | Rating | Replacement |
|-------|------|--------|-------------|
| Pre-filter | Washable aluminum mesh | 50 micron | Clean monthly |
| Main filter | Pleated media | MERV 8-13 | 3-6 months |
| Optional | Activated carbon | Odor/VOC | 6-12 months |

### Filter Access

- Bottom-loading cartridge design
- Tool-free removal
- Filter status indicator (differential pressure sensor)
- Visual inspection window

---

## Electrical System

### Power Architecture

```
    POWER DISTRIBUTION DIAGRAM

    ┌─────────────────────────────────────────┐
    │              MAIN PSU                    │
    │         (ATX 650W-850W)                 │
    │  ┌─────┬─────┬─────┬─────┬─────┐       │
    │  │12V  │12V  │12V  │5V   │5VSB │       │
    │  │Rail1│Rail2│Rail3│Rail │Rail │       │
    │  └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┘       │
    └─────┼─────┼─────┼─────┼─────┼──────────┘
          │     │     │     │     │
          ▼     ▼     ▼     ▼     ▼
    ┌─────┴─────┴─────┴─────┴─────┴─────┐
    │        POWER DISTRIBUTION BOARD    │
    │  ┌─────────────────────────────┐  │
    │  │  12V→3.3V DC-DC Converters  │  │
    │  │  (One per layer, 60W each)  │  │
    │  └─────────────────────────────┘  │
    │  ┌─────────────────────────────┐  │
    │  │     Fan Controllers         │  │
    │  │     (PWM, 4-channel)        │  │
    │  └─────────────────────────────┘  │
    │  ┌─────────────────────────────┐  │
    │  │   Host Interface Power      │  │
    │  │   (PCIe/USB controllers)    │  │
    │  └─────────────────────────────┘  │
    └───────────────────────────────────┘
```

### Per-Layer Power

Each M.2 TPU module power requirements:
- Google Coral M.2: 2W typical, 4W peak
- Per layer (16 slots): 32W typical, 64W peak
- 6 layers total: 192W typical, 384W peak

Power budget per layer:
- M.2 modules: 64W max
- Heatsink fans (if any): 5W
- PCB/regulation losses: 6W
- **Total per layer: 75W**

### Host Connectivity

**Option A: PCIe Switch Architecture**
```
    Host PCIe x16 → PCIe Switch (PLX/Broadcom)
                         │
         ┌───────┬───────┼───────┬───────┐
         ▼       ▼       ▼       ▼       ▼
      Layer 1  Layer 2  Layer 3  Layer 4  ...
      (x4)     (x4)     (x4)     (x4)
```

**Option B: USB 3.x Hub Architecture**
```
    Host USB 3.2 → USB Hub (7-port)
                        │
        ┌───────┬───────┼───────┬───────┐
        ▼       ▼       ▼       ▼       ▼
     Layer 1  Layer 2  Layer 3  Layer 4  ...
     (Hub)    (Hub)    (Hub)    (Hub)
        │       │       │       │
      8-16    8-16    8-16    8-16
      TPUs    TPUs    TPUs    TPUs
```

**Option C: Direct PCIe per Layer**
- Each layer has dedicated PCIe x4 connection
- Requires motherboard with multiple PCIe slots
- Lowest latency, highest bandwidth

---

## Thermal Management

### Heat Dissipation Targets

| Component | TDP | Max Temp | Target Temp |
|-----------|-----|----------|-------------|
| Coral M.2 TPU | 4W | 85°C | <70°C |
| PCIe Switch | 8W | 105°C | <80°C |
| DC-DC Converter | 6W | 125°C | <90°C |

### Heatsink Design

**Per-M.2 Heatsink Specifications**
```
    HEATSINK PROFILE

         40mm
    ←───────────→
    ┌─┬─┬─┬─┬─┬─┬─┐  ─┬─
    │ │ │ │ │ │ │ │   │ 15mm (fin height)
    │ │ │ │ │ │ │ │   │
    ├─┴─┴─┴─┴─┴─┴─┤  ─┼─
    │  BASE PLATE │   │ 3mm
    └─────────────┘  ─┴─
         ↑
    Thermal pad contact
    to M.2 module

    Material: Aluminum 6063-T5
    Fin count: 8-12 fins
    Fin thickness: 1mm
    Fin spacing: 2-3mm
    Surface: Black anodized
```

### Thermal Zones

The tower is divided into thermal zones for monitoring:

```
    ┌─────────────────┐
    │    ZONE 6       │  ← Hottest (top layers)
    │    ZONE 5       │
    │    ZONE 4       │
    │    ZONE 3       │
    │    ZONE 2       │
    │    ZONE 1       │  ← Coolest (intake air)
    └─────────────────┘
```

Temperature sensors per zone:
- 2x per layer (opposite sides)
- 1x in central core
- 1x at exhaust

### Active Cooling Curves

```
    FAN SPEED vs TEMPERATURE

    RPM
    3000│                    ╱
        │                  ╱
    2500│                ╱
        │              ╱
    2000│            ╱
        │          ╱
    1500│        ╱
        │──────╱
    1000│
        └────────────────────────
         30   40   50   60   70   °C
              Hottest Zone Temp
```

---

## Controller System

### Management Board

A dedicated microcontroller board handles:

1. **Thermal Management**
   - Read all temperature sensors
   - PWM fan speed control
   - Thermal throttling alerts

2. **Power Monitoring**
   - Per-layer current sensing
   - Total system power reporting
   - Over-current protection

3. **Status Reporting**
   - USB/UART interface to host
   - LED status indicators
   - Web interface (optional)

### Controller Specifications

```
    MANAGEMENT BOARD BLOCK DIAGRAM

    ┌─────────────────────────────────────┐
    │         MANAGEMENT MCU              │
    │      (ESP32 / STM32 / RP2040)       │
    │                                     │
    │  ┌─────────┐  ┌─────────┐          │
    │  │ ADC     │  │ PWM     │          │
    │  │ Inputs  │  │ Outputs │          │
    │  │ (16ch)  │  │ (8ch)   │          │
    │  └────┬────┘  └────┬────┘          │
    │       │            │               │
    │  ┌────┴────┐  ┌────┴────┐          │
    │  │ Temp    │  │ Fan     │          │
    │  │ Sensors │  │ Headers │          │
    │  └─────────┘  └─────────┘          │
    │                                     │
    │  ┌─────────┐  ┌─────────┐          │
    │  │ USB     │  │ I2C     │          │
    │  │ Serial  │  │ Bus     │          │
    │  └─────────┘  └─────────┘          │
    └─────────────────────────────────────┘
```

---

## Assembly Views

### Exploded View

```
                   ┌───────────┐
                   │  Top Cap  │
                   │  + Fans   │
                   └─────┬─────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 6  │
                   └─────┬─────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 5  │
                   └─────┬─────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 4  │
                   └─────┬─────┘
                         │
         ┌───────────────┴───────────────┐
         │         CENTRAL CORE          │
         │      (runs full height)       │
         └───────────────┬───────────────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 3  │
                   └─────┬─────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 2  │
                   └─────┬─────┘
                         │
                   ┌─────┴─────┐
                   │  Layer 1  │
                   └─────┬─────┘
                         │
              ┌──────────┴──────────┐
              │   POWER DIST BOARD  │
              ├─────────────────────┤
              │   MANAGEMENT BOARD  │
              └──────────┬──────────┘
                         │
              ┌──────────┴──────────┐
              │      BASE UNIT      │
              │   + Filter + Fans   │
              └─────────────────────┘
```

### Tray Installation

```
    TRAY INSERTION (Side View)

    ┌─────────────────────────────┐
    │                             │
    │   ←═══════════════════════  │  Slide tray in
    │         [TRAY]              │
    │   ══════════════════════→   │
    │                             │
    └─────────────────────────────┘

    - Guide rails ensure alignment
    - Blind-mate power connectors
    - Locking tab secures tray
```

---

## Dimensions & Clearances

### Overall Dimensions

```
    FRONT VIEW                    SIDE VIEW

         300mm                        300mm
    ←─────────────→              ←─────────────→

    ┌─────────────┐  ─┬─         ┌─────────────┐  ─┬─
    │  ═══════   │   │ 80mm     │  ═══════   │   │
    ├─────────────┤  ─┼─         ├─────────────┤  ─┼─
    │             │   │          │             │   │
    │             │   │          │             │   │
    │             │   │ 520mm    │             │   │ 520mm
    │             │   │          │             │   │
    │             │   │          │             │   │
    │             │   │          │             │   │
    ├─────────────┤  ─┼─         ├─────────────┤  ─┼─
    │  ░░░░░░░░░ │   │ 80mm     │  ░░░░░░░░░ │   │
    └─────────────┘  ─┴─         └─────────────┘  ─┴─

    Total Height: 680mm (26.8")
    Footprint: 300mm x 300mm (11.8" x 11.8")
```

### Internal Clearances

| Clearance | Minimum | Recommended |
|-----------|---------|-------------|
| M.2 to M.2 (same layer) | 15mm | 20mm |
| Layer to layer | 60mm | 80mm |
| M.2 to outer wall | 20mm | 30mm |
| Central core to M.2 | 40mm | 50mm |

---

## Bill of Materials (Summary)

### Structural Components

| Item | Qty | Description |
|------|-----|-------------|
| Base frame | 1 | Aluminum, machined |
| Central core tube | 1 | 80mm OD perforated aluminum |
| Support rails | 6 | Aluminum extrusion, 500mm |
| Top exhaust assembly | 1 | Aluminum, fan mounts |
| Outer mesh shell | 1 | Perforated steel, optional |
| Layer trays | 6 | Aluminum base plates |

### Electrical Components

| Item | Qty | Description |
|------|-----|-------------|
| ATX PSU | 1 | 650-850W, 80+ Gold |
| M.2 carrier PCBs | 6-12 | Custom, 8-16 slots each |
| DC-DC converters | 6 | 12V→3.3V, 60W |
| Power distribution board | 1 | Custom PCB |
| Management board | 1 | ESP32/STM32 based |

### Cooling Components

| Item | Qty | Description |
|------|-----|-------------|
| Intake fans | 2-3 | 80-120mm, high static pressure |
| Exhaust fans | 2-3 | 120-140mm, high airflow |
| M.2 heatsinks | 48-96 | 40x20x15mm, aluminum |
| Thermal pads | 48-96 | 1mm thick, >6 W/mK |
| Air filter cartridge | 1 | MERV 8-13 pleated |

### Connectivity

| Item | Qty | Description |
|------|-----|-------------|
| PCIe switch (Option A) | 1 | PLX/Broadcom 48-lane |
| USB hubs (Option B) | 6-8 | USB 3.0, 7-port |
| Cables, internal | Various | PCIe, USB, power |

---

## Performance Estimates

### Cooling Performance

| Configuration | Ambient | Max TPU Temp | Airflow |
|---------------|---------|--------------|---------|
| 48 TPU (8/layer) | 25°C | 55°C | 150 CFM |
| 72 TPU (12/layer) | 25°C | 62°C | 200 CFM |
| 96 TPU (16/layer) | 25°C | 68°C | 280 CFM |

### Compute Performance

With Google Coral Edge TPU M.2 modules:
- Per TPU: 4 TOPS (INT8)
- 48 TPUs: 192 TOPS
- 96 TPUs: 384 TOPS

### Power Efficiency

| Load | Power Draw | Efficiency |
|------|------------|------------|
| Idle | ~80W | - |
| 50% | ~200W | 1.0 TOPS/W |
| 100% | ~400W | 0.96 TOPS/W |

---

## Future Considerations

1. **Liquid Cooling Option**: Center core could be replaced with liquid cooling loop
2. **Hot-Swap Trays**: Add blind-mate connectors for tool-less tray replacement
3. **Remote Management**: BMC-style out-of-band management
4. **Rack Mount Version**: 19" rack-mountable variant
5. **Higher Density**: M.2 2242 form factor for smaller modules

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-01-27 | Initial design document |
