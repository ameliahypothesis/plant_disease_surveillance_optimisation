#!/bin/bash
#SBATCH --array=0-8
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=3700
#SBATCH --partition=compute
#SBATCH --time=40:00:00
#SBATCH --output=slurm-%A_%a.out

ml purge ## get rid of modules
ml load GCCcore/11.3.0 Python/3.10.4
source ~/research_project/my_env/bin/activate

# define methods

SURVEY_FREQ_JAs=(26 52 104) 
NSITES_JAs=(5 10 15)


NUM1=${#SURVEY_FREQ_JAs[@]}
NUM2=${#NSITES_JAs[@]}
TASK_ID=$SLURM_ARRAY_TASK_ID


# Compute indices
let "i1=TASK_ID/NUM2"         # index for SURVEY_FREQ_JAs
let "i2=TASK_ID%NUM2"       # index for NSITES_JAs

# Assign parameter values

SURVEY_FREQ_JA=${SURVEY_FREQ_JAs[$i1]}
NSITES_JA=${NSITES_JAs[$i2]}

python ana99_results.py "$SURVEY_FREQ_JA" "$NSITES_JA"
