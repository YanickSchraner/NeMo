#!/bin/bash
#SBATCH --job-name=train_conformer_transducer_bpe
#SBATCH --time=7-00:00:00
#SBATCH --cpus-per-task=20
#SBATCH --tasks-per-node=4
#SBATCH --mem=50G
#SBATCH --qos=gpu1week
#SBATCH --gres=gpu:4
#SBATCH --partition=a100
#SBATCH --output=scicore_out/train-conformer-transducer-bpe-%A_%a.out

ml CMake/3.23.1-GCCcore-11.3.0
ml libsndfile/1.1.0-GCCcore-11.3.0
ml FLAC/1.3.4-GCCcore-11.3.0
ml SoX/14.4.2-GCCcore-11.3.0
ml FFmpeg/.5.0.1-GCCcore-11.3.0
ml CUDA/11.7.0
ml Python/3.10.4-GCCcore-11.3.0

source venv/bin/activate

export HYDRA_FULL_ERROR=1
export NCCL_DEBUG=INFO
export PYTHONFAULTHANDLER=1

srun python train/asr/speech_to_text_rnnt_bpe.py
