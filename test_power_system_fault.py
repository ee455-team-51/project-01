import numpy as np
import power_system_fault
import power_system_builder
import unittest


class TestPowerSystem(unittest.TestCase):
    def test_3p_fault_currents(self):
        # Compare the three phase fault currents to results from PowerWorld.
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, '3p', 1, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 72.95156, 4)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 72.952, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 72.950, 2)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 72.950, 2)

    def test_slg_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'slg', 2, 0.1)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 10.42977, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 10.430, 3)
        np.testing.assert_equal(np.abs(fault.phase_current_b()), 0)
        np.testing.assert_equal(np.abs(fault.phase_current_c()), 0)

    def test_ll_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'll', 4, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 20.53347, 2)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 20.533, 2)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 20.533, 2)

    def test_dlg_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'dlg', 5, 0.1)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 4.48681, 0)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 22.275, 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 18.352, 1)
