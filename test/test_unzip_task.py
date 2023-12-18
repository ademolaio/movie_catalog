import os
import pytest
from scripts.csv_unzip_script import extract_zip_files


@pytest.fixture
def setup_unzip_test_env(tmp_path):
    # Create a temporary directory structure
    zip_dir = tmp_path / "zip"
    csv_dir = tmp_path / "csv"
    zip_dir.mkdir()
    csv_dir.mkdir()

    # Create a test .csv.bz2 file
    test_csv_bz2_file = csv_dir / "test.csv.bz2"
    with open(test_csv_bz2_file, "wb") as f:
        f.write(b"test content")
    return str(zip_dir), str(csv_dir)


def test_extract_zip_files(setup_unzip_test_env):
    zip_dir, csv_dir = setup_unzip_test_env
    extract_zip_files(zip_dir, csv_dir)

    # Check if the extract files exists
    assert os.path.isfile(os.path.join(csv_dir, "test.csv.bz2"))
