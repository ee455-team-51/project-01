import dataclasses
import numpy as np


@dataclasses.dataclass
class Line:
    source: int
    destination: int
    distributed_impedance: complex
    shunt_admittance: complex


@dataclasses.dataclass
class Bus:
    number: int
    voltage: complex
    load_admittance: complex
    generator_impedance_0: complex
    generator_impedance_1: complex
    generator_impedance_2: complex
    generator_impedance_neutral: complex

    def has_generator(self):
        return self.generator_impedance_0 != 0 and self.generator_impedance_1 != 0 and self.generator_impedance_2 != 0


class PowerSystem:
    def __init__(self, buses, lines):
        self.buses = buses
        self.lines = lines

    def admittance_matrix(self):
        matrix = np.zeros((len(self.buses), len(self.buses))) * 1j
        for line in self.lines:
            src = line.source - 1
            dst = line.destination - 1

            y_distributed = 1 / line.distributed_impedance
            y_shunt = line.shunt_admittance / 2

            matrix[src][dst] -= y_distributed
            matrix[dst][src] -= y_distributed
            matrix[src][src] += y_distributed + y_shunt
            matrix[dst][dst] += y_distributed + y_shunt

        return matrix

    def admittance_matrix_0(self):
        # Divide line admittances by 3 since Z_L0 = 3Z_L1.
        matrix = self.admittance_matrix() / 3
        for bus in self.buses:
            y = bus.load_admittance
            if bus.generator_impedance_0 != 0 and bus.generator_impedance_neutral != np.inf:
                y += 1 / (bus.generator_impedance_0 + 3 * bus.generator_impedance_neutral)

            matrix[bus.number - 1][bus.number - 1] += y

        return matrix

    def admittance_matrix_1(self):
        matrix = self.admittance_matrix()
        for bus in self.buses:
            y = bus.load_admittance
            y += 1 / bus.generator_impedance_1 if bus.generator_impedance_1 != 0 else 0
            matrix[bus.number - 1][bus.number - 1] += y

        return matrix

    def admittance_matrix_2(self):
        matrix = self.admittance_matrix()
        for bus in self.buses:
            y = bus.load_admittance
            y += 1 / bus.generator_impedance_2 if bus.generator_impedance_2 != 0 else 0
            matrix[bus.number - 1][bus.number - 1] += y

        return matrix
