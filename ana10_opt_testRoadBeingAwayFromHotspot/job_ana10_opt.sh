#!/bin/bash
#SBATCH --array=0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --mem-per-cpu=3700
#SBATCH --partition=compute
#SBATCH --time=40:00:00
#SBATCH --output=slurm-%A_%a.out

ml purge ## get rid of modules
ml load GCCcore/11.3.0 Python/3.10.4
source ~/research_project/my_env/bin/activate

# define methods
#P_DETECT_JAs=(0.25 0.5 0.75 0.9)
#ROAD_JAs=("0" "1")
#AREA_JAs=("0" "1")
AREA_ROAD_JAs=(2)
SURVEY_FREQ_JAs=(52) 
NSITES_JAs=(10)

#NUM1=${#ROAD_JAs[@]}
#NUM2=${#AREA_JAs[@]}
NUM1=${#AREA_ROAD_JAs[@]}
NUM2=${#SURVEY_FREQ_JAs[@]}
NUM3=${#NSITES_JAs[@]}
TASK_ID=$SLURM_ARRAY_TASK_ID


# Compute indices
let "i1=TASK_ID/(NUM2*NUM3)"         # index for AREA_ROAD_JAs
let "i2=(TASK_ID/(NUM3))%NUM2"       # index for SURVEY_FREQ_JAs
let "i3=(TASK_ID)%NUM3"            # index for NSITES_JAs


# Assign parameter values
#ROAD_JA=${ROAD_JAs[$i1]}
#AREA_JA=${AREA_JAs[$i2]}
AREA_ROAD_JA=${AREA_ROAD_JAs[$i1]}
SURVEY_FREQ_JA=${SURVEY_FREQ_JAs[$i2]}
NSITES_JA=${NSITES_JAs[$i3]}

python ana10_opt.py "$AREA_ROAD_JA" "$SURVEY_FREQ_JA" "$NSITES_JA"
