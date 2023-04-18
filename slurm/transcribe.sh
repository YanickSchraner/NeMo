#!/bin/bash
#SBATCH --job-name=transcribe
#SBATCH --time=0-06:00:00
#SBATCH --cpus-per-task=10
#SBATCH --tasks-per-node=1
#SBATCH --mem=50G
#SBATCH --qos=gpu6hours
#SBATCH --gres=gpu:1
#SBATCH --partition=a100
#SBATCH --output=scicore_out/transcribe-%A_%a.out

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


python examples/asr/transcribe_speech.py \
    model_path="/scicore/home/graber0001/schran0000/NeMo/experiments/stt_de_conformer_ctc_large_finetuning/Conformer-CTC-BPE/2023-03-29_15-29-01/checkpoints/Conformer-CTC-BPE--val_wer=0.2661-epoch=56.ckpt" \
    dataset_manifest="/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/snf_testset/2023-01-09_21-07-27/test.json" \
    batch_size=32 \
    compute_timestamps=True \
    compute_langs=False \
    cuda=0 \
    amp=True \
    append_pred=False \
    audio_type='flac'