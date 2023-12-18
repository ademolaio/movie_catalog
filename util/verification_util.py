import os
from datetime import datetime
from config.logging_config import script_filter
from loguru import logger


# Configure Loguru Logger
verify_logger = logger.bind(script="verification_util")
log_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                             f'verification_util.py_{datetime.now().strftime("%Y%m%d-%H%M%S")}.log')
verify_logger.add(log_file_path, filter=script_filter('verification_util'), rotation="10 MB", enqueue=True)


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
            corresponding_csv = file_name.replace('.bz2', '.csv')
            csv_file_path = os.path.join(csv_folder, corresponding_csv)

            if os.path.isfile(csv_file_path):
                verify_logger.info(f"Verified: '{file_name}' has corresponding .csv file '{corresponding_csv}")
            else:
                verify_logger.warning(f"Missing: No corresponding CSV file '{file_name}'")
                all_files_verified = False

    return all_files_verified

