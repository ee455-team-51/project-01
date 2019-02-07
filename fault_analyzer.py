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
    def sequence_current_0(self):
        return 0j

    def sequence_current_1(self):
        n = self._fault_bus - 1
        v_f = self._system.buses[n].voltage
        z_1 = self._impedance_matrix_1[n][n]
        z_f = self._fault_impedance
        return v_f / (z_1 + z_f)

    def sequence_current_2(self):
        return 0j

    def phase_current_a(self):
        return self.sequence_current_1()

    def phase_current_b(self):
        return A ** 2 * self.sequence_current_1()

    def phase_current_c(self):
        return A * self.sequence_current_1()


class SingleLineToGroundFaultAnalyzer(FaultAnalyzer):
    def sequence_current_0(self):
        n = self._fault_bus - 1
        v_f = self._system.buses[n].voltage
        z_0 = self._impedance_matrix_0[n][n]
        z_1 = self._impedance_matrix_1[n][n]
        z_2 = self._impedance_matrix_2[n][n]
        return v_f / (z_0 + z_1 + z_2 + 3 * self._fault_impedance)

    def sequence_current_1(self):
        return 0j

    def sequence_current_2(self):
        return 0j

    def phase_current_a(self):
        return 3 * self.sequence_current_0()

    def phase_current_b(self):
        return self.phase_current_a()

    def phase_current_c(self):
        return self.phase_current_a()
