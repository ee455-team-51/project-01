import argparse
import power_system_builder

DEFAULT_INPUT_WORKBOOK = 'data/data.xlsx'
DEFAULT_BUS_DATA_WORKSHEET_NAME = 'BusData'
DEFAULT_LINE_DATA_WORKSHEET_NAME = 'LineData'
DEFAULT_GENERATOR_NEUTRAL_REACTANCE = 0


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('input')
    group.add_argument('--input_workbook', default=DEFAULT_INPUT_WORKBOOK,
                       help='An Excel workbook containing bus and line data.')
    group.add_argument('--bus_data_worksheet', default=DEFAULT_BUS_DATA_WORKSHEET_NAME,
                       help='The name of the worksheet containing bus data.')
    group.add_argument('--line_data_worksheet', default=DEFAULT_LINE_DATA_WORKSHEET_NAME,
                       help='The name of the worksheet containing line data.')
    group.add_argument('--generator_neutral_reactance', type=float, default=DEFAULT_GENERATOR_NEUTRAL_REACTANCE,
                       help='The per unit neutral reactance of the generators.')

    group = parser.add_argument_group('fault')
    group.add_argument('--fault_type', required=True, choices=['3p', 'slg', 'll', 'dlg'], help='The fault type.')
    group.add_argument('--fault_bus', required=True, type=int, help='The bus where the fault occurred.')
    group.add_argument('--fault_impedance', required=True, type=float, help='The per unit fault impedance.')
    group.add_argument('--results_bus', required=True, type=int)
    return parser.parse_args()


def main():
    args = parse_arguments()
    generator_neutral_impedance = 1j * args.generator_neutral_reactance

    builder = power_system_builder.ExcelPowerSystemBuilder(
        args.input_workbook, args.bus_data_worksheet, args.line_data_worksheet, generator_neutral_impedance)
    system = builder.build_system()

    print(system.admittance_matrix_0())
    print(system.admittance_matrix_1())
    print(system.admittance_matrix_2())


if __name__ == '__main__':
    main()
