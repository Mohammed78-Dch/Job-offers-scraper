import json
import os
from scraping_all_jobs import extract_data  # Importer la fonction de scraping
# 📌 Définir le chemin du fichier JSON (peut être configuré via une variable d'environnement)
JSON_FILE_PATH = os.getenv("JSON_FILE_PATH", "/home/mohammed/airflow/dags/scripts/offres/offres_combinees.json")
def ensure_directory_exists(file_path):
    """Assure que le répertoire du fichier existe."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


# 📌 Fonction pour scraper et stocker les données en JSON
def insert_data_to_json(**kwargs):
    try:
        # Appeler la fonction de scraping
        scraped_data = extract_data()
        # Stocker les données dans un fichier JSON
        save_to_json(scraped_data, JSON_FILE_PATH)

    except ValueError as ve:
        print(f"❌ Erreur de validation des données : {ve}")
    except Exception as e:
        print(f"❌ Erreur lors du scraping ou de l'enregistrement des données : {e}")

def save_to_json(data, file_path):
    """Sauvegarde les données dans un fichier JSON."""
    try:
        ensure_directory_exists(file_path)  # Créer le dossier si nécessaire
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Données enregistrées dans {file_path}.")
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement des données dans le fichier JSON : {e}")
