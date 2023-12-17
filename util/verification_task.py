import os
from datetime import datetime
from loguru import logger

# Configure Loguru Logger
verify_logger = logger.bind(naam="verification_task")
log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                             f'verification_task.py_{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
verify_logger.add(log_file_path, rotation="10 MB")


def verify_zip_extraction(zip_folder, csv_folder):
    """
    Verifies that for each .bz2 file in the zip folder, there is a corresponding .csv file in the csv folder.

    :param zip_folder: Path to the folder containing .bz2 files
    :param csv_folder: Path to the folder where .csv files are stored
    :return: True if all files are verified, False otherwise
    """

    all_files_verified = True

    for file_name in os.listdir(zip_folder):
        if file_name.endswith('.bz2'):
            csv_file_path = file_name.replace('.bz2', '.csv')
            csv_file_path = os.path.join(csv_folder, csv_file_path)

            if not os.path.isfile(csv_file_path):
                verify_logger.warning(f"Missing CSV file(s) for: {csv_file_path}")
                all_files_verified = False

    return all_files_verified


def execute_zip_to_csv_verification():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_folder_path = os.path.join(project_root, 'zip')
    csv_folder_path = os.path.join(project_root, 'csv')

    logger.info("Starting the Zip to CSV verification process")
    if verify_zip_extraction(zip_folder_path, csv_folder_path):
        verify_logger.info(f"All files are verified successfully for {csv_folder_path}")
    else:
        verify_logger.error("Some files are missing their corresponding .csv files please check the zip folder")
