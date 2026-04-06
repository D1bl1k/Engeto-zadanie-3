# 🗳️ Election Results Scraper (Czech Parliamentary Elections 2017)

This project is a Python script that scrapes official election results from the Czech Statistical Office website and exports them into a structured CSV file.

---

## 📌 Features

* Scrapes election results for a selected region (kraj)
* Extracts:

  * Municipality code and name
  * Registered voters
  * Issued envelopes
  * Valid votes
  * Votes for each political party
* Automatically creates CSV with dynamic columns (all parties included)
* Handles encoding issues (Czech diacritics)
* Works for any region by changing the input URL

---

## 🚀 Usage

Run the script from terminal:

```bash
python main.py "<URL>" output.csv
```

### Example:

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" olomouc.csv
```

---

## 🌍 How to get the URL

1. Go to:
   https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
2. Select a region (kraj)
3. Copy the URL from your browser
4. Use it as input for the script

---

## 📁 Output

The script generates a CSV file with structure like:

```
code;location;registered;envelopes;valid;ANO 2011;ODS;Piráti;...
```

* Each row = one municipality
* Each political party = separate column

---

## 🧰 Requirements

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## ⚙️ Technologies Used

* Python 3
* requests
* BeautifulSoup (bs4)
* CSV module

---

## ⚠️ Notes

* CSV uses `;` as delimiter (compatible with Excel/Google Sheets in CZ/SK)
* Encoding is set to `utf-8-sig` for proper diacritics
* For best results:

  * Open CSV in Google Sheets
  * or import into Excel via **Data → From Text/CSV**

---

## 📈 Possible Improvements

* Add progress bar
* Parallel downloading (faster scraping)
* Export to Excel (.xlsx)
* GUI or web interface
* Scrape all regions automatically

---

## 👨‍💻 Author

Created as a learning project for web scraping and data processing in Python.

---
