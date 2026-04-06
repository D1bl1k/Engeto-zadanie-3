"""
Scraper výsledků voleb do Poslanecké sněmovny 2017
Použití: python main.py <url_uzemniho_celku> <vystupni_soubor.csv>
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup


# ── Validace argumentů ────────────────────────────────────────────────────────

def validate_args():
    """Zkontroluje vstupní argumenty."""
    if len(sys.argv) != 3:
        print("Použitie: python main.py <URL> <output.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not url.startswith("http"):
        print("Chyba: prvý argument musí byť URL")
        sys.exit(1)

    if not output_file.endswith(".csv"):
        print("Chyba: druhý argument musí byť .csv súbor")
        sys.exit(1)

    return url, output_file


# ── Stahování stránek ─────────────────────────────────────────────────────────

def fetch_page(url: str) -> BeautifulSoup:
    """Stáhne stránku a vrátí BeautifulSoup objekt."""
    response = requests.get(url, timeout=10)
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


# ── Parsování seznamu obcí ────────────────────────────────────────────────────

def get_municipality_links(soup: BeautifulSoup, base_url: str):
    """Vrátí seznam obcí (code, name, url)."""
    municipalities = []

    table = soup.find("table", {"id": "ps32_t1"})
    if table is None:
        table = soup.find("table")

    rows = table.find_all("tr")[2:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        code = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)

        link_tag = cols[0].find("a")
        if not link_tag:
            continue

        href = link_tag["href"]
        base = base_url.rsplit("/", 1)[0]
        full_url = f"{base}/{href.lstrip('./')}"

        municipalities.append((code, name, full_url))

    return municipalities


# ── Parsování jedné obce ──────────────────────────────────────────────────────

def parse_municipality(url: str):
    """Vrátí výsledky jedné obce jako dictionary."""
    soup = fetch_page(url)
    result = {}

    def get_value(header: str) -> str:
        tag = soup.find("td", {"headers": header})
        if not tag:
            return "0"

        return (
            tag.get_text(strip=True)
            .replace("\xa0", "")
            .replace(" ", "")
        )

    result["registered"] = get_value("sa2")
    result["envelopes"] = get_value("sa3")
    result["valid"] = get_value("sa6")

    # ── Strany ────────────────────────────────────────────────────────────────
    party_tables = soup.select("table#ps311_t2")

    if not party_tables:
        party_tables = soup.find_all("table")

    for table in party_tables:
        for row in table.find_all("tr"):
            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            party = cols[1].get_text(strip=True)
            votes = (
                cols[2]
                .get_text(strip=True)
                .replace("\xa0", "")
                .replace(" ", "")
            )

            if party and votes.isdigit():
                result[party] = votes

    return result


# ── Sběr všech dat ────────────────────────────────────────────────────────────

def collect_all_results(municipalities):
    """Projde všechny obce a vrátí seznam výsledků."""
    all_rows = []

    for code, name, url in municipalities:
        print(f"Spracovávam: {name}")

        data = parse_municipality(url)

        row = {
            "code": code,
            "location": name,
            "registered": data.get("registered", "0"),
            "envelopes": data.get("envelopes", "0"),
            "valid": data.get("valid", "0"),
        }

        for key, value in data.items():
            if key not in row:
                row[key] = value

        all_rows.append(row)

    return all_rows


# ── CSV export ────────────────────────────────────────────────────────────────

def write_csv(rows, output_file):
    """Zapíše data do CSV."""
    if not rows:
        print("Žiadne dáta.")
        return

    all_keys = list(rows[0].keys())

    for row in rows:
        for key in row:
            if key not in all_keys:
                all_keys.append(key)

    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=all_keys,
            delimiter=";"
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    print(f"\n✅ Hotovo → uložené do: {output_file}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    """Hlavní vstup programu."""
    url, output_file = validate_args()

    soup = fetch_page(url)
    municipalities = get_municipality_links(soup, url)

    rows = collect_all_results(municipalities)

    write_csv(rows, output_file)


if __name__ == "__main__":
    main()