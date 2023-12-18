from scripts.csv_unzip_script import process_zip_files
from config.postgres_connection_config import demonstrate_connection_capabilities


def main():
    process_zip_files()
    demonstrate_connection_capabilities()


if __name__ == '__main__':
    main()
