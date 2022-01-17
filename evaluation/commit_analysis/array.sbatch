#!/bin/bash
#SBATCH --exclusive
#SBATCH --array=0-11
#SBATCH --partition=brown
#SBATCH --job-name=cfgnet_evaluation
#SBATCH --output=output/cfgnet-%a.out
#SBATCH --error=error/cfgnet-%a.err

task.sh $SLURM_ARRAY_TASK_ID $(pwd)
