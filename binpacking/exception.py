
from binpacking.model import Bin


class NonOptimalSolutionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class IncompatibleBinException(Exception):
    def __init__(self, bin: Bin):
        super().__init__(f'Indices {bin.indices()} are incompatible with the bin dimensions {(bin.width, bin.height)}')
