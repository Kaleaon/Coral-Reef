# Coral-Reef Column TPU Tower - Airflow Design

## Airflow Philosophy

The Coral-Reef tower uses a **Central Chimney Architecture** that combines:
1. Natural convection (hot air rises)
2. Forced convection (intake + exhaust fans)
3. Radial distribution (center-out airflow per layer)

This creates a highly efficient cooling system that scales with heat load.

---

## Primary Airflow Path

### Full System Cross-Section

```
                         EXHAUST
                    ↑    ↑    ↑    ↑
              ╔═════╧════╧════╧════╧═════╗
              ║   EXHAUST FAN ASSEMBLY   ║  ← 2-3x 120mm fans (PULL)
              ║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ║
              ╠══════════╤══════════════╣
              ║          │              ║
    ┌─────────╫──────────┼──────────────╫─────────┐
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 6
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    ├─────────╫──────────┼──────────────╫─────────┤
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 5
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    ├─────────╫──────────┼──────────────╫─────────┤
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 4
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    ├─────────╫──────────┼──────────────╫─────────┤
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 3
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    ├─────────╫──────────┼──────────────╫─────────┤
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 2
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    ├─────────╫──────────┼──────────────╫─────────┤
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │  Layer 1
    │←←←←←←←←←║←←←←↑↑↑←←←│←←←↑↑↑←←←←←←←║→→→→→→→→→│
    │ HS HS HS║    ↑↑↑   │   ↑↑↑        ║HS HS HS │
    └─────────╫──────────┼──────────────╫─────────┘
              ║          │              ║
              ║    ↑↑↑   │   ↑↑↑        ║  ← Central Core Tube
              ║    ↑↑↑   │   ↑↑↑        ║    (Perforated)
              ╠══════════╧══════════════╣
              ║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ║
              ║    INTAKE FAN ASSEMBLY  ║  ← 2-3x 80/120mm fans (PUSH)
              ║   ░░░░░░░░░░░░░░░░░░░░  ║  ← Air Filter
              ╚═════╤════╤════╤════╤═════╝
                    ↑    ↑    ↑    ↑
                         INTAKE

    Legend:
    HS = Heatsink (M.2 TPU underneath)
    ↑  = Vertical airflow (upward)
    ←→ = Horizontal airflow (radial)
    ▓  = Fan
    ░  = Filter media
    ║  = Outer wall / structure
```

---

## Layer Airflow Detail

### Top View - Single Layer

```
                           300mm
            ←────────────────────────────────→

        ↑   ┌────────────────────────────────┐   ↑
        │   │ ↖                            ↗ │   │
        │   │   ↖    [HS]      [HS]     ↗    │   │
        │   │      ↖               ↗         │   │
        │   │         ↖        ↗             │   │
        │   │  [HS]     ╔════╗      [HS]     │   │
        │   │     ↖     ║    ║    ↗          │   │
    E   │   │       ←←  ║AIR ║  →→           │   │   W
    X   │   │       ←←  ║CORE║  →→           │   │   A
    H   │   │       ←←  ║    ║  →→           │   │   R
    A   │   │     ↙     ╚════╝    ↘          │   │   M
    U   │   │  [HS]                  [HS]    │   │
    S   │   │         ↙        ↘             │   │   A
    T   │   │      ↙               ↘         │   │   I
        │   │   ↙    [HS]      [HS]     ↘    │   │   R
        │   │ ↙                            ↘ │   │
        ↑   └────────────────────────────────┘   ↑
                            ↓
                      WARM AIR RISES
                   TO EXHAUST AT TOP

    Legend:
    [HS] = Heatsink with M.2 TPU
    ←→↗↘ = Airflow direction (radial outward)
    ╔══╗ = Central air core (80mm diameter)
```

### Airflow Velocity Zones

```
    TOP VIEW - VELOCITY MAP

         ┌────────────────────────────────┐
         │  LOW    LOW    LOW    LOW      │
         │    ↘                  ↙        │
         │       MED        MED           │
         │          ↘    ↙                │
         │             ╔════╗              │
         │    MED  ←←  ║HIGH║  →→  MED    │
         │             ╚════╝              │
         │          ↙    ↘                │
         │       MED        MED           │
         │    ↙                  ↘        │
         │  LOW    LOW    LOW    LOW      │
         └────────────────────────────────┘

    Velocity Zones:
    HIGH = 4-6 m/s (core exit)
    MED  = 2-4 m/s (heatsink zone)
    LOW  = 1-2 m/s (outer edges)
```

---

## Central Core Design

### Core Tube Perforation Pattern

```
    CORE TUBE - UNROLLED VIEW

    TOP ─────────────────────────────────────────── TOP
        │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │    ○   ○   ○   ○   ○   ○   ○   ○   ○    │  ← 12mm holes
    L6  │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │────────────────────────────────────────│
        │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │    ○   ○   ○   ○   ○   ○   ○   ○   ○    │  ← 11mm holes
    L5  │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │────────────────────────────────────────│
        │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │    ○   ○   ○   ○   ○   ○   ○   ○   ○    │  ← 10mm holes
    L4  │  ○   ○   ○   ○   ○   ○   ○   ○   ○   ○  │
        │────────────────────────────────────────│
        │  o   o   o   o   o   o   o   o   o   o  │
        │    o   o   o   o   o   o   o   o   o    │  ← 9mm holes
    L3  │  o   o   o   o   o   o   o   o   o   o  │
        │────────────────────────────────────────│
        │  o   o   o   o   o   o   o   o   o   o  │
        │    o   o   o   o   o   o   o   o   o    │  ← 8mm holes
    L2  │  o   o   o   o   o   o   o   o   o   o  │
        │────────────────────────────────────────│
        │  o   o   o   o   o   o   o   o   o   o  │
        │    o   o   o   o   o   o   o   o   o    │  ← 8mm holes
    L1  │  o   o   o   o   o   o   o   o   o   o  │
        │────────────────────────────────────────│
    BTM ─────────────────────────────────────────── BTM
              ↑                           ↑
          Staggered hole pattern for even distribution

    Note: Hole size increases toward top to compensate
          for decreasing pressure differential
```

### Core Tube Cross-Section

```
    CORE TUBE - CROSS SECTION

              80mm OD
         ←───────────→
         ┌───────────┐
         │░░░░░░░░░░░│  ← 2mm wall thickness
         │░┌───────┐░│
         │░│       │░│
         │░│  AIR  │░│  76mm ID (internal diameter)
         │░│ FLOW  │░│
         │░│   ↑   │░│
         │░└───────┘░│
         │░░░░░░░░░░░│
         └───────────┘

    Material: Aluminum 6061-T6
    Finish: Mill finish or anodized
```

---

## Heatsink Airflow Optimization

### Heatsink Fin Orientation

```
    CORRECT ORIENTATION (Parallel to airflow)

         Airflow →→→→→→→→→→→→→
                 ╔═╤═╤═╤═╤═╤═╤═╤═╗
                 ║ │ │ │ │ │ │ │ ║
                 ║ │ │ │ │ │ │ │ ║  ← Fins aligned with flow
                 ║ │ │ │ │ │ │ │ ║
                 ╚═╧═╧═╧═╧═╧═╧═╧═╝
                 └───────────────┘
                    M.2 TPU Module


    INCORRECT ORIENTATION (Perpendicular - DO NOT USE)

         Airflow →→→→→→→→→→→→→
                 ╔═══════════════╗
                 ╠═══════════════╣
                 ╠═══════════════╣  ← Fins block flow
                 ╠═══════════════╣
                 ╚═══════════════╝
                 └───────────────┘
                    M.2 TPU Module
```

### M.2 + Heatsink Assembly

```
    SIDE VIEW - HEATSINK ASSEMBLY

                    40mm
               ←───────────→

    Airflow →  ┌─┬─┬─┬─┬─┬─┬─┐  ─┬─
               │ │ │ │ │ │ │ │   │ 15mm fins
               │ │ │ │ │ │ │ │   │
               ├─┴─┴─┴─┴─┴─┴─┤  ─┼─ 3mm base
               │░░░░░░░░░░░░░│  ─┼─ 1mm thermal pad
               │ M.2 MODULE  │   │ 2.2mm
               └─────────────┘  ─┴─
               │             │
               └─────────────┘
                  PCB Carrier

    Total Stack Height: ~21mm
```

---

## Filter System Airflow

### Filter Assembly Detail

```
    FILTER SECTION - SIDE VIEW

    From external  ────────────────────────────→  To fans
    environment

         │                                    │
         │    ┌──────────────────────────┐   │
         │    │ ░░░░░░░░░░░░░░░░░░░░░░░░ │   │
         │    │ ░░ PRE-FILTER (mesh) ░░░ │   │
         │    │ ░░░░░░░░░░░░░░░░░░░░░░░░ │   │
         ↓    ├──────────────────────────┤   ↓
              │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
         →→→→ │ ▓▓ MAIN FILTER (MERV) ▓▓ │ →→→→
              │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
         ↓    ├──────────────────────────┤   ↓
         │    │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │   │
         │    │ ▒▒ CARBON (optional) ▒▒▒ │   │
         │    │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │   │
         │    └──────────────────────────┘   │
         │                                    │
         ↓                                    ↓
              ════════════════════════════
                    INTAKE FANS
```

### Filter Pressure Drop

```
    PRESSURE vs FILTER LIFE

    ΔP (Pa)
    100│                           ╱
       │                         ╱
    80 │                       ╱    ← Replace filter
       │                     ╱
    60 │                   ╱
       │                 ╱
    40 │              ╱
       │           ╱
    20 │────────╱                   ← New filter
       │
     0 └────────────────────────────
       0    1    2    3    4    5   months
                 Filter Age
```

---

## Thermal Zones and Monitoring

### Temperature Sensor Placement

```
    SIDE VIEW - SENSOR LOCATIONS

         ╔════════════════════════════╗
         ║          (T13)             ║  ← Exhaust temp
         ╠════════════════════════════╣
         ║ (T11)     │      (T12)     ║  Layer 6
         ╟───────────┼────────────────╢
         ║ (T9)      │       (T10)    ║  Layer 5
         ╟───────────┼────────────────╢
         ║ (T7)      │       (T8)     ║  Layer 4
         ╟──────────(TC)──────────────╢  ← Core temp
         ║ (T5)      │       (T6)     ║  Layer 3
         ╟───────────┼────────────────╢
         ║ (T3)      │       (T4)     ║  Layer 2
         ╟───────────┼────────────────╢
         ║ (T1)      │       (T2)     ║  Layer 1
         ╠════════════════════════════╣
         ║          (T0)              ║  ← Intake temp
         ╚════════════════════════════╝

    Sensor count: 14 total
    - T0: Intake air (ambient reference)
    - T1-T12: Layer sensors (2 per layer)
    - TC: Core center
    - T13: Exhaust air
```

### Expected Temperature Profile

```
    TEMPERATURE GRADIENT (Typical @ 50% load)

    Height   │ Core Temp │ Edge Temp │ Delta
    ─────────┼───────────┼───────────┼───────
    Exhaust  │   52°C    │   50°C    │  +2°C
    Layer 6  │   48°C    │   46°C    │  +2°C
    Layer 5  │   44°C    │   42°C    │  +2°C
    Layer 4  │   40°C    │   39°C    │  +1°C
    Layer 3  │   36°C    │   35°C    │  +1°C
    Layer 2  │   32°C    │   32°C    │   0°C
    Layer 1  │   28°C    │   28°C    │   0°C
    Intake   │   25°C    │   25°C    │   0°C

    Note: Core slightly warmer due to rising hot air
```

---

## Fan Control Strategy

### PWM Control Curves

```
    FAN SPEED vs HOTTEST ZONE TEMPERATURE

    100%│                          ╱────
        │                        ╱
     80%│                      ╱
        │                    ╱
     60%│                  ╱
        │                ╱
     40%│──────────────╱
        │  Minimum
     20%│  Fan Speed
        │
      0%└────────────────────────────────
        20    30    40    50    60    70   °C
              Hottest Zone Temperature

    Zones:
    20-35°C: Minimum speed (quiet operation)
    35-55°C: Linear ramp
    55-65°C: High speed cooling
    65-70°C: Maximum speed
    >70°C: Thermal alert
```

### Intake vs Exhaust Balance

```
    BALANCED AIRFLOW (Slight Negative Pressure)

                    EXHAUST: 165 CFM
                         ↑↑↑↑↑
                    ╔════╧════╗
                    ║         ║
                    ║  TOWER  ║  ← Slight vacuum
                    ║  -0.1"  ║     prevents dust
                    ║   WC    ║     infiltration
                    ║         ║
                    ╚════╤════╝
                         ↑↑↑↑↑
                    INTAKE: 150 CFM

    Ratio: Exhaust = 1.1 × Intake
```

---

## Airflow Optimization Tips

### Installation Considerations

1. **Minimum Clearances**
   - Top exhaust: 150mm clearance above
   - Sides: 50mm clearance minimum
   - Bottom intake: Elevated 50mm from surface

2. **Room Placement**
   - Avoid corners (restricts airflow)
   - Keep away from heat sources
   - Ensure ambient below 30°C

3. **Cable Management**
   - Route cables away from core
   - Use flat cables where possible
   - Avoid blocking edge exhaust paths

### Performance Tuning

| Symptom | Cause | Solution |
|---------|-------|----------|
| High top layer temps | Insufficient exhaust | Increase exhaust fan speed |
| Uneven layer temps | Core obstruction | Check for blockages |
| High pressure drop | Dirty filter | Clean/replace filter |
| Noise at idle | Fans too fast | Adjust PWM minimum |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-27 | Initial airflow design |
