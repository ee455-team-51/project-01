import io
import numpy as np
import tabulate

TABULATE_FLOAT_FMT = '.4f'


def phase_components(sequence_0, sequence_1, sequence_2):
    a = np.exp(1j * np.deg2rad(120))
    return np.matmul([[1, 1, 1],
                      [1, a ** 2, a],
                      [1, a, a ** 2]], [sequence_0, sequence_1, sequence_2])


def fault_current_report(fault):
    out = io.StringIO()
    out.write('Fault Bus Report\n')
    out.write('Phase A Current: {:.4f} pu\n'.format(np.abs(fault.phase_current_a())))
    out.write('Phase B Current: {:.4f} pu\n'.format(np.abs(fault.phase_current_b())))
    out.write('Phase C Current: {:.4f} pu\n'.format(np.abs(fault.phase_current_c())))
    try:
        return out.getvalue()
    finally:
        out.close()


def results_bus_report(system, fault, results_bus_number):
    bus_voltages_0 = fault.bus_voltages_0()
    bus_voltages_1 = fault.bus_voltages_1()
    bus_voltages_2 = fault.bus_voltages_2()

    k = results_bus_number - 1
    e_k0 = bus_voltages_0[k]
    e_k1 = bus_voltages_1[k]
    e_k2 = bus_voltages_2[k]
    results_bus = system.buses[k]

    print('Bus {} Report'.format(results_bus_number))
    headers = ['Component', 'Phase A (pu)', 'Phase B (pu)', 'Phase C (pu)']
    table = []

    # Generator currents.
    if results_bus.has_generator():
        i_0 = e_k0 / (results_bus.generator_impedance_0 + 3 * results_bus.generator_impedance_neutral)
        i_1 = e_k1 / results_bus.generator_impedance_1
        i_2 = e_k2 / results_bus.generator_impedance_2
        table.append(['Generator Currents'] + [np.abs(i) for i in phase_components(i_0, i_1, i_2)])

    # Load currents.
    if results_bus.load_admittance != 0:
        i_0 = e_k0 * results_bus.load_admittance
        i_1 = e_k1 * results_bus.load_admittance
        i_2 = e_k2 * results_bus.load_admittance
        table.append(['Load Currents'] + [np.abs(i) for i in phase_components(i_0, i_1, i_2)])

    for line in system.lines:
        if line.source != results_bus_number and line.destination != results_bus_number:
            continue

        other = (line.destination if line.source == results_bus_number else line.source)

        i_0 = (e_k0 - bus_voltages_0[other - 1]) / (3 * line.distributed_impedance) + e_k0 * line.shunt_admittance / 2
        i_1 = (e_k1 - bus_voltages_1[other - 1]) / line.distributed_impedance + e_k1 * line.shunt_admittance / 2
        i_2 = (e_k2 - bus_voltages_2[other - 1]) / line.distributed_impedance + e_k2 * line.shunt_admittance / 2
        line_currents = [np.abs(i) for i in np.abs(phase_components(i_0, i_1, i_2))]
        table.append(['Line {}-{} Currents'.format(line.source, line.destination)] + line_currents)

    return tabulate.tabulate(table, headers=headers, floatfmt=TABULATE_FLOAT_FMT)
