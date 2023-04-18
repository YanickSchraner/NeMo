#!/bin/bash
#SBATCH --job-name=fairseq_to_json
#SBATCH --time=0:30:00
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1
#SBATCH --mem=5G
#SBATCH --qos=30min
#SBATCH --output=scicore_out/fairseq_to_json-%A_%a.out

ml CMake/3.23.1-GCCcore-11.3.0
ml libsndfile/1.1.0-GCCcore-11.3.0
ml FLAC/1.3.4-GCCcore-11.3.0
ml SoX/14.4.2-GCCcore-11.3.0
ml FFmpeg/.5.0.1-GCCcore-11.3.0
ml cuDNN/8.1.0.77-CUDA-11.2.1
ml Python/3.10.4-GCCcore-11.3.0

source venv/bin/activate

python scripts/dataset_processing/fairseq_to_json.py --data_dir '/scicore/home/graber0001/GROUP/stt/swissgerman_wav2vec_nobackup/data/corpus/stt/annotated/snf_testset/v1.0/2023-01-09_21-07-27' --splits 'test' --manifest '/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/snf_testset/2023-01-09_21-07-27'
