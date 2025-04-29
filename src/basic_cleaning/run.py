#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    logger.info(f"Load input artifact: {args.input_artifact} from WanDB")

    idx = df['price'].between(args.min_price, args.max_price)
    logger.info(f"Selected price range between minimum {args.min_price} and maximum {args.max_price}")
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])


    df.to_csv("clean_sample.csv", index=False)

    logger.info(f"Upload cleaned data to {args.output_artifact}")
    artifact = wandb.Artifact(
    args.output_artifact,
    type=args.output_type,
    description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="The name of the data file that should be cleaned",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="The name of the output file",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="Name of the output data type",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="The description of the output file",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Minimum price to be considered",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Maximum price to be considered",  ## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
