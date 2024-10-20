#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from typing import List, Optional, Union

class Company:
    def __init__(self, name: str, kvk: str, website: Optional[str] = None,
                 careers_page: Optional[str] = None, address: Optional[str] = None,
                 sector: Optional[str] = None, file_path: Optional[str] = None, external_links: Optional[List[str]] = None,
                 emails: Optional[List[str]] = None, visited: Optional[List[str]] = None):
        self.name = name
        self.kvk = kvk
        self.website = website
        self.careers_page = careers_page
        self.address = address
        self.sector = sector
        self.file_path = file_path
        self.external_links = set()
        self.emails = set()
        self.visited = set()

    def __repr__(self):
        return f"Company(name={self.name}, kvk={self.kvk}, website={self.website}, " \
               f"careers_page={self.careers_page}, address={self.address}, sector={self.sector}, " \
               f"file_path={self.file_path})"
    def __str__(self) -> str:
        return f"{self.name} ({self.file_path})"

    @classmethod
    def from_json(cls, json_data: Union[str, dict]) -> 'Company':
        """Create a Company instance from a JSON string or dictionary."""
        path = None
        if isinstance(json_data, str):
            # If the input is a string, it could be a file path
            if os.path.isfile(json_data):
                path = json_data
                with open(json_data, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                # Otherwise, treat it as a JSON string
                data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            raise ValueError("Input must be a JSON string, file path, or dictionary.")

        # Validate mandatory fields
        if 'name' not in data or 'kvk' not in data:
            raise ValueError("Both 'name' and 'kvk' must be provided in the JSON data.")
        
        return cls(
            name=data['name'],
            kvk=data['kvk'],
            website=data.get('website'),
            careers_page=data.get('careers_page'),
            address=data.get('address'),
            sector=data.get('sector'),
            external_links=data.get('external_links'),
            emails=data.get('emails'),
            visited=data.get('visited'),
            file_path=path
        )
    
    def save_to_json(self, filepath: Optional[str] = None):
        """Save a Company instance to a JSON file."""
        if filepath is None:
            if self.file_path is None:
                raise ValueError("File path must be provided.")
            filepath = self.file_path
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'name': self.name,
                'kvk': self.kvk,
                'website': self.website,
                'careers_page': self.careers_page,
                'address': self.address,
                'sector': self.sector,
                'external_links': list(self.external_links),
                'emails': list(self.emails),
                'visited': list(self.visited)
            }, f, indent=4)

# # Example usage
# if __name__ == "__main__":
#     companies_list = load_companies('companies')
#     for company in companies_list:
#         print(company)
