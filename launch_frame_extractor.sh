#!/bin/sh

#SBATCH --job-name=test
#SBATCH --mem=10000
#SBATCH --cpus-per-task=10
#SBATCH --partition=LARGE-G2
#SBATCH --gres=gpu:0
#SBATCH --output=frame_extractor.log
#SBATCH --error=frame_extractor.log

. /home/ICTDOMAIN/d20125529/fps_vs_size/venv/bin/activate
python generate_dataset.py --root_dir /home/ICTDOMAIN/d20125529/datasets/MCAD \
    --out_dir MCAD_FRAMES