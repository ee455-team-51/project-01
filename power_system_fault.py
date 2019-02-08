import numpy as np

A = np.exp(1j * np.deg2rad(120))
THREE_PHASE_FAULT_TYPE = '3p'
SINGLE_LINE_TO_GROUND_FAULT_TYPE = 'slg'


class PowerSystemFaultBuilder:
    @staticmethod
    def build(system, fault_type, fault_bus, fault_impedance):
        if fault_type == THREE_PHASE_FAULT_TYPE:
            return ThreePhaseFault(system, fault_bus, fault_impedance)
        elif fault_type == SINGLE_LINE_TO_GROUND_FAULT_TYPE:
            return SingleLineToGroundFault(system, fault_bus, fault_impedance)

        return None


class Fault:
    def __init__(self, system, fault_bus, fault_impedance):
        z_0 = np.linalg.inv(system.admittance_matrix_0())
        z_1 = np.linalg.inv(system.admittance_matrix_1())
        z_2 = np.linalg.inv(system.admittance_matrix_2())
        self._voltage = system.buses[fault_bus - 1].voltage
        self._impedance_0 = z_0[fault_bus - 1][fault_bus - 1]
        self._impedance_1 = z_1[fault_bus - 1][fault_bus - 1]
        self._impedance_2 = z_2[fault_bus - 1][fault_bus - 1]
        self._fault_impedance = fault_impedance


class ThreePhaseFault(Fault):
    def sequence_current_0(self):
        return 0j

    def sequence_current_1(self):
        return self._voltage / (self._impedance_1 + self._fault_impedance)

    def sequence_current_2(self):
        return 0j

    def phase_current_a(self):
        return self.sequence_current_1()

    def phase_current_b(self):
        return A ** 2 * self.sequence_current_1()

    def phase_current_c(self):
        return A * self.sequence_current_1()


class SingleLineToGroundFault(Fault):
    def sequence_current_0(self):
        denominator = self._impedance_0 + self._impedance_1 + self._impedance_2 + 3 * self._fault_impedance
        return self._voltage / denominator

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
