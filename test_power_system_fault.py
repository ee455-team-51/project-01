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

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 72.95155, 4)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 72.952, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 72.950, 2)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 72.950, 2)

    def test_slg_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'slg', 2, 0.1)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 10.42942, 5)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 10.429, 3)
        np.testing.assert_equal(np.abs(fault.phase_current_b()), 0)
        np.testing.assert_equal(np.abs(fault.phase_current_c()), 0)

    def test_ll_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'll', 4, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 20.53350, 2)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 20.533, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 20.533, 3)

    def test_dlg_fault_currents(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'dlg', 5, 0.1)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 4.36025, 2)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 22.266, 1)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 18.351, 1)

    def test_3p_fault_currents_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, '3p', 3, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 4.267, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 4.267, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 4.267, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 4.267, 3)

    def test_slg_fault_currents_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'slg', 3, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 2.692, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_a()), 2.692, 3)
        np.testing.assert_equal(np.abs(fault.phase_current_b()), 0)
        np.testing.assert_equal(np.abs(fault.phase_current_c()), 0)

    def test_ll_fault_currents_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'll', 3, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 3.959, 3)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 3.959, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 3.959, 3)

    def test_dlg_fault_currents_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, 'dlg', 3, 0)

        np.testing.assert_almost_equal(np.abs(fault.fault_current()), 1.772, 3)
        np.testing.assert_equal(np.abs(fault.phase_current_a()), 0)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_b()), 4.021, 3)
        np.testing.assert_almost_equal(np.abs(fault.phase_current_c()), 4.021, 3)

    def test_3p_fault_voltages_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()
        fault = power_system_fault.FaultBuilder.build(ps, '3p', 3, 0)

        e_0 = fault.bus_voltages_0()
        e_1 = fault.bus_voltages_1()
        e_2 = fault.bus_voltages_2()

        a = np.exp(1j * np.deg2rad(120))
        v_0 = np.add(e_0, np.add(e_1, e_2))
        v_1 = e_0 + np.dot(a ** 2, e_1) + np.dot(a, e_2)
        v_2 = e_0 + np.dot(a, e_1) + np.dot(a ** 2, e_2)

        np.testing.assert_array_almost_equal(np.abs(v_0), [0.66667, 0.66666, 0, 0.66667], 1)
        np.testing.assert_array_almost_equal(np.abs(v_1), [0.66667, 0.66666, 0, 0.66667], 1)
        np.testing.assert_array_almost_equal(np.abs(v_2), [0.66667, 0.66666, 0, 0.66667], 1)
