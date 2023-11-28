import boto3
import os
import sys
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# Add the path of lambda_handler.py to sys.path
#sys.path.append(os.path.abspath('../models/kobert'))
#sys.path.append(os.path.abspath("../models/kpf-sbert"))

#for docker container path
sys.path.append(os.path.abspath("models/kobert"))
sys.path.append(os.path.abspath("models/kpf-sbert"))


from dotenv import load_dotenv
from lambda_handler import lambda_handler
from lambda_cluster import lambda_cluster
# Load environment variables
#load_dotenv("../.env")

#for docker container env path
load_dotenv("./.env")
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')

print("cluster aws_access_key_id:", aws_access_key_id)  
print("cluster aws_secret_access_key:", aws_secret_access_key)
print("cluster region_name:", region_name)
def list_s3_files(bucket_name, s3_client):
    """List files in an S3 bucket."""
    try:
        logging.info(f"Listing files in bucket {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [item['Key'] for item in response['Contents']]
        else:
            return []
    except Exception as e:
        logging.error(f"Error listing S3 files: {e}")
        return []

def load_processed_files(file_path):
    """Load a list of processed files from a local file."""
    try:
        logging.info(f"Loading processed files from {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().splitlines()
        return []
    except Exception as e:
        logging.error(f"Error loading processed files: {e}")
        return []
def save_processed_files(processed_files, file_path):
    """Save the list of processed files to a local file."""
    try:
        logging.info(f"Saving processed files to {file_path}")
        with open(file_path, 'w') as file:
            for file_name in processed_files:
                file.write(file_name + '\n')
    except Exception as e:
        logging.error(f"Error saving processed files: {e}")
def main():
    bucket_name = "aniop2023"
    processed_files_path = 'processed_files.txt'

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, 
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)

    # Get the current list of files in the S3 bucket
    s3_files = list_s3_files(bucket_name, s3_client)

    # Load the list of files that have already been processed
    processed_files = load_processed_files(processed_files_path)

    # Identify new files
    new_files = [file for file in s3_files if file not in processed_files]
    if new_files:
        logging.info(f"New files found: {new_files}")
        # Process each new file
        for new_file in new_files:
            classificated_file_name = new_file.replace('.json', '_2.json')
            event = {
                'bucket': bucket_name,
                'input_file': new_file,
                'output_file': classificated_file_name
            }
            # Call classification function (lambda_handler)
            logging.info(f"Processing file {new_file} for classification")
            lambda_handler(event, None)
            logging.info("Classification completed")
            
            processed_files.append(classificated_file_name)
            save_processed_files(processed_files, processed_files_path)
            logging.info("Updated processed files list")

            # Call clustering function (lambda_cluster)
            clustered_file_name = classificated_file_name.replace('_2.json', '_3.json')
            event = {
                'bucket': bucket_name,
                'input_file': classificated_file_name,
                'output_file': clustered_file_name
            }
            logging.info(f"Processing file {classificated_file_name} for clustering")
            lambda_cluster(event)  # Call the imported lambda_handler function
            logging.info("Clustering completed")
    else:
        logging.info("No new files found.")

if __name__ == "__main__":
    main()