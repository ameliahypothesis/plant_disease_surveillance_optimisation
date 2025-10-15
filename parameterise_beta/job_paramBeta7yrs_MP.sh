#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem-per-cpu=3700
#SBATCH --time=40:00:00

ml purge ## get rid of modules
ml load GCCcore/11.3.0 Python/3.10.4
source ~/research_project/my_env/bin/activate
python parameterise_beta_7yrs.py
