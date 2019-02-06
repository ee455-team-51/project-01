import fault_analyzer

THREE_PHASE_FAULT_TYPE = '3p'
SINGLE_LINE_TO_GROUND_FAULT_TYPE = 'slg'


class FaultAnalyzerBuilder:
    @staticmethod
    def build(system, fault_type, fault_bus, fault_impedance):
        if fault_type == THREE_PHASE_FAULT_TYPE:
            return fault_analyzer.ThreePhaseFaultAnalyzer(system, fault_bus, fault_impedance)
        elif fault_type == SINGLE_LINE_TO_GROUND_FAULT_TYPE:
            return fault_analyzer.SingleLineToGroundFaultAnalyzer(system, fault_bus, fault_impedance)

        return None
