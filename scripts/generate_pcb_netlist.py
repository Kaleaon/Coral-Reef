#!/usr/bin/env python3
"""
Coral-Reef PCB Netlist Generator

This script generates a schematic netlist for the Coral-Reef 16-TPU Carrier Board.
It programmatically defines the connectivity between the PCIe switch, M.2 slots,
power management system, and microcontroller.

Updates:
- Added 4x High-Performance CPU Modules (SOMs) per layer.
- Connected CPUs to PCIe Switch (x4 lanes each).

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
                pass # Already connected
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

        # PCIe Packet Switch (PEX8748 - 48 Lane / 12 Port)
        self.pcie_switch = self.add_component("U1", "PEX8748-BGA")

        # Define Switch Ports
        # Port 0-3: Reserved for CPUs (x4 each)
        # Port 4-19: Reserved for TPUs (x1 each)

        # CPU Ports (x4 lanes each)
        for cpu_idx in range(4):
            for lane in range(4):
                self.pcie_switch.add_pin(f"P{cpu_idx}_TX_P{lane}", f"SW_CPU{cpu_idx}_TX_P[{lane}]")
                self.pcie_switch.add_pin(f"P{cpu_idx}_TX_N{lane}", f"SW_CPU{cpu_idx}_TX_N[{lane}]")
                self.pcie_switch.add_pin(f"P{cpu_idx}_RX_P{lane}", f"SW_CPU{cpu_idx}_RX_P[{lane}]")
                self.pcie_switch.add_pin(f"P{cpu_idx}_RX_N{lane}", f"SW_CPU{cpu_idx}_RX_N[{lane}]")

        # TPU Ports (x1 lane each)
        for tpu_idx in range(16):
            port_num = 4 + tpu_idx # Start after CPU ports
            self.pcie_switch.add_pin(f"DS{tpu_idx}_TX_P", f"SW_TPU{tpu_idx}_TX_P")
            self.pcie_switch.add_pin(f"DS{tpu_idx}_TX_N", f"SW_TPU{tpu_idx}_TX_N")
            self.pcie_switch.add_pin(f"DS{tpu_idx}_RX_P", f"SW_TPU{tpu_idx}_RX_P")
            self.pcie_switch.add_pin(f"DS{tpu_idx}_RX_N", f"SW_TPU{tpu_idx}_RX_N")

        # 4x CPU Modules (System-on-Module)
        self.cpu_modules = []
        for i in range(4):
            cpu = self.add_component(f"SOM{i+1}", "RK3588-Compute-Module")
            # Power
            cpu.add_pin("VIN", "VIN_5V")
            cpu.add_pin("GND", "GND")
            # PCIe x4 Interface
            for lane in range(4):
                cpu.add_pin(f"PCIE_TX_P{lane}", f"TX_P{lane}")
                cpu.add_pin(f"PCIE_TX_N{lane}", f"TX_N{lane}")
                cpu.add_pin(f"PCIE_RX_P{lane}", f"RX_P{lane}")
                cpu.add_pin(f"PCIE_RX_N{lane}", f"RX_N{lane}")
            self.cpu_modules.append(cpu)

        # 16x M.2 Connectors
        self.m2_slots = []
        for i in range(16):
            slot = self.add_component(f"J{i+1}", "M.2-KeyE-Socket")
            slot.add_pin("1", "GND")
            slot.add_pin("2", "3.3V")
            slot.add_pin("35", "PETp0") # Transmit + (Device TX)
            slot.add_pin("37", "PETn0") # Transmit -
            slot.add_pin("41", "PERp0") # Receive + (Device RX)
            slot.add_pin("43", "PERn0") # Receive -
            self.m2_slots.append(slot)

        # Power Management
        # 12V -> 3.3V (TPUs)
        self.pmic_3v3 = self.add_component("U2", "TPS54xxx-Buck-3V3")
        self.pmic_3v3.add_pin("IN", "VIN_12V")
        self.pmic_3v3.add_pin("OUT", "VOUT_3V3")
        self.pmic_3v3.add_pin("GND", "GND")

        # 12V -> 5V (CPUs)
        self.pmic_5v = self.add_component("U4", "TPS54xxx-Buck-5V")
        self.pmic_5v.add_pin("IN", "VIN_12V")
        self.pmic_5v.add_pin("OUT", "VOUT_5V")
        self.pmic_5v.add_pin("GND", "GND")

        # Management MCU (ESP32)
        self.mcu = self.add_component("U3", "ESP32-S3-WROOM")
        self.mcu.add_pin("1", "3.3V")
        self.mcu.add_pin("2", "GND")
        self.mcu.add_pin("3", "IO0_I2C_SDA")
        self.mcu.add_pin("4", "IO1_I2C_SCL")


        # 2. Connect Components

        # Power Rails
        self.connect_pins("GND",
            [(self.pmic_3v3, "GND"), (self.pmic_5v, "GND"), (self.mcu, "2")] +
            [(slot, "1") for slot in self.m2_slots] +
            [(cpu, "GND") for cpu in self.cpu_modules]
        )
        self.connect_pins("3.3V",
            [(self.pmic_3v3, "OUT"), (self.mcu, "1")] +
            [(slot, "2") for slot in self.m2_slots]
        )
        self.connect_pins("5V_CPU",
            [(self.pmic_5v, "OUT")] +
            [(cpu, "VIN") for cpu in self.cpu_modules]
        )
        self.connect_pins("12V_MAIN", [(self.pmic_3v3, "IN"), (self.pmic_5v, "IN")])

        # PCIe: CPU Modules <-> Switch (x4 Lanes each)
        for i in range(4): # 4 CPUs
            cpu = self.cpu_modules[i]
            for lane in range(4):
                # CPU TX -> Switch RX
                self.connect_pins(f"PCIE_CPU{i}_LANE{lane}_TX", [
                    (cpu, f"PCIE_TX_P{lane}"),
                    (self.pcie_switch, f"P{i}_RX_P{lane}")
                ])
                self.connect_pins(f"PCIE_CPU{i}_LANE{lane}_TX_N", [
                    (cpu, f"PCIE_TX_N{lane}"),
                    (self.pcie_switch, f"P{i}_RX_N{lane}")
                ])
                # Switch TX -> CPU RX
                self.connect_pins(f"PCIE_CPU{i}_LANE{lane}_RX", [
                    (self.pcie_switch, f"P{i}_TX_P{lane}"),
                    (cpu, f"PCIE_RX_P{lane}")
                ])
                self.connect_pins(f"PCIE_CPU{i}_LANE{lane}_RX_N", [
                    (self.pcie_switch, f"P{i}_TX_N{lane}"),
                    (cpu, f"PCIE_RX_N{lane}")
                ])

        # PCIe: Switch <-> TPUs (x1 Lane each)
        for i in range(16):
            slot = self.m2_slots[i]
            # Switch TX -> TPU RX (PERp0)
            self.connect_pins(f"PCIE_TPU{i}_RX", [
                (self.pcie_switch, f"DS{i}_TX_P"),
                (slot, "41")
            ])
            self.connect_pins(f"PCIE_TPU{i}_RX_N", [
                (self.pcie_switch, f"DS{i}_TX_N"),
                (slot, "43")
            ])
            # TPU TX (PETp0) -> Switch RX
            self.connect_pins(f"PCIE_TPU{i}_TX", [
                (slot, "35"),
                (self.pcie_switch, f"DS{i}_RX_P")
            ])
            self.connect_pins(f"PCIE_TPU{i}_TX_N", [
                (slot, "37"),
                (self.pcie_switch, f"DS{i}_RX_N")
            ])

        # Management I2C (MCU to Switch)
        self.pcie_switch.add_pin("SMB_CLK", "SMBus_CLK")
        self.pcie_switch.add_pin("SMB_DAT", "SMBus_DAT")

        self.connect_pins("I2C_SCL", [(self.mcu, "4"), (self.pcie_switch, "SMB_CLK")])
        self.connect_pins("I2C_SDA", [(self.mcu, "3"), (self.pcie_switch, "SMB_DAT")])

        print(f"Design completed: {len(self.components)} components, {len(self.nets)} nets.")

    def export_netlist(self, filepath: str):
        print(f"Exporting netlist to {filepath}...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Net Name', 'Component Ref', 'Pin Number', 'Pin Name', 'Part Type'])
            for net_name in sorted(self.nets.keys()):
                net = self.nets[net_name]
                for comp, pin in net.connections:
                    writer.writerow([net.name, comp.ref_des, pin.number, pin.name, comp.part_type])
        print("Export complete.")

if __name__ == "__main__":
    design = TPUCarrierBoardDesign()
    design.generate()
    output_path = "designs/column-tpu-tower/pcb/netlist.csv"
    if not os.path.exists("designs") and os.path.exists("../designs"):
        output_path = "../designs/column-tpu-tower/pcb/netlist.csv"
    design.export_netlist(output_path)
