import numpy as np


class ThreePhaseFaultAnalyzer:
    def __init__(self, system, fault_bus, fault_impedance):
        self._system = system
        self._fault_bus = fault_bus
        self._fault_impedance = fault_impedance
        self._impedance_matrix_1 = np.linalg.inv(system.admittance_matrix_1())

    def zero_sequence_current(self):
        return 0j

    def positive_sequence_current(self):
        n = self._fault_bus - 1
        V_F = self._system.buses[n].voltage
        Z_1 = self._impedance_matrix_1[n][n]
        Z_F = self._fault_impedance
        return V_F / (Z_1 + Z_F)

    def negative_sequence_current(self):
        return 0j

    def phase_a_current(self):
        return self.positive_sequence_current()

    def phase_b_current(self):
        a = np.exp(1j * np.deg2rad(120))
        return a ** 2 * self.positive_sequence_current()

    def phase_c_current(self):
        a = np.exp(1j * np.deg2rad(120))
        return a * self.positive_sequence_current()
