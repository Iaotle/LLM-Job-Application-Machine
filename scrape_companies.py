import os
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table body containing the information
    table_body = soup.find('tbody')
    
    if table_body:
        # Iterate over the rows of the table body
        for row in table_body.find_all('tr')[1:]: # Skip the first row (header)
            # Find all table cells in the current row
            cells = row.find_all('td')
            
            # If the row contains 2 cells (organisation name and KvK number)
            if len(cells) == 2:
                organisation = cells[0].text.strip()
                kvk_number = cells[1].text.strip()
                
                # Print or store the parsed information
                print(f"Organisation: {organisation}, KvK Number: {kvk_number}")
                
                # if not dir mkdir:
                if not os.path.exists('companies'):
                    os.makedirs('companies')
                # put the info in companies/kvk_number.json
                with open(f'companies/{kvk_number}.json', 'w') as f:
                    f.write(f'{{"name": "{organisation}", "kvk": "{kvk_number}"}}')
    else:
        print("Table body not found!")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
