import argparse
import json
import os


def main():
    parser = argparse.ArgumentParser(description="Calculate manifest statistics")
    parser.add_argument(
        "--data_dir", required=True, type=str, help="data in fairseq format",
    )
    parser.add_argument(
        "--splits", required=True, type=str, help="comma-separated list of splits to process",
    )

    args = parser.parse_args()

    manifest_dir = args.data_dir
    splits = args.splits.split(",")

    for split in splits:
        # read <split>.json
        with open(os.path.join(manifest_dir, split + '.json')) as f:
            data = json.load(f)
            # Calculate statistics
            durations = [d['duration'] for d in data]
            print(f"Split: {split}")
            print(f"Number of samples: {len(durations)}")
            print(f"Average duration: {sum(durations) / len(durations)}")
            print(f"Max duration: {max(durations)}")
            print(f"Min duration: {min(durations)}")
            print()


if __name__ == "__main__":
    main()
