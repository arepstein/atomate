#!/bin/bash
#SBATCH --job-name=crest_ts
#SBATCH --time=24:00:00
#SBATCH --partition=savio2
#SBATCH --account=fc_lsdi

crest input.xyz -squick
