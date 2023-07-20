import re


def allowed_cpus(n_cpus, only_physical=True, reversed=False):
    """Return a list of the first n_cpus CPUs that are available on Frontier"""

    _num_physical = 64
    _num_logical = 128
    # Following includes both physical and logical core
    _reserved_ids = [0, 64, 8, 72, 16, 80, 24, 88, 32, 96, 40, 104, 48, 112, 56, 120]

    num_cpus = _num_physical if only_physical else _num_logical
    allowed_list = [id for id in range(num_cpus) if id not in _reserved_ids]
    if reversed:
        allowed_list.reverse()

    return allowed_list[:n_cpus]



