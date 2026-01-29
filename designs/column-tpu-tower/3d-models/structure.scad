include <parameters.scad>;

module structure() {
    // Central Core Tube
    color("silver")
    difference() {
        cylinder(h=total_height, r=inner_core_radius);
        translate([0,0,-1])
        cylinder(h=total_height+2, r=inner_core_radius-2); // 2mm wall thickness

        // Perforations
        // Create a pattern of holes
        // This can be computationally expensive in preview,
        // so we limit it or make it conditional.
        // For this task, we'll do a simple pattern.
        for(z=[20:20:total_height-20]) {
            for(a=[0:45:360]) {
                 rotate([0,0,a + (z%40==0?22.5:0)]) // Staggered
                 translate([inner_core_radius, 0, z])
                 rotate([0,90,0])
                 cylinder(h=10, r=4, center=true);
            }
        }
    }

    // Support Rails
    // Aluminum extrusions
    color("gray")
    for(i=[0:rail_count-1]) {
        rotate([0, 0, i * (360/rail_count) + 30])
        translate([rail_offset, 0, total_height/2])
        cube([rail_depth, rail_width, total_height], center=true);
    }
}

structure();
