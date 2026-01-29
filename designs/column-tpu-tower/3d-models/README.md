# 3D CAD Models for Coral-Reef Column Tower

This directory contains parametric 3D models for the Coral-Reef Column TPU Tower, generated using [OpenSCAD](https://openscad.org/).

## Files

- **`assembly.scad`**: The main file that assembles all components into the full tower model. Open this to see the complete design.
- **`tray.scad`**: Detailed model of a single 16-TPU layer tray.
- **`enclosure.scad`**: Models for the Base Platform (intake) and Top Exhaust Assembly.
- **`structure.scad`**: Structural components including the central perforated core and vertical rails.
- **`parameters.scad`**: Shared configuration variables (dimensions, clearances).

## How to View

1. Install [OpenSCAD](https://openscad.org/downloads.html).
2. Open `assembly.scad` to view the full tower.
3. Use `Design > Render` (F6) to generate the geometry.
4. Use `File > Export` to save as STL for 3D printing.

## Customization

You can modify `parameters.scad` to adjust:
- Tower height and diameter
- Number of layers
- TPU slots per layer
- Rail dimensions

## Components

### Base Unit
The 60mm base houses the intake fans and filter cartridge slots.

### Trays
Each tray holds 16 M.2 modules in a radial pattern. The model includes placeholders for the M.2 PCB and heatsinks.

### Core
The 80mm central core is perforated to distribute air from the base plenum to each layer.
