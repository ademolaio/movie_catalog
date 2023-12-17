import bz2
import shutil
import os
from datetime import datetime
from util.verification_util import verify_zip_extraction
from loguru import logger
from config.logging_config import script_filter

# Configure Loguru Logger
unzip_logger = logger.bind(script="unzip_script")
log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                             f'unzip_script.py_{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
unzip_logger.add(log_file_path, filter=script_filter('unzip_script'), rotation="10 MB", enqueue=True)


def extract_zip_files(source_folder, target_folder):
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.bz2'):
            file_path = os.path.join(source_folder, file_name)
            target_file_name = file_name.replace('.bz2', '.csv')
            target_file_path = os.path.join(target_folder, target_file_name)

            try:
                with bz2.BZ2File(file_path, 'rb') as file_in, open(target_file_path, 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)
                unzip_logger.info(f"Extracting {file_path} to {target_file_path}")
            except Exception as e:
                unzip_logger.error(f"Error extracting {file_path}: {e}")


def process_zip_files():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_folder_path = os.path.join(project_root, 'zip')
    csv_folder_path = os.path.join(project_root, 'csv')

    unzip_logger.info("Starting the extraction process...")
    extract_zip_files(zip_folder_path, csv_folder_path)
    unzip_logger.info("Extraction process completed")

    logger.info("Starting the Zip to CSV verification process")
    if verify_zip_extraction(zip_folder_path, csv_folder_path):
        unzip_logger.info(f"All files are verified successfully for {csv_folder_path}")
    else:
        unzip_logger.error("Some files are missing their corresponding .csv files please check the zip folder")
