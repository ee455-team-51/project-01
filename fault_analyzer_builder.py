import fault_analyzer


class FaultAnalyzerBuilder:
    @staticmethod
    def build(system, fault_type, fault_bus, fault_impedance):
        return fault_analyzer.ThreePhaseFaultAnalyzer(system, fault_bus, fault_impedance)
