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