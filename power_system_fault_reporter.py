import numpy as np
import tabulate

TABULATE_FLOAT_FMT = '.4f'


def phase_components(sequence_0, sequence_1, sequence_2):
    a = np.exp(1j * np.deg2rad(120))
    return [np.abs(i) for i in np.matmul([[1, 1, 1],
                                          [1, a ** 2, a],
                                          [1, a, a ** 2]], [sequence_0, sequence_1, sequence_2])]


def report(system, fault, results_bus_number):
    bus_voltages_0 = fault.bus_voltages_0()
    bus_voltages_1 = fault.bus_voltages_1()
    bus_voltages_2 = fault.bus_voltages_2()

    k = results_bus_number - 1
    e_k0 = bus_voltages_0[k]
    e_k1 = bus_voltages_1[k]
    e_k2 = bus_voltages_2[k]
    results_bus = system.buses[k]

    # Generator currents are the sum of currents leaving the bus.
    i_gen0 = 0j
    i_gen1 = 0j
    i_gen2 = 0j

    headers = ['Bus {} {} Fault'.format(fault.fault_bus_number, fault.fault_type), 'I_a (pu)', 'I_b (pu)', 'I_c (pu)']
    table = [['Bus {} Fault'.format(fault.fault_bus_number),
              np.abs(fault.phase_current_a()), np.abs(fault.phase_current_b()), np.abs(fault.phase_current_c())]]

    # Line currents.
    for line in system.lines:
        if line.source != results_bus_number and line.destination != results_bus_number:
            continue

        other = (line.destination if line.source == results_bus_number else line.source)

        i_line0 = ((e_k0 - bus_voltages_0[other - 1]) / (3 * line.distributed_impedance)
                   + e_k0 * line.shunt_admittance / 2)
        i_line1 = (e_k1 - bus_voltages_1[other - 1]) / line.distributed_impedance + e_k1 * line.shunt_admittance / 2
        i_line2 = (e_k2 - bus_voltages_2[other - 1]) / line.distributed_impedance + e_k2 * line.shunt_admittance / 2
        i_gen0 += i_line0
        i_gen1 += i_line1
        i_gen2 += i_line2
        table.append(['Line {}-{}'.format(line.source, line.destination)] + phase_components(i_line0, i_line1, i_line2))

    # Load currents.
    if results_bus.has_load():
        i_load0 = e_k0 * results_bus.load_admittance
        i_load1 = e_k1 * results_bus.load_admittance
        i_load2 = e_k2 * results_bus.load_admittance
        i_gen0 += i_load0
        i_gen1 += i_load1
        i_gen2 += i_load2
        table.append(['Bus {} Load'.format(results_bus_number)] + phase_components(i_load0, i_load1, i_load2))

    # If the generator is at the fault bus, the fault current is also included.
    if fault.fault_bus_number == results_bus_number:
        i_gen0 += fault.sequence_current_0()
        i_gen1 += fault.sequence_current_1()
        i_gen2 += fault.sequence_current_2()

    if results_bus.has_generator():
        table.append(['Bus {} Generator'.format(results_bus_number)] + phase_components(i_gen0, i_gen1, i_gen2))

    return tabulate.tabulate(table, headers=headers, floatfmt=TABULATE_FLOAT_FMT)
