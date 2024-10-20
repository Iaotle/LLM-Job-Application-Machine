#!/usr/bin/env python3
from __future__ import annotations
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
from utils import load_companies
from company import Company
from bs4 import ParserRejectedMarkup
import shutil
size = shutil.get_terminal_size()
class JobCrawler:
    def __init__(self, company: Company):
        self.company = company
        self.base_url = company.website
        self.visited = set()
        self.career_links = set()
        self.emails = set()
        self.external_links = set()
    def normalize_url(self, url):
            """Normalize the URL for comparison."""
            parsed_url = urlparse(url)
            # Remove www. from the domain
            domain = parsed_url.netloc.replace('www.', '')
            # Remove trailing slash
            domain = domain.rstrip('/')
            return f"{parsed_url.scheme}://{domain}"

    def crawl(self, url: str):
        if url in self.visited:
            return
        self.visited.add(url)
        # print(f"\033[AVisiting: {url}".ljust(size.columns))
        
        # newline = False
        # print(f"\033[A")

        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})  # Use a common user agent
            if response.status_code != 200:
                print(f"Failed to access: {url}".ljust(size.columns), response)
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')

            # Search for links
            links = soup.find_all('a', href=True)

            # Normalize the base URL for comparison
            normalized_base_url = self.normalize_url(self.base_url)
            

            for link in links:
                href = link['href']
                if href in self.visited:
                    continue
                # Skip files
                if href.endswith('.pdf') or href.endswith('.jpg') or href.endswith('.png') or href.endswith('.jpeg') \
                    or href.endswith('.gif') or href.endswith('.svg') or href.endswith('.webp') or href.endswith('.bmp') \
                    or href.endswith('.tiff') or href.endswith('.ico') or href.endswith('.mp4') or href.endswith('.avi') \
                    or href.endswith('.mov') or href.endswith('.mp3') or href.endswith('.wav') or href.endswith('.flac') \
                    or href.endswith('.ogg') or href.endswith('.doc') or href.endswith('.docx') or href.endswith('.xls') \
                    or href.endswith('.xlsx') or href.endswith('.ppt') or href.endswith('.pptx') or href.endswith('.odt') \
                    or href.endswith('.ods') or href.endswith('.odp') or href.endswith('.zip') or href.endswith('.rar') \
                    or href.endswith('.tar') or href.endswith('.gz') or href.endswith('.bz2') or href.endswith('.7z') \
                    or href.endswith('.dmg') or href.endswith('.exe') or href.endswith('.msi') or href.endswith('.apk') \
                    or href.endswith('.iso') or href.endswith('.img') or href.endswith('.csv') or href.endswith('.json') \
                    or href.endswith('.xml') or href.endswith('.sql') or href.endswith('.db') or href.endswith('.dbf'):
                    continue
                if href.startswith('javascript:') or href.startswith('#'):
                    continue
                if href.startswith('mailto:'):
                    # TODO: Handle email links, we can extract the email address for the company
                    if href.replace('mailto:', '') not in self.emails:
                        print(f"Found email: {href}".ljust(size.columns))
                        self.emails.add(href.replace('mailto:', ''))
                    continue
                if 'news' in href or 'blog' in href:
                    continue
                
                keywords = ['career', 'werken bij', 
                            'vacature', 'contact', 
                            'contact us', 'contact form', 
                            'sollicitatie', 'solliciteren',
                            'job',
                            'jobs', 'baan']
                # TODO: sometimes career links will be on a different website, see https://huhtamaki.wd3.myworkdayjobs.com/External (ID 01051894)
                #       Check for career-related keywords in the URL earlier?
                
                full_url = urljoin(url, href)  # Create full URL from base and link
                # Check for career-related keywords in link text or href
                if any(keyword in link.text.lower() for keyword in keywords) or \
                   any(keyword in href.lower() for keyword in keywords):
                    if full_url not in self.career_links:
                        print(f"Found career link: {full_url}".ljust(size.columns))
                        self.career_links.add(full_url)
                

                # Normalize full URL for comparison
                normalized_full_url = self.normalize_url(full_url)
                
                # Check if the full URL is part of the base URL
                if normalized_base_url != normalized_full_url:
                    self.external_links.add(href)
                    continue
                
                # Recur for new links
                self.crawl(full_url)
        except ParserRejectedMarkup as e:
            print(f"Assertion error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        

    def get_contact_form(self):
        # Logic to find a contact form if no career page is found
        print("No careers page found. Trying to find a contact form...")

    def output(self):
        print(f"External Links for {self.company.name}:")
        for link in self.external_links:
            print(link)
        
        # Print visited links
        print(f"Visited Links for {self.company.name}:")
        for link in self.visited:
            print(link)
        
        print(f"Career Links for {self.company.name}:")
        for link in self.career_links:
            print(link)
            
        print(f"Emails for {self.company.name}:")
        for email in self.emails:
            print(email)
        

import time
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument("--force", action='store_true', help="Force re-crawling of all companies.")
args = argparser.parse_args()

if __name__ == "__main__":
    force = args.force
    if force:
        print("\033[91mForcing re-crawling of all companies!!!\033[0m")
        time.sleep(3)
    companies = load_companies()
    career_links = dict()

    for company in companies:
        if not company.website:
            continue
        if company.careers_page and not force:
            print(f"Skipping {company.name}, already found careers page.")
            continue
        print(f"Crawling for company: {company.name}")
        crawler = JobCrawler(company)
        
        
        
        # load visited, external_links, emails from company if available
        if not force:
            if company.visited:
                crawler.visited = company.visited
            if company.external_links:
                crawler.external_links = company.external_links
            if company.emails:
                crawler.emails = company.emails
            if company.careers_page:
                crawler.career_links = company.careers_page
                continue

        crawler.crawl(company.website)
        # result = crawler.output()
        # print(result)
        if len(crawler.career_links) > 0:
            career_links[company.name] = crawler.career_links
            company.careers_page = list(crawler.career_links)
            company.visited = crawler.visited
            company.external_links = crawler.external_links
            company.emails = crawler.emails
            
            company.save_to_json()
    print(f"Found {len(career_links)} career links in total.")
    print(career_links)
    
# TODO: some issues with trailing / in URLs, e.g. https://www.ing.com/ vs https://www.ing.com