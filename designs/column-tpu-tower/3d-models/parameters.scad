// Coral-Reef Column TPU Tower - Parameters
// Based on designs/column-tpu-tower/DESIGN.md

// Global Resolution
$fn = 60; // Medium resolution for preview

// Overall Dimensions
tower_diameter = 300;
tower_radius = tower_diameter / 2;
inner_core_diameter = 80;
inner_core_radius = inner_core_diameter / 2;

// Vertical Dimensions
base_height = 60;
top_height = 80;
layer_spacing = 80; // Center-to-center vertical distance
tray_thickness = 3;
num_layers = 6;

// Calculated Total Height
// Base + (Layers * Spacing) + Top?
// No, Base + Layers Stack + Top
// Let's assume the layers stack on the rails.
total_height = base_height + (num_layers * layer_spacing) + top_height;

// Structural Rails
rail_count = 6;
rail_width = 20; // 2020 extrusion
rail_depth = 20;
rail_offset = tower_radius - 20; // Inset from edge

// Tray Details
tray_diameter = tower_diameter - 5; // Slight clearance
m2_slot_count = 16;
m2_width = 22;
m2_length = 80;

// Colors
color_aluminum = [0.9, 0.9, 0.9];
color_pcb = [0.2, 0.5, 0.2];
color_black = [0.2, 0.2, 0.2];
