import argparse
import json
import os

import pandas as pd

from nemo.utils import logging


def main():
    parser = argparse.ArgumentParser(description="Convert fairseq data folder to manifest.json")
    parser.add_argument(
        "--data_dir", required=True, type=str, help="data in fairseq format",
    )
    parser.add_argument(
        "--splits", required=True, type=str, help="comma-separated list of splits to process",
    )
    parser.add_argument(
        "--manifest", required=True, type=str, help="path to store the manifest file",
    )
    args = parser.parse_args()

    fairseq_folder = args.data_dir
    splits = args.splits.split(",")
    required_data = {
        "audio_filepath_duration": os.path.join(fairseq_folder, "*.tsv"),
        "text": os.path.join(fairseq_folder, "*.wrd"),
    }

    output_names = list(required_data.keys())

    # check if required files exist
    for name, file in required_data.items():
        for split in splits:
            file = file.replace("*", split)
            if not os.path.exists(file):
                raise ValueError(f"{os.path.basename(file)} is not in {fairseq_folder}.")

    for split in splits:
        # read path and duration
        path_duration_df = pd.read_csv(required_data["audio_filepath_duration"].replace("*", split), sep="\t",
                                       header=None, skiprows=1)
        path_duration_df = path_duration_df.rename(columns={0: "audio_filepath", 1: "duration"})

        # read text
        with open(required_data["text"].replace("*", split), "r", encoding="utf-8") as f:
            text = f.read().splitlines()
        text = pd.DataFrame(text, columns=["text"])

        # merge
        wav_segments_text = pd.concat([path_duration_df, text], axis=1)

        # write data to .json
        entries = wav_segments_text[output_names].to_dict(orient="records")
        manifest = os.path.join(args.manifest, f"{split}.json")
        os.makedirs(manifest, exist_ok=True)
        with open(manifest, "w", encoding="utf-8") as fout:
            for m in entries:
                fout.write(json.dumps(m, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
