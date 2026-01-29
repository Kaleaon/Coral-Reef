include <parameters.scad>;
use <enclosure.scad>;
use <structure.scad>;
use <tray.scad>;

// Global View Options
$fn = 50;

// 1. Enclosure
// Base and Top Cap
enclosure();

// 2. Structural Frame
// Central Core and Rails running full height
structure();

// 3. Compute Layers (Trays)
// We stack them starting above the base
start_z = base_height + 10; // Clearance above intake plenum

for(i=[0:num_layers-1]) {
    // Alternate rotation for visual variety or airflow if needed
    // But design says "Radial Airflow", so alignment is good.

    translate([0, 0, start_z + (i * layer_spacing)])
    tray();
}

// Optional: Cutaway view if variable set
// difference() { ... }
