import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configuration
IMAGE_FOLDER = "/home/mohammed/airflow/dags/scripts/offres/images"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Créer le dossier pour les images
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def clean_text(text):
    """Nettoyer le texte en supprimant les caractères spéciaux et les espaces inutiles."""
    if text == "N/A" or not text:
        return "Non spécifié"
    text = re.sub(r'[\r\n\t]+', ' ', text)  # Remplacer les caractères spéciaux par un espace
    text = re.sub(r'\s+', ' ', text).strip()  # Supprimer les espaces multiples
    return text

def download_image(image_url, job_id, base_url=None):
    """Télécharger une image et la sauvegarder localement."""
    try:
        if not image_url or image_url == "N/A":
            return "Image non disponible"
        # Assurez-vous que l'URL est absolue
        if base_url and image_url.startswith('/'):
            image_url = urljoin(base_url, image_url)
        # Obtenir l'extension du fichier
        ext = os.path.splitext(image_url)[1] or ".png"
        filename = f"{job_id}{ext}" if ext.lower() in ('.jpg', '.jpeg', '.png', '.gif') else f"{job_id}.png"
        image_path = os.path.join(IMAGE_FOLDER, filename)
        # Télécharger l'image
        response = requests.get(image_url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return image_path
        print(f"Échec du téléchargement de l'image ({response.status_code})")
        return "Image non disponible"
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image: {e}")
        return "Image non disponible"

def extract_from_rekrute_com():
    """Extraire les offres d'emploi depuis rekrute.com."""
    all_offers = []
    base_url = "https://www.rekrute.com/offres.html?s=1&p={}&o=1"
    try:
        # Récupérer la première page pour déterminer le nombre total de pages
        response = requests.get(base_url.format(1), headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"Erreur de requête pour la première page (rekrute.com): {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extraire le nombre total de pages
        pagination_span = soup.select_one('div.section span.jobs')
        total_pages = int(re.search(r'sur\s*(\d+)', pagination_span.get_text(strip=True)).group(1)) if pagination_span else 1
        print(f"(rekrute.com) Nombre total de pages : {total_pages}")
        # Pour Extraire les offres d'emploi de toutes les pages utiliser /total_pages/  et pour spécifier uniquement pour les 2 pages premieres utiliser /2+1/
        for page in range(1, 2 + 1):
            print(f"(rekrute.com) Traitement de la page {page}...")
            url = base_url.format(page)
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code != 200:
                print(f"(rekrute.com) Erreur de requête pour la page {page}: {response.status_code}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            for job_element in soup.find_all('li', class_='post-id'):
                try:
                    job_id = job_element.get('id', 'unknown')
                    title_element = job_element.select_one('.titreJob')
                    title = title_element.text.strip() if title_element else "Non spécifié"
                    job_url = title_element['href'] if title_element else "Non spécifié"
                    company = job_element.select_one('img.photo')['alt'].strip() if job_element.select_one('img.photo') else "Non spécifié"
                    logo_url = job_element.select_one('img.photo')['src'] if job_element.select_one('img.photo') else "N/A"
                    image_path = download_image(logo_url, job_id, base_url="https://www.rekrute.com")
                    location = "Non spécifié"
                    if title and "|" in title:
                        parts = title.split("|")
                        title = parts[0].strip()
                        location = parts[1].strip() if len(parts) > 1 else "Non spécifié"
                    date_element = job_element.select_one('.date')
                    pub_start = re.search(r'Publication : du\s+(\d{2}/\d{2}/\d{4})', date_element.text.strip()).group(1) if date_element else "Non spécifié"
                    ul_element = job_element.select_one('div.info ul')
                    competences_cles = niveau_experience = niveau_etudes = contrat = "Non spécifié"
                    if ul_element:
                        li_elements = ul_element.find_all('li')
                        for li in li_elements:
                            li_text = li.text.strip()
                            if "Fonction :" in li_text:
                                competences_cles = li_text.replace('Fonction :', '').strip()
                            elif "Expérience requise :" in li_text:
                                niveau_experience = li_text.replace('Expérience requise :', '').strip()
                            elif "Niveau d'étude demandé :" in li_text:
                                niveau_etudes = li_text.replace("Niveau d'étude demandé :", '').strip()
                            elif "Type de contrat proposé :" in li_text:
                                contrat = li_text.replace('Type de contrat proposé :', '').strip()
                    all_offers.append({
                        "Source": "rekrute.com",
                        "Poste": clean_text(title),
                        "Entreprise": clean_text(company),
                        "URL de l'offre": job_url,
                        "Chemin de l'image": image_path,
                        "Niveau d'études": clean_text(niveau_etudes),
                        "Niveau d'expérience": clean_text(niveau_experience),
                        "Contrat": clean_text(contrat),
                        "Région": clean_text(location),
                        "Compétences clés": clean_text(competences_cles),
                        "Date de publication": clean_text(pub_start)
                    })
                except Exception as e:
                    print(f"(rekrute.com) Erreur lors du traitement d'une offre : {e}")
                    continue
            time.sleep(2)  # Délai entre les pages
    except Exception as e:
        print(f"(rekrute.com) Erreur globale : {e}")
    return all_offers

def extract_from_marocemploi_net():
    """Extraire les offres d'emploi depuis marocemploi.net."""
    all_offers = []
    base_url = "https://marocemploi.net/offre/?ajax_filter=true&job_page={}"
    max_pages = 2  # Limiter à 2 pages pour cet exemple
    try:
        for page_num in range(1, max_pages + 1):
            url = base_url.format(page_num)
            print(f"(marocemploi.net) Traitement de la page {page_num}...")
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"(marocemploi.net) Erreur de requête pour la page {page_num}: {response.status_code}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            job_elements = soup.find_all('li', class_='jobsearch-column-12')
            if not job_elements:
                print("(marocemploi.net) Aucune offre trouvée sur cette page.")
                break
            for job_element in job_elements:
                try:
                    # ID du poste
                    job_id = job_element.find('h2', class_='jobsearch-pst-title')['data-job-id']
                    # Titre et URL du poste
                    title_element = job_element.find('h2', class_='jobsearch-pst-title').find('a')
                    title = title_element.text.strip() if title_element else "Non spécifié"
                    job_url = title_element['href'] if title_element else "Non spécifié"
                    # Entreprise
                    company_element = job_element.find('li', class_='job-company-name').find('a')
                    company = company_element.text.strip() if company_element else "Non spécifié"
                    # Localisation
                    location_element = job_element.find('i', class_='jobsearch-icon jobsearch-maps-and-flags').parent
                    location = location_element.text.strip() if location_element else "Non spécifié"
                    # Date de publication
                    date_element = job_element.find('i', class_='jobsearch-icon jobsearch-calendar').parent
                    date_publication = date_element.text.strip() if date_element else "Non spécifié"
                    # Type de contrat
                    contract_element = job_element.find('a', class_='jobsearch-option-btn')
                    contract = contract_element.text.strip() if contract_element else "Non spécifié"
                    # Secteur d'activité
                    sector_element = job_element.find('i', class_='jobsearch-icon jobsearch-filter-tool-black-shape').parent.find('a')
                    sector = sector_element.text.strip() if sector_element else "Non spécifié"
                    # Image
                    image_element = job_element.find('img')
                    image_url = image_element['src'] if image_element and 'src' in image_element.attrs else "N/A"
                    image_path = download_image(image_url, job_id)
                    # Retourner les données nettoyées
                    all_offers.append({
                        "Source": "marocemploi.net",
                        "Poste": clean_text(title),
                        "Entreprise": clean_text(company),
                        "URL de l'offre": job_url,
                        "Chemin de l'image": image_path,
                        "Niveau d'études": "Non spécifié",  # Non disponible dans le HTML fourni
                        "Niveau d'expérience": "Non spécifié",  # Non disponible dans le HTML fourni
                        "Contrat": clean_text(contract),
                        "Région": clean_text(location),
                        "Compétences clés": clean_text(sector),  # Utilisé comme proxy pour les compétences
                        "Date de publication": clean_text(date_publication)
                    })
                except Exception as e:
                    print(f"(marocemploi.net) Erreur lors du traitement d'une offre : {e}")
                    continue
            time.sleep(2)  # Délai entre les pages
    except Exception as e:
        print(f"(marocemploi.net) Erreur globale : {e}")
    return all_offers

def extract_data():
    """Extraire les données des deux sites et les combiner."""
    all_offers = []
    print("Extraction des données depuis rekrute.com...")
    all_offers.extend(extract_from_rekrute_com())
    print("Extraction des données depuis marocemploi.net...")
    all_offers.extend(extract_from_marocemploi_net())
    return all_offers

