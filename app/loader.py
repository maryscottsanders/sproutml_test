"""
Start Date: 22 January 2019
Project AWS NLP Pipeline
"""

import pandas as pd
import io
import sys
import os
from io import BytesIO
from sklearn.externals import joblib

import boto3
from botocore import UNSIGNED
from botocore import exceptions
from botocore.client import Config


class DataLoader:

    def __init__(self):
        # to load in basic values
        self.features = None
        self.response = None
        self.data = None

    @staticmethod
    def get_s3_bucket_name():
        return DataLoader.get_required_environment_variable('PROD_ML_S3_BUCKET')

    @staticmethod
    def get_input_data_filename():
        return DataLoader.get_required_environment_variable('PROD_ML_INPUT_DATA_FILENAME')

    @staticmethod
    def get_required_environment_variable(variable_name):
        value = os.environ.get(variable_name)

        if value == None:
            print('error: unable to find environment variable ' + variable_name)
            sys.exit(1)

        return value

    def query_data(self):
        """
        Method to populate object with data in a structured csv file
        :return: updates self with features
        """
        # Load Data - Check Locally & S3

        print('Looking for data locally...')
        filename = DataLoader.get_input_data_filename()

        try:
            data = pd.read_csv(filename)
            features = data.features
            response = data.response
            print('Data found locally and loaded.')
        except FileNotFoundError:
            print('Data not found locally. Pulling from S3...')

            try:
                s3client = boto3.client('s3')
                bucket_name = self.get_s3_bucket_name()
                obj = s3client.get_object(Bucket=bucket_name, Key=filename)
            except exceptions.ClientError as e:
                print('error: unable to download object from S3:', e)
                sys.exit(1)

            try:
                initialBytes = obj['Body'].read()
                buffer = io.BytesIO(initial_bytes)

                print('Data loaded from S3.')
            except FileNotFoundError:
                print('error: unable to read file after S3 download')
                sys.exit(1)

        data = pd.read_csv(buffer)

        self.features = data.features
        self.response = data.response
        self.data = data
