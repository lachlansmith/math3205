
from binpacking.model import Bin


class NonOptimalSolutionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TimeoutException(Exception):
    def __init__(self):
        super().__init__('Time limit reached')


class IncompatibleBinException(Exception):
    def __init__(self, bin: Bin):
        self.bin = bin
        super().__init__(f'Indices {bin.indices()} are incompatible with the bin dimensions {(bin.width, bin.height)}')
