# Introduction

This repository has all the scripts and inputs necessary to run a toy model
of the ocean using MOM6. A machine-learning model is embedded into the
numerical solver (the momentum component of the Navier-Stokes equations).

# Quick Instructions

1.  Go to user directory on scratch

    ```
    export SCRATCH_ROOT=/lus/scratch/$USER/demo_scratch
    mkdir -p $SCRATCH_ROOT
    cd $SCRATCH_ROOT
    ```

1. Clone down the repository and checkout horizon branch

    ```
    git clone https://github.com/CrayLabs/OLCF_SmartSim2023.git
    git checkout horizon
    ```

1. Get a Slurm allocation

    ```
    salloc -N 1 -t 01:00:00 -C P100
    ```

1. Add the modulefile for SmartSim

    ```
    module use /lus/scratch/smartsim/local/modulefiles
    ```

1. Load the modulefile

    ```
    module load py-smartsim/0.5.0
    ```

1. Run the MOM6 example

    ```
    cd $SCRATCH_ROOT/OLCF_SmartSim2023/smartsim_drivers/double_gyre
    ulimit -s unlimited # Necessary for MOM6
    python call_MOM6.py
    ```
