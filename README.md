🗳️ Czech Election Results Scraper (2017)

Python script for scraping official parliamentary election results from the Czech Statistical Office and exporting them into a structured CSV file.

📌 Features
Scrapes election results for a selected region (kraj)
Extracts:

Municipality code and name
Registered voters
Issued envelopes
Valid votes
Votes for each political party
Automatically generates CSV with dynamic columns (all parties included)
Handles Czech diacritics correctly
Works for any region by changing the input URL

🚀 Installation
Clone the repository and install dependencies:

git clone <your-repo-url>
cd <your-repo-name>
pip install -r requirements.txt

Or install manually:

pip install requests beautifulsoup4

▶️ Usage
Run the script from terminal:

python main.py "<URL>" output.csv

Example:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6206" Vyskov.csv

🌍 How to Get the Input URL
Go to:
https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Select a region (kraj)
Copy the URL from your browser
Use it as input for the script

🧰 Technologies Used
Python 3
requests
BeautifulSoup (bs4)
CSV module

⚙️ Notes
CSV uses ; as delimiter (Excel/Google Sheets friendly in CZ/SK)
Encoding is set to utf-8-sig for correct diacritics
Recommended:
Open in Google Sheets
Or import into Excel via Data → From Text/CSV

⚠️ Disclaimer
This project is intended for educational purposes only.
All data is scraped from publicly available sources provided by the Czech Statistical Office.

📈 Possible Improvements
Add progress bar
Parallel downloading (faster scraping)
Export to Excel (.xlsx)
GUI or web interface
Scrape all regions automatically
Add CLI arguments (--help)

👨‍💻 Author
Created as a learning project focused on:
Web scraping
Data processing
Working with real-world datasets
