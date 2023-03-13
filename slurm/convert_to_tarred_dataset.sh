#!/bin/bash
#SBATCH --job-name=convert_to_tarred_dataset
#SBATCH --time=0:30:00
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1
#SBATCH --mem=5G
#SBATCH --qos=30min
#SBATCH --output=scicore_out/convert_to_tarred_dataset-%A_%a.out

ml CMake/3.23.1-GCCcore-11.3.0
ml libsndfile/1.1.0-GCCcore-11.3.0
ml FLAC/1.3.4-GCCcore-11.3.0
ml SoX/14.4.2-GCCcore-11.3.0
ml FFmpeg/.5.0.1-GCCcore-11.3.0
ml cuDNN/8.1.0.77-CUDA-11.2.1
ml Python/3.10.4-GCCcore-11.3.0

source venv/bin/activate


python scripts/speech_recognition/convert_to_tarred_audio_dataset.py \
  --manifest_path=/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/combined/2022-10-21_12-29-58/train.json \
  --target_dir=/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/combined/2022-10-21_12-29-58/train_shards \
  --num_shards=120 # 1200h total, 10h per shard, dividable by 8 workers = 120 shards
  --max_duration=20 \
  --min_duration=2 \
  --sort_in_shards \
  --buckets_num=4 \
  --shuffle --shuffle_seed=42