import collections
import numpy

Line = collections.namedtuple('Line', ['source', 'destination', 'distributed_impedance', 'shunt_admittance'])

Bus = collections.namedtuple('Bus',
                             ['number', 'active_power_consumed', 'reactive_power_consumed', 'active_power_generated',
                              'voltage'])


class PowerSystem(collections.namedtuple('PowerSystem', ['buses', 'lines'])):
    def admittance_matrix(self):
        # TODO(kjiwa): Include generator impedances.
        # TODO(kjiwa): Create zero, positive, and negative sequence matrices.
        matrix = numpy.zeros((len(self.buses), len(self.buses))) * 1j
        for line in self.lines:
            src = line.source - 1
            dst = line.destination - 1

            y_distributed = 1 / line.distributed_impedance
            y_shunt = line.shunt_admittance

            matrix[src][dst] -= y_distributed
            matrix[dst][src] -= y_distributed
            matrix[src][src] += y_distributed + y_shunt
            matrix[dst][dst] += y_distributed + y_shunt

        return matrix
