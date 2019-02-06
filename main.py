import argparse
import power_system_builder

DEFAULT_INPUT_WORKBOOK = 'data/CHW1Data.xlsx'
DEFAULT_BUS_DATA_WORKSHEET_NAME = 'BusData'
DEFAULT_LINE_DATA_WORKSHEET_NAME = 'LineData'


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('input')
    group.add_argument('--input_workbook', default=DEFAULT_INPUT_WORKBOOK,
                       help='An Excel workbook containing bus and line data.')
    group.add_argument('--bus_data_worksheet', default=DEFAULT_BUS_DATA_WORKSHEET_NAME,
                       help='The name of the worksheet containing bus data.')
    group.add_argument('--line_data_worksheet', default=DEFAULT_LINE_DATA_WORKSHEET_NAME,
                       help='The name of the worksheet containing line data.')

    group = parser.add_argument_group('fault')
    group.add_argument('--fault_type', required=True, choices=['3p', 'slg', 'll', 'dlg'], help='The fault type.')
    group.add_argument('--fault_bus', required=True, type=int, help='The bus where the fault occurred.')
    group.add_argument('--fault_impedance', required=True, type=float, help='The per unit fault impedance.')
    group.add_argument('--results_bus', required=True, type=int)
    return parser.parse_args()


def main():
    args = parse_arguments()

    builder = power_system_builder.ExcelPowerSystemBuilder(
        args.input_workbook, args.bus_data_worksheet, args.line_data_worksheet)
    system = builder.build_system()
    print(system.admittance_matrix_0())


if __name__ == '__main__':
    main()
