# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
# Preparing the Tokenizer for the dataset
Use the `process_asr_text_tokenizer.py` script under <NEMO_ROOT>/scripts/tokenizers/ in order to prepare the tokenizer.

```sh
python <NEMO_ROOT>/scripts/tokenizers/process_asr_text_tokenizer.py \
        --manifest=<path to train manifest files, seperated by commas>
        OR
        --data_file=<path to text data, seperated by commas> \
        --data_root="<output directory>" \
        --vocab_size=<number of tokens in vocabulary> \
        --tokenizer=<"spe" or "wpe"> \
        --no_lower_case \
        --spe_type=<"unigram", "bpe", "char" or "word"> \
        --spe_character_coverage=1.0 \
        --log
```

# Training the model
```sh
python speech_to_text_ctc_bpe.py \
    # (Optional: --config-path=<path to dir of configs> --config-name=<name of config without .yaml>) \
    model.train_ds.manifest_filepath=<path to train manifest> \
    model.validation_ds.manifest_filepath=<path to val/test manifest> \
    model.tokenizer.dir=<path to directory of tokenizer (not full path to the vocab file!)> \
    model.tokenizer.type=<either bpe or wpe> \
    trainer.devices=-1 \
    trainer.accelerator="gpu" \
    trainer.strategy="ddp" \
    trainer.max_epochs=100 \
    model.optim.name="adamw" \
    model.optim.lr=0.001 \
    model.optim.betas=[0.9,0.999] \
    model.optim.weight_decay=0.0001 \
    model.optim.sched.warmup_steps=2000
    exp_manager.create_wandb_logger=True \
    exp_manager.wandb_logger_kwargs.name="<Name of experiment>" \
    exp_manager.wandb_logger_kwargs.project="<Name of project>"
```

# Fine-tune a model

For documentation on fine-tuning this model, please visit -
https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/configs.html#fine-tuning-configurations

# Pretrained Models

For documentation on existing pretrained models, please visit -
https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/results.html

"""

import pytorch_lightning as pl
import torch
from omegaconf import OmegaConf

from nemo.collections.asr.models.ctc_bpe_models import EncDecCTCModelBPE
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager


@hydra_runner(config_path="./conf/", config_name="conformer_ctc_bpe")
def main(cfg):
    logging.info(f'Hydra config: {OmegaConf.to_yaml(cfg)}')

    # Print available GPUs
    logging.info(f'Available GPUs: {torch.cuda.device_count()}')

    # Create PyTorch Lightning trainer with specified parameters
    trainer = pl.Trainer(**cfg.trainer)
    exp_manager(trainer, cfg.get("exp_manager", None))
    # asr_model = EncDecCTCModelBPE(cfg=cfg.model, trainer=trainer)
    asr_model = EncDecCTCModelBPE.restore_from(
        '/scicore/home/graber0001/schran0000/NeMo/experiments/stt_de_conformer_ctc_large_finetuning/Conformer-CTC-BPE/2023-03-29_15-29-01/checkpoints/Conformer-CTC-BPE.nemo',
        trainer=trainer)
    # Update vocab
    # asr_model.change_vocabulary(new_tokenizer_dir=cfg.model.tokenizer.dir, new_tokenizer_type=cfg.model.tokenizer.type)
    asr_model.setup_training_data(train_data_config=cfg.model.train_ds)
    asr_model.setup_validation_data(val_data_config=cfg.model.validation_ds)
    # asr_model.cfg.sample_rate = cfg.model.sample_rate
    # asr_model.cfg.log_prediction = cfg.model.log_prediction
    # asr_model.cfg.ctc_reduction = cfg.model.ctc_reduction
    # asr_model.spec_augment = asr_model.from_config_dict(cfg.model.spec_augment)
    # asr_model.cfg.optim.name = cfg.model.optim.name
    # asr_model.cfg.optim.lr = cfg.model.optim.lr
    # asr_model.cfg.optim.betas = cfg.model.optim.betas
    # asr_model.cfg.optim.weight_decay = cfg.model.optim.weight_decay
    # asr_model.cfg.optim.sched.warmup_steps = cfg.model.optim.sched.warmup_steps
    # asr_model.cfg.optim.sched.warmup_ratio = cfg.model.optim.sched.warmup_ratio
    # asr_model.cfg.optim.sched.min_lr = cfg.model.optim.sched.min_lr
    # asr_model.cfg.optim.sched.name = cfg.model.optim.sched.name
    # asr_model.cfg.optim.sched.d_model = cfg.model.optim.sched.d_model

    # Validate model before training
    trainer.validate(asr_model)

    model_path = '/scicore/home/graber0001/schran0000/NeMo/experiments/stt_de_conformer_ctc_large_finetuning/Conformer-CTC-BPE/2023-03-29_15-29-01/checkpoints/Conformer-CTC-BPE--val_wer=0.2661-epoch=56.ckpt'
    # Validate pretrained model
    trainer.validate(asr_model, ckpt_path=model_path)

    # Fit model to data
    trainer.fit(asr_model, ckpt_path=model_path)

    if hasattr(cfg.model, 'test_ds') and cfg.model.test_ds.manifest_filepath is not None:
        if asr_model.prepare_test(trainer):
            asr_model.setup_test_data(test_data_config=cfg.model.test_ds)
            trainer.test(asr_model)


if __name__ == '__main__':
    main()
