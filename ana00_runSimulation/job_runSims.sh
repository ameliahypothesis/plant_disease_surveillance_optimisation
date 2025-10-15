#!/bin/bash
#SBATCH --partition=hmem
#SBATCH --array=0-4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem-per-cpu=3700
#SBATCH --time=40:00:00


ml purge ## get rid of modules
ml load GCCcore/11.3.0 Python/3.10.4
source ~/research_project/my_env/bin/activate

AREA_JAs=("04" "05" "06" "07" "08")

NUM1=${#AREA_JAs[@]}
TASK_ID=$SLURM_ARRAY_TASK_ID

let "i1=TASK_ID%NUM1"                     # index for NSITES_JAs

# Assign parameter values
AREA_JA=${AREA_JAs[$i1]}

python run_sims.py "$AREA_JA"
