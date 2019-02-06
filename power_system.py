import collections
import numpy as np

Line = collections.namedtuple('Line', ['source', 'destination', 'distributed_impedance', 'shunt_admittance'])

Bus = collections.namedtuple('Bus',
                             ['number', 'power_consumed', 'power_generated', 'voltage', 'generator_impedance_0',
                              'generator_impedance_1', 'generator_impedance_2', 'generator_impedance_neutral'])


class PowerSystem(collections.namedtuple('PowerSystem', ['buses', 'lines'])):
    def admittance_matrix(self):
        matrix = np.zeros((len(self.buses), len(self.buses))) * 1j
        for line in self.lines:
            src = line.source - 1
            dst = line.destination - 1

            y_distributed = 1 / line.distributed_impedance
            y_shunt = line.shunt_admittance

            matrix[src][dst] -= y_distributed
            matrix[dst][src] -= y_distributed
            matrix[src][src] += y_distributed + y_shunt
            matrix[dst][dst] += y_distributed + y_shunt

        return matrix

    def admittance_matrix_0(self):
        matrix = self.admittance_matrix() / 3
        for bus in self.buses:
            # Loads are solidly grounded.
            # Y_L0 = S* / |V|^2
            y = np.conjugate(bus.power_consumed) / np.abs(bus.voltage) ** 2

            # Y_G0 = 1 / (Z_0 + 3Z_n)
            if bus.generator_impedance_0 != 0 and bus.generator_impedance_neutral != np.inf:
                y += 1 / (bus.generator_impedance_0 + 3 * bus.generator_impedance_neutral)

            matrix[bus.number - 1][bus.number - 1] += y

        return matrix

    def admittance_matrix_1(self):
        matrix = self.admittance_matrix()
        for bus in self.buses:
            # Y_L1 = S* / |V|^2
            y = np.conjugate(bus.power_consumed) / np.abs(bus.voltage) ** 2

            # Y_G1 = 1 / Z_1
            if bus.generator_impedance_1 != 0:
                y += 1 / bus.generator_impedance_1

            matrix[bus.number - 1][bus.number - 1] += y

        return matrix

    def admittance_matrix_2(self):
        matrix = self.admittance_matrix()
        for bus in self.buses:
            # Y_L2 = S* / |V|^2
            y = np.conjugate(bus.power_consumed) / np.abs(bus.voltage) ** 2

            # Y_G2 = 1 / Z_2
            if bus.generator_impedance_2 != 0:
                y += 1 / bus.generator_impedance_2

            matrix[bus.number - 1][bus.number - 1] += y

        return matrix
