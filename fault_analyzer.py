import numpy as np

A = np.exp(1j * np.deg2rad(120))


class FaultAnalyzer:
    def __init__(self, system, fault_bus, fault_impedance):
        self._system = system
        self._fault_bus = fault_bus
        self._fault_impedance = fault_impedance
        self._impedance_matrix_0 = np.linalg.inv(system.admittance_matrix_0())
        self._impedance_matrix_1 = np.linalg.inv(system.admittance_matrix_1())
        self._impedance_matrix_2 = np.linalg.inv(system.admittance_matrix_2())


class ThreePhaseFaultAnalyzer(FaultAnalyzer):
    def positive_sequence_current(self):
        n = self._fault_bus - 1
        v_f = self._system.buses[n].voltage
        z_1 = self._impedance_matrix_1[n][n]
        z_f = self._fault_impedance
        return v_f / (z_1 + z_f)

    def phase_a_current(self):
        return self.positive_sequence_current()

    def phase_b_current(self):
        return A ** 2 * self.positive_sequence_current()

    def phase_c_current(self):
        return A * self.positive_sequence_current()


class SingleLineToGroundFaultAnalyzer(FaultAnalyzer):
    def zero_sequence_current(self):
        n = self._fault_bus - 1
        v_f = self._system.buses[n].voltage
        z_0 = self._impedance_matrix_0[n][n]
        z_1 = self._impedance_matrix_1[n][n]
        z_2 = self._impedance_matrix_2[n][n]
        return v_f / (z_0 + z_1 + z_2 + 3 * self._fault_impedance)

    def phase_a_current(self):
        return 3 * self.zero_sequence_current()

    def phase_b_current(self):
        return self.phase_a_current()

    def phase_c_current(self):
        return self.phase_a_current()
