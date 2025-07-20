# 💼 Job Offers Scraper – Job Market Intelligence Platform

This project aims to **automate the extraction of job offers** from multiple employment websites, store the data in a structured format, and provide a user-friendly **web interface** to consult or apply for jobs.

📅 **Duration:** March 2025 – April 2025  

---

## 📌 Objective

- Scrape job offers from popular Moroccan websites
- Automate the scraping workflow using Apache Airflow
- Store the offers in a structured PostgreSQL database
- Create a web application for users to consult or apply to job offers

---

## 🌐 Target Websites

The scraper targets job listing platforms such as:
- Rekrute
- Emploi.ma
- Indeed Maroc (optional)
- Others (configurable)

---

## 🧠 Architecture Overview

The project is divided into **4 main components**:

1. **Web Scraping**  
   - Developed using `Scrapy`
   - Extract job title, location, contract type, company, description, and date

2. **Automation Pipeline**  
   - Managed with `Apache Airflow`
   - Scheduled scraping tasks with logging and retries

3. **Database Layer**  
   - Jobs stored in `PostgreSQL`
   - Ensures de-duplication and structured storage

4. **Web Interface**  
   - Developed using `Flask`
   - Allows users to search, filter, and apply to job offers

---

## 🛠️ Technologies

| Stack        | Tools Used                            |
|--------------|----------------------------------------|
| Language     | Python                                 |
| Scraping     | Scrapy                                 |
| Automation   | Apache Airflow                         |
| Backend      | Flask                                  |
| Database     | PostgreSQL                             |
| Deployment   | Docker (optional)                      |

---

## 🧪 Features

- ✅ Real-time job offer extraction
- ✅ Scheduled scraping pipelines
- ✅ RESTful API for accessing jobs
- ✅ Simple and responsive user interface
- ✅ Export functionality (CSV/JSON)

---

## 🧰 Installation

### 1. Clone the project
```bash
git clone https://github.com/Mohammed78-Dch/Job-offers-scraper.git
cd Job-offers-scraper
```
---

## 📈 Results

- Collected over **thousands of job offers** from multiple Moroccan platforms  
- Reduced search effort and centralized access to job data  
- Provided users with a smooth job browsing and filtering experience  

---

## 📬 Contact

For inquiries or suggestions:

**Mohammed Dechraoui**  
📧 [mdechraoui@insea.ac.ma](mailto:mdechraoui@insea.ac.ma)  
🔗 [LinkedIn – Mohammed Dechraoui](https://www.linkedin.com/in/mohammed-dechraoui)

