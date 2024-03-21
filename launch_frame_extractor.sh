#!/bin/sh

#SBATCH --job-name=FR_GEN
#SBATCH --mem=10000
#SBATCH --cpus-per-task=10
#SBATCH --partition=LARGE-G2
#SBATCH --gres=gpu:0
#SBATCH --output=frame_extractor.log
#SBATCH --error=frame_extractor.log

. /home/ICTDOMAIN/d20125529/fps_vs_size/venv/bin/activate

# python generate_dataset.py --root_dir /home/ICTDOMAIN/d20125529/datasets/MCAD \
#     --out_dir MCAD_FRAMES \
#     --act extract

# python generate_dataset.py --root_dir MCAD_FRAMES \
#     --out_dir MCAD_FRAMES \
#     --act annotation

# python generate_dataset.py --root_dir /home/ICTDOMAIN/d20125529/datasets/MMAct/trimmed/data \
#     --out_dir MMAct_FRAMES \
#     --act extract \
#     --dataset mmact

python generate_dataset.py --root_dir MMAct_FRAMES \
    --out_dir MMAct_FRAMES \
    --act annotation \
    --dataset mmact

