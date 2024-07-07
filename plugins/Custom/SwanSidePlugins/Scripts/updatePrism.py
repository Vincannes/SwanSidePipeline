import re
import os
import sys
import json
import shutil
import datetime

FOLDER_SCRIPTS = os.path.join("C:\\ProgramData", "Prism2")
ARCHIVE_DIR = os.path.join(FOLDER_SCRIPTS, ".archive")
# SOURCE_DIR = os.path.join(FOLDER_SCRIPTS, "plugins")
# DESTIN_DIR = os.path.join(FOLDER_SCRIPTS, "test")
SOURCE_DIR = os.path.join("Z:\Vincent", "Scripts_SWANSIDE")
DESTIN_DIR = os.path.join(FOLDER_SCRIPTS, "plugins")
DEST_VERSION_JSON_FILE = os.path.join(DESTIN_DIR, "version.json")
SOURC_VERSION_JSON_FILE = os.path.join(SOURCE_DIR, "version.json")

if not os.path.exists(ARCHIVE_DIR):
    os.mkdir(ARCHIVE_DIR)


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
    return float(data.get("version", 1.0))


def zip_directory(directory):
    shutil.make_archive(directory, 'zip', SOURCE_DIR)
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


def copy_files(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            shutil.copy2(
                os.path.join(root, f),
                os.path.join(directory, f)
            )


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


def copy_files():
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            full_file_name = os.path.join(root, f)
            if os.path.isfile(full_file_name):
                dest = full_file_name.replace(SOURCE_DIR, DESTIN_DIR)
                if any([a in root for a in [".git"]]):
                    print("la")
                    print(root)
                    continue
                if not os.path.exists(os.path.dirname(dest)):
                    os.makedirs(os.path.dirname(dest))
                shutil.copy(full_file_name, dest)


def rollback():
    versions = get_archive_versions()
    latest_version = max(versions.keys())
    latest_path = versions[latest_version]
    clean_files(DESTIN_DIR)
    unzip_directory(latest_path, DESTIN_DIR)


def has_to_run():
    src_json_version = get_version(SOURC_VERSION_JSON_FILE)
    dst_json_version = get_version(DEST_VERSION_JSON_FILE)
    return src_json_version < dst_json_version


def run():
    src_json_version = get_version(SOURC_VERSION_JSON_FILE)
    save_dir_zip = create_save_file(src_json_version)
    zip_file = zip_directory(save_dir_zip)
    clean_files(DESTIN_DIR)
    copy_files()


if __name__ == "__main__":
    # run()
    from pprint import pprint
    rollback()
