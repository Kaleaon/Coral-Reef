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
            // Assuming rails pass through or mount to edge
            for(i=[0:rail_count-1]) {
                rotate([0, 0, i * (360/rail_count) + 30]) // Offset from M.2s
                translate([rail_offset, 0, -1])
                // Square cutout for rail pass-through
                cube([rail_depth+1, rail_width+1, tray_thickness+2], center=true);
            }

            // Ventilation Slots (between M.2s)
            for(i=[0:m2_slot_count-1]) {
                rotate([0, 0, i * (360/m2_slot_count) + (360/m2_slot_count)/2])
                translate([inner_core_radius + 15, -5, -1])
                cube([m2_length-10, 10, tray_thickness+2]);
            }
        }

        // Populate with M.2 Modules
        for(i=[0:m2_slot_count-1]) {
            rotate([0, 0, i * (360/m2_slot_count)])
            translate([inner_core_radius + 5, -m2_width/2, tray_thickness])
            m2_module();
        }
    }
}

tray();
