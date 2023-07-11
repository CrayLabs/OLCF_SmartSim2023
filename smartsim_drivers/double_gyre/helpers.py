import pandas as pd
import re

def parse_mom6_out(fname='MOM6_run_exp/MOM6_run/MOM6_run.out'):
    """Retrieve timings from the MOM6 standard output"""
    with open(fname) as f:
        lines = f.readlines()

    read = False
    fields = ['name', 'tmin', 'tmax', 'tavg', 'tstd', 'tfrac', 'grain', 'pemin', 'pemax']
    timings = []

    for line in lines:
        if 'Total runtime' in line:
            read = True
        if 'MPP_STACK' in line:
            read = False
        if read:
            parsed_string = line.replace('\n','')
            parsed_string = re.split('  +', parsed_string)
            timings.append(parsed_string)

    df = pd.DataFrame(timings,columns=fields)
    return df

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



