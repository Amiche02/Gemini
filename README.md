# Gemini: OCR et LLM pour l'Extraction de Tableaux à partir d'Images

## Description

Gemini est un outil innovant qui combine la reconnaissance optique de caractères (OCR) et un modèle de langage avancé (LLM) pour extraire et interpréter des tableaux à partir d'images. Ce projet vise à fournir une solution précise et efficace pour convertir des tableaux d'images en données structurées utilisables.

## Fonctionnalités

- **OCR avancé :** Utilisation de Tesseract pour la reconnaissance de texte dans les images.
- **Modèle de langage :** Intégration du modèle Gemini pour analyser et structurer les données extraites sous forme de tableaux.
- **Précision élevée :** Algorithmes optimisés pour améliorer la précision et la vitesse d'extraction.
- **Polyvalence :** Capacité à traiter divers types d'images contenant des tableaux.
- **Documentation complète :** Guide d'utilisation et documentation technique détaillée.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.7 ou plus récent
- Tesseract OCR
- Bibliothèques Python nécessaires (voir `requirements.txt`)

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/Amiche02/Gemini.git
    cd Gemini
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Assurez-vous que Tesseract OCR est installé et configuré correctement sur votre système.

## Utilisation

1. Placez les images contenant des tableaux dans le répertoire `input_images`.
2. Exécutez le script principal :
    ```bash
    python main.py
    ```
3. Les résultats seront sauvegardés dans le répertoire `output_tables` sous forme de fichiers CSV.

## Structure du Projet

- `input_images/` : Répertoire pour les images à traiter.
- `output_tables/` : Répertoire pour les fichiers CSV générés.
- `main.py` : Script principal pour l'extraction des tableaux.
- `requirements.txt` : Liste des dépendances Python.
- `README.md` : Ce fichier README.

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes pour contribuer :

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/ma-fonctionnalité`)
3. Committez vos changements (`git commit -am 'Ajoutez une fonctionnalité'`)
4. Poussez votre branche (`git push origin feature/ma-fonctionnalité`)
5. Ouvrez une Pull Request

## Auteurs

- **Amiche02** - Créateur et développeur principal

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Merci aux développeurs de Tesseract OCR et du modèle Gemini pour leurs outils exceptionnels.
- Remerciements à la communauté open-source pour leur soutien et leurs contributions.
