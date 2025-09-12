# Importing all the required Libraries and Packages.
import subprocess
import sys
import os
import shutil
from pathlib import Path

subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])


def download_dataset(dataset_name):
    # Storing the path to the directories that are being used.
    downloads_folder = Path.home() / "Downloads"
    target_directory = Path.home() / ".kaggle"
    target_directory.mkdir(exist_ok=True)

    # Listing out all the previously downloaded "kaggle.json" files.
    kaggle_files = list(downloads_folder.glob("kaggle*.json"))

    # Checking if the "kaggle.json" files exists in the Downloads folder.
    if len(kaggle_files) == 0:
        print('No "kaggle.json" file found in the Downloads folder.\nPlease download it from the website first.')

    else:
        latest_file = max(kaggle_files, key=os.path.getmtime) # Finding the latest downloaded file.
        target_path = target_directory / "kaggle.json" # Setting the target folder path to move the file to.
        
        shutil.move(latest_file, target_path) # Moving the file to the target folder.
        os.chmod(target_path, 0o600) # Giving the read/write access only to the owner.

        print(f'Moved latest "kaggle.json": {latest_file} to {target_path}')

        # Deleting the old irrelevant kaggle.json files from the Downloads folder.
        for old_file in kaggle_files:
            if old_file != latest_file:
                try:
                    old_file.unlink() # Removing the old file.
                    print(f"Removed old file: {old_file}")
                except Exception as e:
                    print(f"Error removing old file: {old_file}.\nError: {e}") # Exception Handling.
        
        project_path = os.getcwd() # Getting the current working directory to download the dataset to.

        # Downloading the Dataset using the Kaggle API.
        import kaggle
        kaggle.api.dataset_download_files(dataset_name, path=project_path, unzip=True)
    