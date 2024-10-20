#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import List, Optional
from company import Company


def load_companies(directory: Optional[str] = None) -> List[Company]:
    companies = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            companies.append(Company.from_json(filepath))        
    return companies
