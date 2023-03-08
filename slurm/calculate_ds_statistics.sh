#!/bin/bash
#SBATCH --job-name=calculate_ds_statistics
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1
#SBATCH --mem=5G
#SBATCH --qos=6hours
#SBATCH --output=scicore_out/calculate_ds_statistics-%A_%a.out

ml CMake/3.23.1-GCCcore-11.3.0
ml libsndfile/1.1.0-GCCcore-11.3.0
ml FLAC/1.3.4-GCCcore-11.3.0
ml SoX/14.4.2-GCCcore-11.3.0
ml FFmpeg/.5.0.1-GCCcore-11.3.0
ml cuDNN/8.1.0.77-CUDA-11.2.1
ml Python/3.10.4-GCCcore-11.3.0

source venv/bin/activate

python scripts/dataset_processing/calculate_statistics.py --data_dir '/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/combined/2022-10-21_12-29-58' --splits 'train,test,valid'
