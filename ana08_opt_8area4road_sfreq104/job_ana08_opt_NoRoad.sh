#!/bin/bash
#SBATCH --array=0-23
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --mem-per-cpu=3700
#SBATCH --time=40:00:00
#SBATCH --output=slurm-%A_%a.out

ml purge ## get rid of modules
ml load GCCcore/11.3.0 Python/3.10.4
source ~/research_project/my_env/bin/activate

# define methods
#P_DETECT_JAs=(0.25 0.5 0.75 0.9)
ROAD_JAs=("01_0")
AREA_JAs=("01" "02" "03" "04" "05" "06" "07" "08")
SURVEY_FREQ_JAs=(104) # (52 26 17)  # representing once, twice, thrice per year
NSITES_JAs=(5 10 15) #(5 10 15 20)  

NUM1=${#ROAD_JAs[@]}
NUM2=${#AREA_JAs[@]}
NUM3=${#SURVEY_FREQ_JAs[@]}
NUM4=${#NSITES_JAs[@]}
TASK_ID=$SLURM_ARRAY_TASK_ID


# Compute indices
let "i1=TASK_ID/(NUM2*NUM3*NUM4)"         # index for ROAD_JAs
let "i2=(TASK_ID/(NUM4*NUM3))%NUM2"       # index for AREA_JAs
let "i3=(TASK_ID/(NUM4))%NUM3"            # index for SURVEY_FREQ_JAs
let "i4=TASK_ID%NUM4"                     # index for NSITES_JAs

# Assign parameter values
ROAD_JA=${ROAD_JAs[$i1]}
AREA_JA=${AREA_JAs[$i2]}
SURVEY_FREQ_JA=${SURVEY_FREQ_JAs[$i3]}
NSITES_JA=${NSITES_JAs[$i4]}

python ana08_opt_NoRoad.py "$ROAD_JA" "$AREA_JA" "$SURVEY_FREQ_JA" "$NSITES_JA"

