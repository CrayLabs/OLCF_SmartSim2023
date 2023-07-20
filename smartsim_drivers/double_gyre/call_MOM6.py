
import argparse
import glob
import itertools
import logging
import shutil
import time

import pandas as pd
from smartsim import Experiment

from helpers import parse_mom6_out, allowed_cpus

_DISPLAY_NAMES = ['Total runtime','(CNN total inference)']
NUM_NODES = 1
ML_INPUTS = "./ml_inputs"

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO,
)

def main():
    timing_dfs = []

    db_cpus = [8]
    mom6_cpus = [8]
    refines = [3]  # Refinement relative to 1/4-degree, e.g. '3' refers to a 1/12-degree model

    combinations = itertools.product(db_cpus, mom6_cpus, refines)

    for db_cpu, mom6_cpu, refine in combinations:
        logging.info(f'Starting: db_cpu={db_cpu}\tmom6_cpu={mom6_cpu}')
        start_time = time.time()

        exp_name = f"MOM6_run_exp_{db_cpu}_{mom6_cpu}_{refine}"
        exp = Experiment(exp_name, launcher='slurm')
        # create and start an instance of the Orchestrator database
        # create and start an MOM6 experiment
        srun = exp.create_run_settings(
                exe='/lus/scratch/smartsim/demos/MOM6_frontier/MOM6-examples/build/ocean_only/MOM6',
                run_command='srun'
                )
        srun.set_nodes(NUM_NODES)
        srun.set_tasks(mom6_cpu*NUM_NODES)
        srun.set_tasks_per_node(mom6_cpu)

        # start MOM6
        model = exp.create_model("MOM6_run", srun)
        model.params = {
            'nx':44*refine,
            'ny':40*refine,
            'daymax':5.0,
            'use_hor_visc_python':'True'
            }

        model.colocate_db_uds(
                db_cpus=db_cpu,
                unix_socket='/tmp/redis.socket'
                )
        model.add_ml_model(
                f'ml_0',
                'TORCH',
                model_path=f'{ML_INPUTS}/CNN_GPU_2X21X21X2.pt',
                device=f'GPU:0',
                batch_size=mom6_cpu,
                min_batch_size=mom6_cpu
                )
        model.add_script(
                'pys',
                script_path=f'{ML_INPUTS}/testNN_trace.txt'
                )

        files = glob.glob('./basecase/')
        files.append('./basecase/INPUT')
        files.append('./basecase/RESTART')
        model.attach_generator_files(to_copy=files, to_configure='./MOM_override')
        exp.generate(model, overwrite=True)

        exp.start(model, summary=False, block=True)

        end_time = time.time()

        tmp_df = parse_mom6_out(f'{exp_name}/MOM6_run/MOM6_run.out')
        tmp_df['db_cpu'] = db_cpu
        tmp_df['mom6_cpu'] = mom6_cpu
        tmp_df['refine'] = refine

        print(tmp_df.loc[tmp_df['name'].isin(_DISPLAY_NAMES)])
        logging.info(f'Finished: db_cpu={db_cpu}\tmom6_cpu={mom6_cpu}\t{end_time-start_time}')

        timing_dfs.append(tmp_df)

    full_df = pd.concat(timing_dfs, ignore_index=True)
    full_df.to_csv('timings.csv')

if __name__ == "__main__":
    main()
