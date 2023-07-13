# Introduction

This repository has all the scripts and inputs necessary to run a toy model
of the ocean using MOM6. A machine-learning model is embedded into the
numerical solver (the momentum component of the Navier-Stokes equations).

# Quick Instructions

1. Navigate to the workshop scratch space on the Lustre filesystem

    ```
    export SCRATCH_ROOT=/lustre/orion/gen150/world-shared/smartsim-2023/workshop_scratch/$USER
    cd $SCRATCH_ROOT
    ```

1. Clone down the repository

    ```
    git clone https://github.com/CrayLabs/OLCF_SmartSim2023.git
    ```

1. Get a Slurm allocation

    ```
    salloc -N 2 -t 01:00:00 --reservation=smartsim
    ```

1. Add the modulefile for SmartSim

    ```
    module use $SCRATCH_ROOT/OLCF_SmartSim2023/modulefiles
    ```

1. Load the modulefile

    ```
    module load py-smartsim-0.5.0-gcc-11.2.0
    ```

1. Run the MOM6 example

    ```
    cd $SCRATCH_ROOT/OLCF_SmartSim2023/smartsim_drivers/double_gyre
    python call_MOM6.py
    ```
