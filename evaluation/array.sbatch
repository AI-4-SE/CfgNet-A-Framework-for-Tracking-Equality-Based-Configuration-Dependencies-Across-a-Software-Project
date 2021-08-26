#!/bin/bash
#SBATCH --exclusive
#SBATCH --array=0
#SBATCH --partition=brown
#SBATCH --job-name=cfgnet_so_evaluation
#SBATCH --output=output/cfgnet-so-%a.out
#SBATCH --error=error/cfgnet-so-%a.err

task.sh $(pwd)
