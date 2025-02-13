#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import subprocess
import configparser


def is_mount_accessible(mount_point):
    return os.path.ismount(mount_point)


def is_nas_reachable(ip_address):
    try:
        # On utilise le ping pour verifier la connectivite reseau
        response = subprocess.run(['ping', '-n', '1', ip_address], stdout=subprocess.PIPE)
        return response.returncode == 0  # Si returncode est 0, la connexion a réussi
    except Exception as e:
        print(f"Erreur : {e}")
        return False


def readConfig(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def writeConfig(path, data):
    config = configparser.ConfigParser()

    for section, values in data.items():
        config[section] = values

    with open(path, 'w') as configfile:
        config.write(configfile)


def generate_pattern(file_list):
    first_file = file_list[0]
    dir_path, file_name = os.path.split(first_file)
    base_name, ext = os.path.splitext(file_name)
    parts = base_name.split('.')
    frame_number = parts[-1]
    base_pattern = '.'.join(parts[:-1])

    pattern = os.path.join(dir_path, f"{base_pattern}.%04d.{ext[1:]}")
    return pattern