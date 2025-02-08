Voici une documentation complète pour l'installation d'un dossier .rar situé sur un NAS au chemin Z://install. Cette procédure inclut la décompression et le remplacement des fichiers spécifiques.

# Documentation d'installation - Dossier Prism2

## Pré-requis :
- Accès au NAS avec le chemin Z://install

## 1. Accéder au fichier .rar sur le NAS
1. Connectez-vous au NAS en accédant à Z://install via l'Explorateur de fichiers Windows.
2. Recupérerez le fichier .rar qui contient les fichiers nécessaires (Prism2.rar).

## 2. Décompression du fichier .rar
1. Copiez le fichier .rar depuis le NAS à un emplacement local, par exemple sur le bureau ou dans un autre dossier temporaire.
2. Décompressez le fichier .rar

## 3. Remplacement du dossier Prism2
1. Une fois décompressé, vous verrez un dossier nommé Prism2.

2. Ouvrez l'Explorateur de fichiers et accédez à C:\ProgramData\Prism2 (note : ProgramData est un dossier caché par défaut, il peut être nécessaire de l’afficher en activant l'option "Afficher les éléments cachés" dans l'onglet "Affichage" de l'Explorateur).

3. Copiez le dossier décompressé Prism2 et remplacez l'ancien dossier présent à cet emplacement :

    - Clic droit sur le dossier décompressé, puis sélectionnez Copier.
    - Naviguez jusqu'à C:\ProgramData\Prism2, clic droit et sélectionnez Coller, puis cliquez sur Remplacer les fichiers dans la destination si une fenêtre de confirmation s'affiche.

## 4. Remplacement des fichiers Prism.json et PluginPath.json (si première installation)

### 4.1. Si c'est la première installation, vous devez également copier deux fichiers supplémentaires :

- Prism.json
- PluginPath.json
Ces fichiers sont situés dans C:\ProgramData\Prism2.

### 4.2 Copiez ces fichiers dans le répertoire utilisateur suivant : C:\Users\User\Documents\Prism2.

- Allez dans C:\ProgramData\Prism2, sélectionnez les fichiers Prism.json et PluginPath.json, faites un clic droit et sélectionnez Copier.

- Allez ensuite dans C:\Users\User\Documents\Prism2 et collez les fichiers dans ce dossier. S'il existe déjà des fichiers avec le même nom, remplacez-les.

## Vérifications
Assurez-vous que tous les fichiers ont bien été remplacés et qu'il n'y a pas eu d'erreurs lors de la copie.

Redémarrez le programme Prism2 pour que les modifications prennent effet.



## Notes :
Si vous rencontrez des erreurs de permission lors de la copie des fichiers, vérifiez que vous disposez bien des droits administratifs.

Assurez-vous d’avoir un logiciel de décompression à jour pour éviter tout problème lors de l'extraction du fichier .rar.
Cela vous guide à travers l'installation en remplaçant les fichiers nécessaires dans les emplacements appropriés.
