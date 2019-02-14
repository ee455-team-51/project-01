import numpy as np
import power_system_builder
import unittest


class TestPowerSystem(unittest.TestCase):
    def test_admittance_matrix_0(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()

        actual = ps.admittance_matrix_0()
        expected = [[-10j, 6.67j, 0, 3.33j, 0, 0],
                    [6.67j, -210j, 0, 0, 3.33j, 0],
                    [0, 0, -205.71j, 2.38j, 0, 3.33j],
                    [3.33j, 0, 2.38j, 0.96 - 12.76j, 6.67j, 0],
                    [0, 3.33j, 0, 6.67j, 0.48 - 16.96j, 6.67j],
                    [0, 0, 3.33j, 0, 6.67j, 1.07 - 10.39j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)

    def test_admittance_matrix_1(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()

        actual = ps.admittance_matrix_1()
        expected = [[-80j, 20j, 0, 10j, 0, 0],
                    [20j, -80j, 0, 0, 10j, 0],
                    [0, 0, -67.14j, 7.14j, 0, 10j],
                    [10j, 0, 7.14j, 0.96 - 37.53j, 20j, 0],
                    [0, 10j, 0, 20j, 0.48 - 50.29j, 20j],
                    [0, 0, 10j, 0, 20j, 1.07 - 30.39j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)

    def test_admittance_matrix_2(self):
        filename = 'data/data.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()

        actual = ps.admittance_matrix_1()
        expected = [[-80j, 20j, 0, 10j, 0, 0],
                    [20j, -80j, 0, 0, 10j, 0],
                    [0, 0, -67.14j, 7.14j, 0, 10j],
                    [10j, 0, 7.14j, 0.96 - 37.53j, 20j, 0],
                    [0, 10j, 0, 20j, 0.48 - 50.29j, 20j],
                    [0, 0, 10j, 0, 20j, 1.07 - 30.39j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)

    def test_admittance_matrix_0_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()

        actual = ps.admittance_matrix_0()
        expected = [[-3.33j, 1.11j, 1.11j, 1.11j],
                    [1.11j, -22.22j, 1.11j, 0],
                    [1.11j, 1.11j, -2.22j, 0],
                    [1.11j, 0, 0, -1.11j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)

    def test_admittance_matrix_1_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0.01j)
        ps = builder.build_system()

        actual = ps.admittance_matrix_1()
        expected = [[-16.67j, 3.33j, 3.33j, 3.33j],
                    [3.33j, -13.33j, 3.33j, 0],
                    [3.33j, 3.33j, -6.67j, 0],
                    [3.33j, 0, 0, -3.33j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)

    def test_admittance_matrix_2_hw04p4(self):
        filename = 'data/sample-hw04p4.xlsx'
        builder = power_system_builder.ExcelPowerSystemBuilder(filename, 'BusData', 'LineData', 0)
        ps = builder.build_system()

        actual = ps.admittance_matrix_2()
        expected = [[-21.11j, 3.33j, 3.33j, 3.33j],
                    [3.33j, -17.78j, 3.33j, 0],
                    [3.33j, 3.33j, -6.67j, 0],
                    [3.33j, 0, 0, -3.33j]]

        np.testing.assert_array_almost_equal(actual, expected, 2)
