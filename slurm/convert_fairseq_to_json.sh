#!/bin/bash
#SBATCH --job-name=fairseq_to_json
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=10
#SBATCH --ntasks=1
#SBATCH --mem=5G
#SBATCH --qos=6hours
#SBATCH --output=scicore_out/fairseq_to_json-%A_%a.out

ml CUDA/11.7.0
ml Miniconda2/4.3.30
ml intel/2022.00
source activate nemo

sbatch python scripts/dataset_processing/fairseq_to_json.py --data_dir '/scicore/home/graber0001/GROUP/stt/swissgerman_wav2vec_nobackup/data/corpus/stt/annotated/combined_annotated_speech/2022-10-21_12-29-58' --splits 'train,test,valid' --manifest '/scicore/home/graber0001/GROUP/stt/nemo_nobackup/data/combined/2022-10-21_12-29-58'
