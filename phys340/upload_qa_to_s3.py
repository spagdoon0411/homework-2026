#!/usr/bin/env python3
import argparse
import json
import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError


def parse_json_files(folder_path):
    qa_pairs = []
    folder = Path(folder_path)

    for json_file in folder.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    qa_pairs.extend(data)
                else:
                    print(f"Warning: {json_file} does not contain a list")
        except json.JSONDecodeError as e:
            print(f"Error parsing {json_file}: {e}")
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    return qa_pairs


def create_qa_file_content(question, answer):
    return f"Q: {question}\nA: {answer}"


def sanitize_filename(text, max_length=100):
    sanitized = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in text)
    sanitized = sanitized.strip().replace(" ", "_")
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized


def upload_to_s3(qa_pairs, bucket_name):
    s3_client = boto3.client("s3")

    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            print(f"Error: Bucket '{bucket_name}' does not exist")
        else:
            print(f"Error accessing bucket '{bucket_name}': {e}")
        return

    uploaded_count = 0
    failed_count = 0

    for idx, qa in enumerate(qa_pairs, start=1):
        if "Q" not in qa or "A" not in qa:
            print(f"Warning: Q&A pair {idx} is missing 'Q' or 'A' field, skipping")
            failed_count += 1
            continue

        question = qa["Q"]
        answer = qa["A"]

        file_content = create_qa_file_content(question, answer)

        sanitized_q = sanitize_filename(question)
        s3_key = f"qa_{idx}_{sanitized_q}.txt"

        try:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_content.encode("utf-8"),
                ContentType="text/plain",
            )
            uploaded_count += 1
            print(f"Uploaded: {s3_key}")
        except Exception as e:
            print(f"Error uploading {s3_key}: {e}")
            failed_count += 1

    print(f"\nUpload complete: {uploaded_count} files uploaded, {failed_count} failed")


def main():
    parser = argparse.ArgumentParser(
        description="Extract Q&A pairs from JSON files and upload to S3"
    )
    parser.add_argument(
        "folder", help="Path to folder containing JSON files with Q&A pairs"
    )
    parser.add_argument("bucket", help="S3 bucket name to upload files to")

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a valid directory")
        return

    print(f"Reading JSON files from: {args.folder}")
    qa_pairs = parse_json_files(args.folder)
    print(f"Found {len(qa_pairs)} Q&A pairs")

    if not qa_pairs:
        print("No Q&A pairs found to upload")
        return

    print(f"Uploading to S3 bucket: {args.bucket}")
    upload_to_s3(qa_pairs, args.bucket)


if __name__ == "__main__":
    main()



