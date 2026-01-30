#!/usr/bin/env python3
"""
Coral-Reef PCB Netlist Generator

This script generates a schematic netlist for the Coral-Reef 16-TPU Carrier Board.
It programmatically defines the connectivity between the PCIe switch, M.2 slots,
power management system, and microcontroller.

Output:
    designs/column-tpu-tower/pcb/netlist.csv
"""

import csv
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# --- Data Structures ---

@dataclass
class Pin:
    number: str
    name: str
    net: Optional['Net'] = None

    def __repr__(self):
        return f"{self.number}({self.name})"

@dataclass
class Component:
    ref_des: str  # Reference Designator (e.g., U1, J1)
    part_type: str # Part Type/Value (e.g., PEX8748, M.2-KeyE)
    pins: Dict[str, Pin] = field(default_factory=dict)

    def add_pin(self, number: str, name: str):
        self.pins[number] = Pin(number, name)

    def get_pin(self, number: str) -> Pin:
        return self.pins.get(str(number))

@dataclass
class Net:
    name: str
    connections: List[tuple[Component, Pin]] = field(default_factory=list)

    def connect(self, component: Component, pin_number: str):
        pin = component.get_pin(pin_number)
        if pin:
            if pin.net:
                # Disconnect from old net if needed, or warn
                pass
            pin.net = self
            self.connections.append((component, pin))
        else:
            print(f"Warning: Pin {pin_number} not found on {component.ref_des}")

# --- Schematic Generator ---

class TPUCarrierBoardDesign:
    def __init__(self):
        self.components: List[Component] = []
        self.nets: Dict[str, Net] = {}

    def add_component(self, ref_des: str, part_type: str) -> Component:
        comp = Component(ref_des, part_type)
        self.components.append(comp)
        return comp

    def get_net(self, name: str) -> Net:
        if name not in self.nets:
            self.nets[name] = Net(name)
        return self.nets[name]

    def connect_pins(self, net_name: str, connections: List[tuple[Component, str]]):
        net = self.get_net(net_name)
        for comp, pin_num in connections:
            net.connect(comp, pin_num)

    def generate(self):
        print("Generating Coral-Reef Carrier Board Design...")

        # 1. Instantiate Main Components

        # PCIe Packet Switch (PEX8748 - simplified pinout for example)
        # Assuming a BGA package, using logical names here
        self.pcie_switch = self.add_component("U1", "PEX8748-BGA")
        # Define Upstream Port (x16)
        for i in range(16):
            self.pcie_switch.add_pin(f"US_TX_P{i}", f"UP_TX_P[{i}]")
            self.pcie_switch.add_pin(f"US_TX_N{i}", f"UP_TX_N[{i}]")
            self.pcie_switch.add_pin(f"US_RX_P{i}", f"UP_RX_P[{i}]")
            self.pcie_switch.add_pin(f"US_RX_N{i}", f"UP_RX_N[{i}]")

        # Define 16 Downstream Ports (x1 each) for TPUs
        for port in range(16):
            self.pcie_switch.add_pin(f"DS{port}_TX_P", f"DN_TX_P[{port}]")
            self.pcie_switch.add_pin(f"DS{port}_TX_N", f"DN_TX_N[{port}]")
            self.pcie_switch.add_pin(f"DS{port}_RX_P", f"DN_RX_P[{port}]")
            self.pcie_switch.add_pin(f"DS{port}_RX_N", f"DN_RX_N[{port}]")

        # 16 M.2 Connectors
        self.m2_slots = []
        for i in range(16):
            # M.2 Key E Pinout (Simplified subset for PCIe)
            # Pins: 1=GND, 2=3.3V, 3=USB_D+, 5=USB_D-, ...
            # PCIe Lane 0: TX on 35/37, RX on 41/43 (Example)
            slot = self.add_component(f"J{i+1}", "M.2-KeyE-Socket")
            slot.add_pin("1", "GND")
            slot.add_pin("2", "3.3V")
            slot.add_pin("3", "USB_D_P")
            slot.add_pin("5", "USB_D_N")
            slot.add_pin("35", "PETp0") # Transmit +
            slot.add_pin("37", "PETn0") # Transmit -
            slot.add_pin("41", "PERp0") # Receive +
            slot.add_pin("43", "PERn0") # Receive -
            slot.add_pin("50", "PERST#")
            slot.add_pin("52", "CLKREQ#")
            slot.add_pin("54", "PEWAKE#")
            self.m2_slots.append(slot)

        # Power Management (Simplified)
        self.pmic_3v3 = self.add_component("U2", "TPS54xxx-Buck") # 12V to 3.3V
        self.pmic_3v3.add_pin("IN", "VIN")
        self.pmic_3v3.add_pin("OUT", "VOUT")
        self.pmic_3v3.add_pin("GND", "GND")

        # Management MCU (ESP32)
        self.mcu = self.add_component("U3", "ESP32-S3-WROOM")
        self.mcu.add_pin("1", "3.3V")
        self.mcu.add_pin("2", "GND")
        self.mcu.add_pin("3", "IO0_I2C_SDA")
        self.mcu.add_pin("4", "IO1_I2C_SCL")

        # 2. Connect Components (The Wiring)

        # Power Rails
        self.connect_pins("GND",
            [(self.pmic_3v3, "GND"), (self.mcu, "2")] +
            [(slot, "1") for slot in self.m2_slots]
        )
        self.connect_pins("3.3V",
            [(self.pmic_3v3, "OUT"), (self.mcu, "1")] +
            [(slot, "2") for slot in self.m2_slots]
        )
        self.connect_pins("12V_MAIN", [(self.pmic_3v3, "IN")])

        # PCIe Connections (Switch <-> M.2 Slots)
        for i in range(16):
            slot = self.m2_slots[i]
            # TX from Switch goes to RX on Slot
            self.connect_pins(f"PCIE_LANE{i}_TX_P", [
                (self.pcie_switch, f"DS{i}_TX_P"),
                (slot, "41") # PERp0 (RX on device side)
            ])
            self.connect_pins(f"PCIE_LANE{i}_TX_N", [
                (self.pcie_switch, f"DS{i}_TX_N"),
                (slot, "43") # PERn0
            ])
            # RX on Switch comes from TX on Slot
            self.connect_pins(f"PCIE_LANE{i}_RX_P", [
                (self.pcie_switch, f"DS{i}_RX_P"),
                (slot, "35") # PETp0 (TX on device side)
            ])
            self.connect_pins(f"PCIE_LANE{i}_RX_N", [
                (self.pcie_switch, f"DS{i}_RX_N"),
                (slot, "37") # PETn0
            ])

        # Management Bus (I2C)
        # Connecting MCU to... well, let's say the Switch has I2C management
        self.pcie_switch.add_pin("SMB_CLK", "SMBus_CLK")
        self.pcie_switch.add_pin("SMB_DAT", "SMBus_DAT")

        self.connect_pins("I2C_SCL", [
            (self.mcu, "4"),
            (self.pcie_switch, "SMB_CLK")
        ])
        self.connect_pins("I2C_SDA", [
            (self.mcu, "3"),
            (self.pcie_switch, "SMB_DAT")
        ])

        print(f"Design completed: {len(self.components)} components, {len(self.nets)} nets.")

    def export_netlist(self, filepath: str):
        print(f"Exporting netlist to {filepath}...")

        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Net Name', 'Component Ref', 'Pin Number', 'Pin Name', 'Part Type'])

            # Sort nets for consistent output
            for net_name in sorted(self.nets.keys()):
                net = self.nets[net_name]
                for comp, pin in net.connections:
                    writer.writerow([net.name, comp.ref_des, pin.number, pin.name, comp.part_type])

        print("Export complete.")

if __name__ == "__main__":
    design = TPUCarrierBoardDesign()
    design.generate()

    output_path = "designs/column-tpu-tower/pcb/netlist.csv"
    # Adjust path if running from script directory or root
    if not os.path.exists("designs") and os.path.exists("../designs"):
        output_path = "../designs/column-tpu-tower/pcb/netlist.csv"

    design.export_netlist(output_path)
