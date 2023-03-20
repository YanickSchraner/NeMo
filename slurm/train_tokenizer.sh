#!/bin/bash
#SBATCH --job-name=train_tokenizer
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=20
#SBATCH --ntasks=1
#SBATCH --mem=128G
#SBATCH --qos=6hours
#SBATCH --output=scicore_out/train-tokenizer-%A_%a.out

ml CMake/3.23.1-GCCcore-11.3.0
ml libsndfile/1.1.0-GCCcore-11.3.0
ml FLAC/1.3.4-GCCcore-11.3.0
ml SoX/14.4.2-GCCcore-11.3.0
ml FFmpeg/.5.0.1-GCCcore-11.3.0
ml cuDNN/8.2.1.32-CUDA-11.3.1
ml Python/3.10.4-GCCcore-11.3.0

source venv/bin/activate


python scripts/tokenizers/process_asr_text_tokenizer.py \
        --data_file="/scicore/home/graber0001/GROUP/stt/swissgerman_wav2vec_nobackup/data/corpus/lm/combined_text/2022-10-21_11-22-40/train.txt" \
        --data_root="checkpoints/spm" \
        --vocab_size=5000 \
        --tokenizer="spe" \
        --no_lower_case \
        --spe_type="unigram" \
        --spe_character_coverage=1.0 \
        --spe_sample_size=10000000 \
        --log
