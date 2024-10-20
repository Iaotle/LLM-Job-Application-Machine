#!/usr/bin/env python3
from __future__ import annotations
import multiprocessing
from multiprocessing.managers import ValueProxy
import time
from bs4 import BeautifulSoup
from googlesearch import search
from company import Company
from utils import load_companies
import requests
from multiprocessing import Pool, Manager, cpu_count

# Function to get the first Google search result
def get_first_google_result(query, retries=50, delay=1, lock=None, stop_flag: ValueProxy[int]=None):
    attempt = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'
    }
    
    while attempt < retries:
        if stop_flag.get() != multiprocessing.current_process().name and stop_flag.get():
            # Wait if another thread encountered a 429 and set the flag
            # print(f"Waiting for {stop_flag.get()}")
            time.sleep(delay)
            continue

        try:
            # Make the search request to Google (or any other search engine)
            response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
            
            # Check if 429 status code is returned
            if response.status_code == 429:
                with lock:
                    stop_flag.set(multiprocessing.current_process().name)  # Set the stop flag to notify all threads
                    print(f"429 Too Many Requests encountered. Retrying in {delay} seconds...")
                    
                time.sleep(delay)
                attempt += 1
                if delay >= 512:
                    delay += 60 # after 8.5 minutes, just add 1 minute
                else:
                    delay *= 2  # Exponential backoff
                continue
            else:
                if stop_flag.get() == multiprocessing.current_process().name:
                    with lock:
                        stop_flag.set(False)            
            # Parse the first result from the Google search page (using BeautifulSoup)
            soup = BeautifulSoup(response.text, 'html.parser')
            first_result = soup.find('a').get('href')
            return first_result
        
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return str(e)
    
    return "Failed to get result after several attempts."

# The function to fetch the company website and handle 429 status
def get_website(company: Company, lock, stop_flag: ValueProxy[int]):
    if not company.website:
        query = company.name
        first_result = get_first_google_result(query, lock=lock, stop_flag=stop_flag)
        print(f"{company.name}: {first_result}")
        company.website = first_result
        company.save_to_json()

# Load companies
companies = load_companies()

# Set up multiprocessing with a Manager for shared state
cores = cpu_count()
print(f"Number of cores: {cores}")

with Manager() as manager:
    # Create shared variables
    lock = manager.Lock()
    stop_flag = manager.Value(int, 0)  # Shared flag to stop other threads on 429
    
    # Create pool of workers
    pool = Pool(cores)
    
    # Pass lock and stop_flag to all processes
    pool.starmap(get_website, [(company, lock, stop_flag) for company in companies])
