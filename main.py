"""
Scraper výsledků voleb do Poslanecké sněmovny 2017
Použití: python main.py <url_uzemniho_celku> <vystupni_soubor.csv>
"""

# built-in
import csv
import sys
from typing import List, Tuple, Dict

# third-party
import requests
from bs4 import BeautifulSoup


def validate_args() -> Tuple[str, str]:
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


def fetch_page(url: str) -> BeautifulSoup:
    """Stáhne stránku a vrátí BeautifulSoup objekt."""
    response = requests.get(url, timeout=10)
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, "html.parser")


def get_value(soup: BeautifulSoup, header: str) -> str:
    """Vrátí hodnotu z tabulky podle headeru."""
    tag = soup.find("td", {"headers": header})
    if not tag:
        return "0"

    return tag.get_text(strip=True).replace("\xa0", "").replace(" ", "")


def get_municipality_links(
    soup: BeautifulSoup, base_url: str
) -> List[Tuple[str, str, str]]:
    """Vrátí seznam obcí (code, name, url) ze všech tabulek."""
    municipalities: List[Tuple[str, str, str]] = []

    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

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


def parse_municipality(url: str) -> Dict[str, str]:
    """Vrátí výsledky jedné obce jako dictionary (finální robustní verze)."""
    soup = fetch_page(url)
    result: Dict[str, str] = {}

    result["Registered"] = get_value(soup, "sa2")
    result["Envelopes"] = get_value(soup, "sa3")
    result["Valid"] = get_value(soup, "sa6")

    tables = soup.find_all("table")

    for table in tables:
        for row in table.find_all("tr"):
            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            party_number = cols[0].get_text(strip=True)

            if not party_number.isdigit():
                continue

            party = cols[1].get_text(strip=True)

            votes = (
                cols[2]
                .get_text(strip=True)
                .replace("\xa0", "")
                .replace(" ", "")
            )

            if party and votes:
                result[party] = votes

    return result


def collect_all_results(
    municipalities: List[Tuple[str, str, str]]
) -> List[Dict[str, str]]:
    """Projde všechny obce a vrátí seznam výsledků."""
    all_rows: List[Dict[str, str]] = []

    for code, name, url in municipalities:
        print(f"Spracovávam: {name}")

        data = parse_municipality(url)

        row: Dict[str, str] = {
            "Code": code,
            "Location": name,
            "Registered": data.get("Registered", "0"),
            "Envelopes": data.get("Envelopes", "0"),
            "Valid": data.get("Valid", "0"),
        }

        for key, value in data.items():
            if key not in row:
                row[key] = value

        all_rows.append(row)

    return all_rows


def write_csv(rows: List[Dict[str, str]], output_file: str) -> None:
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

    print(f"\nHotovo → uložené do: {output_file}")


def main() -> None:
    """Hlavní vstup programu."""
    url, output_file = validate_args()

    soup = fetch_page(url)
    municipalities = get_municipality_links(soup, url)

    if not municipalities:
        print("Chyba: URL neobsahuje zoznam obcí (pravdepodobne ps311)")
        sys.exit(1)

    rows = collect_all_results(municipalities)
    write_csv(rows, output_file)


if __name__ == "__main__":
    main()