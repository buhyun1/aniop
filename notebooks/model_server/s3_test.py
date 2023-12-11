from dotenv import load_dotenv
import boto3
import os
import json
load_dotenv("../.env")
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')


s3 = boto3.client('s3',
                    region_name=region_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

# S3 버킷 내부 파일 목록 조회
def list_files_in_bucket(bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                print("'"+item['Key']+"'")
        else:
            print(f"버킷 {bucket_name}은 비어있습니다.")
    except Exception as e:
        print(f"파일 목록을 조회하는 중 오류가 발생했습니다: {e}")

#s3 버킷 내부 파일 조회
def see_file_from_bucket(bucket, file_name):
    try:
        input_obj = s3.get_object(Bucket="aniop2023", Key=file_name)
        input_data = json.loads(input_obj['Body'].read().decode('utf-8'))
        print(input_data)   
    except Exception as e:
        print(f"파일을 다운로드하는 중 오류가 발생했습니다: {e}")


# Keep only Title and Link
def keep_only_title_and_link(bucket_name, file_name):
    input_obj = s3.get_object(bucket_name, Key=file_name)
    input_data = json.loads(input_obj['Body'].read().decode('utf-8'))
    print(input_data)
    for item in input_data['news']:
        keys_to_remove = [key for key in item if key not in ('Title', 'Link')]
        for key in keys_to_remove:
            del item[key]
    # Convert back to JSON
    json_data = json.dumps(input_data, indent=4)
    s3.put_object(Body=json_data, Bucket="aniop2023", Key=file_name)
    print(input_data)
    return input_data

def del_file_from_bucket(bucket_name, file_name):
    try:
        response = s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(response)
    except Exception as e:
        print(f"파일을 삭제하는 중 오류가 발생했습니다: {e}")

#see_file_from_bucket("aniop2023","20231127_combined_news_3.json")
#del_file_from_bucket("aniop2023","manual_predicted_news_articles_2.json")
# list_files_in_bucket("aniop2023") #버킷 내부 파일 목록 조회

def main():
    while True:
        print("\nOptions:")
        print("1: List files in bucket")
        print("2: View a file from bucket")
        print("3: Keep only Title and Link in a file")
        print("4: Delete a file from bucket")
        print("5: Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            bucket_name = input("Enter bucket name: ")
            list_files_in_bucket(bucket_name)
        elif choice == '2':
            bucket_name = input("Enter bucket name: ")
            file_name = input("Enter file name: ")
            see_file_from_bucket(bucket_name, file_name)
        elif choice == '3':
            bucket_name = input("Enter bucket name: ")
            file_name = input("Enter file name: ")
            keep_only_title_and_link(bucket_name, file_name)
        elif choice == '4':
            bucket_name = input("Enter bucket name: ")
            file_name = input("Enter file name: ")
            del_file_from_bucket(bucket_name, file_name)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please choose a number between 1 and 5.")

if __name__ == "__main__":
    main()
