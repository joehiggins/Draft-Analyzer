# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 17:58:10 2017

@author: Joe
"""

import boto3
import botocore
import pandas as pd
import os

def prepare_data():
    '''
    print("starting data prep")
    
    #Access keys to our S3
    access_key = os.environ['access_key']
    secret_access_key = os.environ['secret_access_key']    
    
    s3 = boto3.resource(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_access_key 
    )

    print("grabbing data")

    #Grab the file from a specific bucket associated with our S3
    bucket_name = 'elasticbeanstalk-us-west-2-713897343340'
    file_path = 'Draft Analyzer/'
    file = 'dota2_pro_match_picks_bans.pkl' # replace with your object key    
    
    try:
        s3.Bucket(bucket_name).download_file(file_path + file, 'from_s3.pkl')
        #s3.Bucket(bucket_name).download_file(file_path + file, '../DotA2 Data/from_s3.pkl')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    '''
    print("reading data")
    
    #read data
    file_path = ''
    file_name = 'from_s3.pkl'
    df = pd.read_pickle(file_path + file_name)
    
    #for now, getting rid of the object list, because its big and takes up memory
    df = df.drop('picks_bans', 1)
    
    print("data ready")    
    
    return df