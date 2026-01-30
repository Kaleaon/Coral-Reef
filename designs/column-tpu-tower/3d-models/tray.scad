include <parameters.scad>;

module m2_module() {
    // Standard M.2 2280 module representation

    // PCB
    color(color_pcb)
    cube([m2_length, m2_width, 1]);

    // Heatsink (as per design specs: 40x20x15mm minimum)
    // Centered on the module roughly
    translate([20, 1, 1]) // Small offset
    color(color_black)
    cube([40, 20, 15]);

    // Connector Gold Fingers area (visual)
    color("gold")
    translate([-2, 1, 0])
    cube([2, 20, 1]);
}

module tray() {
    union() {
        difference() {
            // Base plate
            color(color_aluminum)
            cylinder(h=tray_thickness, r=tray_diameter/2);

            // Central Air Hole
            translate([0,0,-1])
            cylinder(h=tray_thickness+2, r=inner_core_radius);

            // Rail Cutouts/Mounting points
            // Rails at 30, 90, 150... (offset 30)
            for(i=[0:rail_count-1]) {
                rotate([0, 0, i * (360/rail_count) + 30]) // Offset from M.2s
                translate([rail_offset, 0, -1])
                // Square cutout for rail pass-through
                cube([rail_depth+1, rail_width+1, tray_thickness+2], center=true);
            }

            // Ventilation Slots (between M.2s)
            // Adjusted for 16 slots, but we only have 8 per side.
            // Let's put slots between the pairs.
             for(i=[0:7]) {
                rotate([0, 0, i * (360/8) + 15 + 22.5]) // Offset to be between M.2s
                translate([inner_core_radius + 15, -5, -1])
                cube([m2_length-10, 10, tray_thickness+2]);
            }
        }

        // Populate with M.2 Modules
        // Split 16 modules into Top (8) and Bottom (8) to resolve spatial conflict
        // and rotated by 15 degrees to avoid Rail collision at 125mm radius.

        // Top Side (8 modules)
        for(i=[0:7]) {
            rotate([0, 0, i * (360/8) + 15])
            translate([inner_core_radius + 5, -m2_width/2, tray_thickness])
            m2_module();
        }

        // Bottom Side (8 modules)
        // Offset by half-step (22.5 deg) relative to Top
        // 15 + 22.5 = 37.5 deg start
        for(i=[0:7]) {
            rotate([0, 0, i * (360/8) + 15 + 22.5])
            translate([inner_core_radius + 5, m2_width/2, 0]) // Start at z=0 (bottom of tray)
            rotate([180,0,0]) // Flip upside down so heatsink points down
            m2_module();
        }
    }
}

tray();
