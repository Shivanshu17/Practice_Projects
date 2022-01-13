# -*- coding: utf-8 -*-
import requests
import csv
import click
import logging
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv


@click.command()
#@click.argument('input_filepath', type=click.Path(exists=True))
#@click.argument('output_filepath', type=click.Path())
def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    data_url  = "https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews/download"
    #data_url = "https://github.com/laxmimerit/IMDB-Movie-Reviews-Large-Dataset-50k/blob/master/train.xlsx"
    data_response = requests.get(data_url)
    url_content = data_response.content
    dirname = os.path.dirname(__file__)
    data_path = os.path.join(dirname, '../../data/raw/')
    file_name = 'imdb_dataset.csv'
    complete_name = os.path.join(data_path, file_name)
    # #data_path = "../../data/raw/IMDB Dataset.csv"
    # is_path = os.path.isdir(data_path)
    # print(is_path)
    csv_file = open(complete_name, 'wb')
    csv_file.write(url_content)
    csv_file.close()
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
