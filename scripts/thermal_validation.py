import sys

def validate_thermal_design():
    print("Coral-Reef Thermal Validation Simulation")
    print("========================================")

    # Constants
    AMBIENT_TEMP = 25.0  # deg C
    MAX_TPU_TEMP = 85.0  # deg C
    TARGET_TPU_TEMP = 70.0  # deg C

    # Heat Sources
    TPU_POWER_PEAK = 4.0  # W
    TPU_POWER_TYPICAL = 2.0  # W
    TPUS_PER_LAYER = 16
    LAYERS = 6
    TOTAL_TPUS = TPUS_PER_LAYER * LAYERS

    SYSTEM_POWER_MAX = 480.0  # W (Total system including fans)

    # Cooling System
    AIRFLOW_CFM = 300.0  # Recommended
    AIR_DENSITY = 1.184  # kg/m^3 @ 25C
    CP_AIR = 1006.0      # J/kg*K
    HEATSINK_R_TH = 8.0  # C/W

    print(f"Ambient Temperature: {AMBIENT_TEMP} C")
    print(f"Max Allowed TPU Temp: {MAX_TPU_TEMP} C")
    print(f"Target TPU Temp: {TARGET_TPU_TEMP} C")
    print(f"Airflow: {AIRFLOW_CFM} CFM")
    print(f"System Power (Max): {SYSTEM_POWER_MAX} W")
    print("-" * 40)

    # 1. Global Airflow Analysis
    # Convert CFM to kg/s
    # 1 CFM = 0.000471947 m^3/s
    volume_flow_m3s = AIRFLOW_CFM * 0.000471947
    mass_flow_kgs = volume_flow_m3s * AIR_DENSITY

    # Calculate global air temperature rise
    # Q = m * Cp * dT  => dT = Q / (m * Cp)
    global_delta_t = SYSTEM_POWER_MAX / (mass_flow_kgs * CP_AIR)
    exhaust_temp_calculated = AMBIENT_TEMP + global_delta_t

    print(f"Calculated Mass Flow Rate: {mass_flow_kgs:.4f} kg/s")
    print(f"Global Temperature Rise (dT): {global_delta_t:.2f} C")
    print(f"Calculated Average Exhaust Temp: {exhaust_temp_calculated:.2f} C")

    if global_delta_t > 15.0:
        print("WARNING: High global temperature rise. Airflow might be insufficient.")
    else:
        print("Global airflow is sufficient to remove total heat load.")

    print("-" * 40)

    # 2. Localized Thermal Analysis (Worst Case Layer)
    # Using data from AIRFLOW.md for worst-case local ambient (Layer 6 Core)
    # The document states Layer 6 core temp is 48C.
    # This is much higher than our calculated average exhaust, suggesting
    # internal recirculation, hot spots, or conservative design numbers.
    # We will validate against this specific conservative scenario.

    DESIGN_CORE_TEMP_L6 = 48.0 # C
    print(f"Validating against Design Spec Worst-Case Local Ambient (Layer 6): {DESIGN_CORE_TEMP_L6} C")

    # Check Peak Load
    tpu_rise_peak = TPU_POWER_PEAK * HEATSINK_R_TH
    tpu_temp_peak = DESIGN_CORE_TEMP_L6 + tpu_rise_peak

    print(f"TPU Peak Power: {TPU_POWER_PEAK} W")
    print(f"Heatsink Delta T: {tpu_rise_peak} C")
    print(f"Estimated TPU Temp (Peak): {tpu_temp_peak} C")

    if tpu_temp_peak < MAX_TPU_TEMP:
        print("PASS: Peak TPU temperature is within maximum limits.")
    else:
        print("FAIL: Peak TPU temperature exceeds maximum limits!")
        sys.exit(1)

    if tpu_temp_peak < TARGET_TPU_TEMP:
        print("PASS: Peak TPU temperature is within target limits.")
    else:
        print(f"NOTE: Peak TPU temperature exceeds target ({TARGET_TPU_TEMP} C) but is safe.")

    print("-" * 40)

    # Check Typical Load
    tpu_rise_typical = TPU_POWER_TYPICAL * HEATSINK_R_TH
    tpu_temp_typical = DESIGN_CORE_TEMP_L6 + tpu_rise_typical

    print(f"TPU Typical Power: {TPU_POWER_TYPICAL} W")
    print(f"Heatsink Delta T: {tpu_rise_typical} C")
    print(f"Estimated TPU Temp (Typical): {tpu_temp_typical} C")

    if tpu_temp_typical < TARGET_TPU_TEMP:
         print("PASS: Typical TPU temperature is within target limits.")
    else:
         print(f"NOTE: Typical TPU temperature exceeds target ({TARGET_TPU_TEMP} C).")

    print("=" * 40)
    print("THERMAL VALIDATION SUCCESSFUL")

if __name__ == "__main__":
    validate_thermal_design()
