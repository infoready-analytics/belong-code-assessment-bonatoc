import argparse
from pathlib import Path

from belong_code_assessment import api
from belong_code_assessment.aws import upload_to_s3
from belong_code_assessment.config import Config
from belong_code_assessment.stats import aggregate
from belong_code_assessment.utils import load_dataframe, save_dataframe


def _arg_check_exists(arg):
    if not Path(arg).exists():
        raise argparse.ArgumentTypeError(f"{arg} does not exist.")

    return arg


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config-file",
        required=True,
        type=_arg_check_exists,
        help="Path to a yaml configuration to load.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    cfg = Config(args.config_file)

    this_dir = Path(__file__).parent.absolute()
    output_dir = Path(
        this_dir.parent.joinpath("data") if not cfg["output_dir"] else cfg["output_dir"]
    )
    output_dir.mkdir(exist_ok=True, parents=True)

    df = None

    df_path = output_dir.joinpath("pedestrian_counts.parquet")

    if df_path.exists() and cfg["load_dataframe"]:
        df = load_dataframe(df_path)
    elif cfg["pedestrian_csv_url"]:
        output_filepath = output_dir.joinpath("pedestrian_counts.csv")
        df = api.get_pedestrian_data_from_http(cfg["pedestrian_csv_url"], output_filepath)
    elif cfg["pedestrian_api_url"]:
        df = api.get_pedestrian_data_from_api(cfg["pedestrian_api_url"])

    if df is None:
        raise RuntimeError("Could not load data into DataFrame.")

    if cfg["save_dataframe"] and not df_path.exists():
        df.to_parquet(df_path)

    outputs = aggregate(df)

    for key, output_df in outputs.items():
        output_path = output_dir.joinpath(f"{key}.csv")
        save_dataframe(output_df, output_path, fmt="csv")
        upload_to_s3(output_path, cfg["aws_s3_bucket"])


if __name__ == "__main__":
    main()
