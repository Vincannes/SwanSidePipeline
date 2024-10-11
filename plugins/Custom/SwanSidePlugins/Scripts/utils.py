#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import subprocess


def is_mount_accessible(mount_point):
    return os.path.ismount(mount_point)


def is_nas_reachable(ip_address):
    try:
        # On utilise le ping pour vérifier la connectivité réseau
        response = subprocess.run(['ping', '-n', '1', ip_address], stdout=subprocess.PIPE)
        return response.returncode == 0  # Si returncode est 0, la connexion a réussi
    except Exception as e:
        print(f"Erreur : {e}")
        return False
