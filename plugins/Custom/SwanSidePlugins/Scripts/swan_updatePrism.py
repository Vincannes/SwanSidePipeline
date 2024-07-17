import re
import os
import sys
import json
import shutil
import logging
import datetime

THIS_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(THIS_DIR, "ExternalModules", "releaser_modules"))

import requests
from github_release_downloader import AuthSession, get_latest_version, GitHubRepo, get_available_versions

FOLDER_SCRIPTS = os.path.join("C:\\ProgramData", "Prism2")
ARCHIVE_DIR = os.path.join(FOLDER_SCRIPTS, ".archive")
# DESTIN_DIR = os.path.join(FOLDER_SCRIPTS, "plugins")
DESTIN_DIR = os.path.join(FOLDER_SCRIPTS, "test_plugins")
DEST_VERSION_JSON_FILE = os.path.join(DESTIN_DIR, "version.json")


try:
    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
except:
    logging.info("BUG Path {} does't exist".format(ARCHIVE_DIR))

REPO = GitHubRepo("Vincannes", "SwanSidePipeline")
AuthSession.init(REPO)


def version_tuple(version):
    return tuple(map(int, version.split('.')))


def get_archive_versions():
    data = {}
    pattern = r'v(\d+\.\d+)'
    for archive in sorted(os.listdir(ARCHIVE_DIR)):
        match = re.search(pattern, archive)
        if not match:
            continue
        version = match.group(1)
        data[float(version)] = os.path.join(ARCHIVE_DIR, archive)
    return data


def get_version(version_json):
    f = open(version_json)
    data = json.load(f)
    return data.get("version", 1.0)


def zip_directory(directory):
    shutil.make_archive(directory, 'zip', DESTIN_DIR)
    return "{}.zip".format(directory)


def unzip_directory(zip_filepath, extract_to):
    if not os.path.isfile(zip_filepath):
        print(f"Le fichier {zip_filepath} n'existe pas.")
        return

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    try:
        shutil.unpack_archive(zip_filepath, extract_to)
        print(f"Fichiers extraits dans {extract_to}")

    except shutil.ReadError:
        print(f"Erreur lors de la lecture du fichier {zip_filepath}")


def create_save_file(version):
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y%m%d_%H_%M_%S") + "_v{}".format(str(version))
    formated_path = os.path.join(ARCHIVE_DIR, formatted_now)
    return formated_path


def clean_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_release_versions():
    return sorted([f"{i}" for i in get_available_versions(REPO)])


def get_release_url(release_version):
    request_url = f"https://api.github.com/repos/{REPO.user}/{REPO.repo}/releases/tags/{release_version}"
    data = json.loads(requests.get(request_url, headers=AuthSession.header).text)
    if 'message' in data:
        return
    name = data.get("name")
    zip_url = data.get("zipball_url")
    return name, zip_url


def download_release(name, zip_url):
    response = requests.get(
        zip_url, stream=True, headers=AuthSession.header
    )
    zip_file = os.path.join(FOLDER_SCRIPTS, "{}.zip".format(name))
    with open(zip_file, 'wb') as file:
        for i, data in enumerate(response.iter_content(2 ** 20, )):
            file.write(data)
    return zip_file


def copy_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            zip_file_path = os.path.join(root, f)
            if os.path.isfile(zip_file_path):
                dest = zip_file_path.replace(dir_path, FOLDER_SCRIPTS)
                if any([a in root for a in [".git", ".archive"]]):
                    continue
                if not os.path.exists(os.path.dirname(dest)):
                    os.makedirs(os.path.dirname(dest))
                if os.path.exists(dest):
                    os.remove(dest)
                shutil.copy(zip_file_path, dest)


def rollback():
    versions = get_archive_versions()
    latest_version = max(versions.keys())
    latest_path = versions[latest_version]
    clean_files(DESTIN_DIR)
    unzip_directory(latest_path, DESTIN_DIR)


def has_to_run():
    last_release_version = get_release_versions()[-1]
    dst_json_version = get_version(DEST_VERSION_JSON_FILE)
    return version_tuple(last_release_version) > version_tuple(dst_json_version)


def run():
    last_release_version = get_release_versions()[-1]
    dst_json_version = get_version(DEST_VERSION_JSON_FILE)

    save_dir_zip = create_save_file(dst_json_version)
    zip_directory(save_dir_zip)

    name, zip_realease_url = get_release_url(last_release_version)
    zip_file = download_release(name, zip_realease_url)
    # clean_files(DESTIN_DIR)
    unzip_directory(zip_file, FOLDER_SCRIPTS)

    for i in os.listdir(FOLDER_SCRIPTS):
        if i.startswith("Vincannes"):
            github_folder = os.path.join(FOLDER_SCRIPTS, i)
            copy_files(github_folder)
            os.remove(github_folder)
    shutil.copy(zip_file, os.path.join(ARCHIVE_DIR, os.path.basename(zip_file)))


if __name__ == "__main__":
    # run()
    from pprint import pprint
    # rollback()

    out_dir = "D:\\Desk\\projets\\test.zip"
    run()
