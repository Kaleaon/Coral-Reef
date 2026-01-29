include <parameters.scad>;

module base_unit() {
    // Base Platform housing intake fans
    color("darkgrey")
    union() {
        difference() {
            cylinder(h=base_height, r=tower_radius);

            // Intake Vents around perimeter
            for(a=[0:20:360]) {
                rotate([0,0,a])
                translate([tower_radius, 0, base_height/2])
                cube([20, 10, base_height-20], center=true);
            }

            // Inner hollow for plenum
            translate([0,0,5])
            cylinder(h=base_height, r=tower_radius-10);

            // Central air passage to core
            translate([0,0,-1])
            cylinder(h=base_height+2, r=inner_core_radius);
        }

        // Feet
        for(a=[45:90:360]) {
            rotate([0,0,a])
            translate([tower_radius-40, 0, -10])
            cylinder(h=10, r=15);
        }
    }
}

module top_unit() {
    // Top Exhaust Assembly
    color("darkgrey")
    difference() {
        cylinder(h=top_height, r=tower_radius);

        // Main exhaust opening
        translate([0,0,-1])
        cylinder(h=top_height+2, r=tower_radius-20);
    }

    // Fan mounting plate
    translate([0,0,5])
    difference() {
        cylinder(h=5, r=tower_radius-20);

        // Fan holes (3x 120mm pattern approx)
        for(a=[0:120:360]) {
            rotate([0,0,a])
            translate([tower_radius/2 + 10, 0, -1])
            cylinder(h=7, r=55);
        }
    }
}

module enclosure() {
    // Base Unit
    base_unit();

    // Top Exhaust (positioned at top of structure)
    // Note: total_height includes base, layers, top.
    translate([0, 0, total_height - top_height])
    top_unit();
}

enclosure();
