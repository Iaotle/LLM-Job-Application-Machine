#!/usr/bin/env python3
from __future__ import annotations

import os
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import time
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL of the webpage
url = "https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants"


def fetch_webpage(url: str) -> Optional[BeautifulSoup]:
    """
    Fetch and parse the webpage.
    :param url: The URL of the webpage to fetch.
    :return: Parsed BeautifulSoup object or None if fetch fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Ensure we notice bad responses
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        logging.error(f"Error fetching the webpage: {e}")
        return None


def parse_table(soup: BeautifulSoup) -> List[dict]:
    """
    Parse the table and extract organisation and KvK number.
    :param soup: BeautifulSoup object of the webpage.
    :return: List of dictionaries with organisation name and KvK number.
    """
    table_data = []
    table_body = soup.find('tbody')

    row: BeautifulSoup
    # Iterate over rows, skip the first row (header)
    for row in table_body.find_all('tr')[1:]:
        cells: List[BeautifulSoup] = row.find_all('td')
        if len(cells) == 2:
            organisation = cells[0].text.strip()
            kvk_number = cells[1].text.strip()
            table_data.append({"name": organisation, "kvk": kvk_number})

    return table_data


def save_company_data(company: dict) -> int:
    """
    Save the company information to a JSON file.
    Skip saving if the file already exists to avoid overwriting.
    :param company: Dictionary containing company 'name' and 'kvk'.
    :return: 1 if file saved, 0 otherwise.
    """
    directory = 'companies'
    os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist

    file_path = os.path.join(directory, f'{company["kvk"]}.json')
    
    if os.path.exists(file_path):
        logging.debug(f"File already exists, skipping: {file_path}")
        return 0

    try:
        with open(file_path, 'w') as f:
            f.write(f'{{"name": "{company["name"]}", "kvk": "{company["kvk"]}"}}')
        logging.debug(f'Saved: {company["name"]} (KvK: {company["kvk"]})')
    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        return 0
    return 1


def main():
    """Main function to orchestrate the fetching, parsing, and saving of data."""
    logging.info(f"Working...")
    beforeUrl = time.time()
    soup = fetch_webpage(url)
    if not soup:
        return
    afterUrl = time.time()

    companies = parse_table(soup)
    
    afterTableParse = time.time()
    saved = 0
    for company in companies:
        saved += save_company_data(company)

    afterSave = time.time()

    logging.info(f'Done! ({afterSave - beforeUrl:.2f}s) {len(companies)} records processed. {saved} files saved ')
    logging.debug(f'Webpage fetch: {afterUrl-beforeUrl:.2f}s')
    logging.debug(f'Table parse:   {afterTableParse-afterUrl:.2f}s')
    logging.debug(f'File I/O:      {afterSave-afterTableParse:.2f}s')


if __name__ == "__main__":
    main()
