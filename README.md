# OLCF_Frontier_SmartSim_2023
Workshop materials for the SmartSim workshop at OLCF Frontier

Quick Instructions

1. Navigate to your directory on the Orion Lustre Filesystem

    ```
    export SCRATCH_ROOT=/lustre/orion/$PROJECT/scratch/$USER
    cd $SCRATCH_ROOT
    ```
1. Clone down the repository

    ```
    git clone https://github.com/CrayLabs/OLCF_SmartSim2023.git
    ```

1. Get a Slurm allocation

    ```
    salloc -N 1 -q debug -t 00:30:00 -A GEN150_smartsim
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
    cd $SCRATCH_ROOT/OLCF_SmartSim2023/smartsim_drivers
    python call_MOM6.py
    ```
