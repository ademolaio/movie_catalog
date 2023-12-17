import bz2
import shutil
import os
from datetime import datetime

from loguru import logger


# Configure Loguru Logger
log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', f'unzip_task.py_{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
logger.add(log_file, rotation="10 MB")


def extract_zip_files(source_folder, target_folder):
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.bz2'):
            file_path = os.path.join(source_folder, file_name)
            target_file_name = file_name.replace('.bz2', '.csv')
            target_file_path = os.path.join(target_folder, target_file_name)

            try:
                with bz2.BZ2File(file_path, 'rb') as file_in, open(target_file_path, 'wb') as file_out:
                    shutil.copyfileobj(file_in, file_out)
                logger.info(f"Extracting {file_path} to {target_file_path}")
            except Exception as e:
                logger.error(f"Error extracting {file_path}: {e}")


def process_zip_files():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_folder_path = os.path.join(project_root, 'zip')
    csv_folder_path = os.path.join(project_root, 'csv')

    logger.info("Starting the extraction process...")
    extract_zip_files(zip_folder_path, csv_folder_path)
    logger.info("Extraction process completed")