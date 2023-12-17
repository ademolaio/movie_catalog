from util.unzip_task import process_zip_files
from util.verification_task import execute_zip_to_csv_verification


def main():
    process_zip_files()
    execute_zip_to_csv_verification()


if __name__ == '__main__':
    main()
