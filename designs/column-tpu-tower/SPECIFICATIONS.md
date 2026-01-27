# Coral-Reef Column TPU Tower - Technical Specifications

## Physical Specifications

### Dimensions

| Measurement | Metric | Imperial |
|-------------|--------|----------|
| Total Height | 680mm | 26.8" |
| Base Width | 300mm | 11.8" |
| Base Depth | 300mm | 11.8" |
| Weight (empty) | ~8kg | ~17.6 lbs |
| Weight (loaded) | ~12kg | ~26.4 lbs |

### Layer Specifications

| Parameter | Value |
|-----------|-------|
| Number of Layers | 6 (expandable to 8) |
| Layer Height | 70mm |
| Layer Spacing | 10mm |
| Tray Thickness | 3mm aluminum |
| M.2 Slots per Layer | 8 / 12 / 16 (configurable) |

### Central Airflow Core

| Parameter | Value |
|-----------|-------|
| Outer Diameter | 80mm |
| Wall Thickness | 2mm |
| Material | Aluminum 6061-T6 |
| Perforation Pattern | Staggered holes |
| Hole Diameter | 8mm (bottom) to 12mm (top) |
| Open Area | 40% |

---

## Airflow Specifications

### Fan Specifications

#### Intake Fans (Base)

| Parameter | Option A | Option B |
|-----------|----------|----------|
| Size | 3x 80mm | 2x 120mm |
| Type | High Static Pressure | High Static Pressure |
| Speed Range | 1500-3500 RPM | 1000-2500 RPM |
| Airflow | 25-50 CFM each | 50-90 CFM each |
| Static Pressure | 2.5-4.0 mmH2O | 2.0-3.5 mmH2O |
| Noise | 20-40 dBA | 18-35 dBA |
| Connector | 4-pin PWM | 4-pin PWM |

**Recommended Models:**
- Noctua NF-A8 PWM (80mm)
- Noctua NF-F12 industrialPPC (120mm)
- Delta AFB0812SH (80mm, high performance)

#### Exhaust Fans (Top)

| Parameter | Option A | Option B |
|-----------|----------|----------|
| Size | 3x 120mm | 2x 140mm |
| Type | High Airflow | High Airflow |
| Speed Range | 800-2000 RPM | 600-1500 RPM |
| Airflow | 40-80 CFM each | 60-100 CFM each |
| Static Pressure | 1.0-2.0 mmH2O | 0.8-1.5 mmH2O |
| Noise | 15-32 dBA | 12-28 dBA |
| Connector | 4-pin PWM | 4-pin PWM |

**Recommended Models:**
- Noctua NF-A12x25 PWM (120mm)
- Noctua NF-A14 PWM (140mm)
- Arctic P12 PWM PST (120mm, budget)

### Airflow Performance

| Configuration | Min Airflow | Max Airflow | Recommended |
|---------------|-------------|-------------|-------------|
| 48 TPU (8/layer) | 100 CFM | 300 CFM | 150 CFM |
| 72 TPU (12/layer) | 150 CFM | 350 CFM | 220 CFM |
| 96 TPU (16/layer) | 200 CFM | 400 CFM | 300 CFM |

### Air Velocity Targets

| Location | Target Velocity |
|----------|-----------------|
| Intake plenum | 2.0-3.0 m/s |
| Central core | 3.0-5.0 m/s |
| Across heatsinks | 2.0-4.0 m/s |
| Exhaust | 3.0-6.0 m/s |

---

## Filtration Specifications

### Pre-Filter

| Parameter | Value |
|-----------|-------|
| Type | Washable aluminum mesh |
| Mesh Size | 40-60 mesh (250-400 micron) |
| Frame | Aluminum, snap-fit |
| Dimensions | 280mm x 280mm x 5mm |
| Maintenance | Wash monthly |
| Lifespan | Indefinite (washable) |

### Main Filter

| Parameter | Standard | High-Efficiency |
|-----------|----------|-----------------|
| Type | Pleated synthetic | HEPA-style |
| Rating | MERV 8 | MERV 13 |
| Particle Capture | >70% @ 3-10μm | >90% @ 1-3μm |
| Initial ΔP | 0.10" WC | 0.25" WC |
| Max ΔP | 0.50" WC | 0.75" WC |
| Dimensions | 280mm x 280mm x 25mm | 280mm x 280mm x 25mm |
| Replacement | 3-6 months | 2-4 months |

### Optional Carbon Filter

| Parameter | Value |
|-----------|-------|
| Type | Activated carbon pad |
| Purpose | VOC/odor absorption |
| Thickness | 5mm |
| Replacement | 6-12 months |

---

## Electrical Specifications

### Power Supply Requirements

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Wattage | 550W | 750W |
| Efficiency | 80+ Bronze | 80+ Gold |
| 12V Rail | 40A | 60A |
| 5V Rail | 15A | 20A |
| Form Factor | ATX | ATX |

### Power Consumption

| State | 48 TPU | 72 TPU | 96 TPU |
|-------|--------|--------|--------|
| Idle | 60W | 75W | 95W |
| 25% Load | 110W | 150W | 190W |
| 50% Load | 160W | 220W | 285W |
| 75% Load | 210W | 295W | 380W |
| 100% Load | 260W | 370W | 480W |

*Includes fans, controllers, and conversion losses*

### Per-Module Power

| Parameter | Coral M.2 TPU |
|-----------|---------------|
| Voltage | 3.3V |
| Idle Current | 150mA |
| Typical Current | 600mA |
| Peak Current | 1200mA |
| Idle Power | 0.5W |
| Typical Power | 2.0W |
| Peak Power | 4.0W |

### Power Distribution

| Rail | Source | Load |
|------|--------|------|
| 12V | PSU | DC-DC converters, fans |
| 5V | PSU | USB hubs, management |
| 3.3V | DC-DC | M.2 TPU modules |
| 5VSB | PSU | Management (standby) |

---

## Thermal Specifications

### Operating Temperatures

| Component | Min | Max | Target |
|-----------|-----|-----|--------|
| Ambient (operating) | 0°C | 40°C | 20-25°C |
| Ambient (storage) | -20°C | 60°C | - |
| M.2 TPU | 0°C | 85°C | <70°C |
| Heatsinks | - | 90°C | <75°C |
| PCB | - | 105°C | <85°C |

### Heatsink Specifications

| Parameter | Value |
|-----------|-------|
| Material | Aluminum 6063-T5 |
| Dimensions | 40mm x 22mm x 18mm |
| Fin Count | 10 |
| Fin Thickness | 1.0mm |
| Fin Spacing | 2.5mm |
| Base Thickness | 3.0mm |
| Surface Finish | Black anodized |
| Thermal Resistance | ~8°C/W (with airflow) |

### Thermal Interface Material

| Parameter | Value |
|-----------|-------|
| Type | Silicone thermal pad |
| Thickness | 1.0mm |
| Thermal Conductivity | >6.0 W/mK |
| Hardness | Shore 00-40 |
| Operating Range | -40°C to 200°C |

---

## Connectivity Specifications

### Option A: PCIe Architecture

| Parameter | Value |
|-----------|-------|
| Host Interface | PCIe 3.0 x16 |
| Switch IC | PLX PEX8748 or Broadcom |
| Downstream Ports | 6x PCIe x4 |
| Per-Layer Bandwidth | 4 GB/s |
| Total Bandwidth | 16 GB/s |
| Latency | <1μs switch latency |

### Option B: USB Architecture

| Parameter | Value |
|-----------|-------|
| Host Interface | USB 3.2 Gen 1 (5 Gbps) |
| Root Hub | 7-port USB 3.0 hub |
| Layer Hubs | 4-port USB 3.0 each |
| Per-TPU Bandwidth | 400 MB/s theoretical |
| Practical Bandwidth | 200-300 MB/s |

### Management Interface

| Parameter | Value |
|-----------|-------|
| Protocol | USB CDC (serial) |
| Baud Rate | 115200 default |
| Optional | Ethernet (10/100) |
| Web Interface | HTTP on port 80 |

---

## Environmental Specifications

### Operating Environment

| Parameter | Value |
|-----------|-------|
| Temperature | 0°C to 40°C |
| Humidity | 10% to 90% RH (non-condensing) |
| Altitude | 0 to 3000m |
| Vibration | 0.5G, 10-500Hz |

### Acoustic Specifications

| Mode | Sound Level |
|------|-------------|
| Idle | <30 dBA |
| Normal Operation | 35-40 dBA |
| Full Load | 40-48 dBA |
| Maximum Cooling | <55 dBA |

*Measured at 1m distance*

### Compliance (Targets)

- FCC Part 15 Class B
- CE Mark
- RoHS compliant
- UL/CSA (power supply)

---

## Connector Specifications

### External Connectors

| Connector | Type | Purpose |
|-----------|------|---------|
| Power | IEC C14 | AC input |
| Host Data | PCIe x16 or USB-B | Primary data |
| Management | USB-B mini | Serial console |
| Ethernet | RJ-45 (optional) | Remote management |

### Internal Connectors

| Connector | Type | Purpose |
|-----------|------|---------|
| Layer Power | Molex Mini-Fit Jr 8-pin | 12V + 3.3V |
| Layer Data | PCIe x4 or USB 3.0 | Per-layer data |
| Fan Power | 4-pin PWM | Fan control |
| Sensors | JST-XH 3-pin | Temperature |

---

## Reliability Specifications

### Target MTBF

| Component | MTBF |
|-----------|------|
| Fan (per unit) | 70,000 hours |
| PSU | 100,000 hours |
| M.2 TPU | 50,000 hours |
| System | >30,000 hours |

### Maintenance Schedule

| Task | Interval |
|------|----------|
| Pre-filter cleaning | Monthly |
| Main filter replacement | 3-6 months |
| Fan inspection | 6 months |
| Thermal paste/pad check | 12 months |
| Full inspection | Annually |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-27 | - | Initial specifications |
