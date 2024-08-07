# Import Required Libraries
import requests
import json
import pandas as pd

# Required Constants
headers = {'User-Agent': 'fivepercentchange@fpc.com'}
DIR_NAME = 'sec_edgar_files/MSFT/'

def get_cik(ticker):
    url = f"https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=headers)
    data = response.json()

    for company in data.values():
        if company['ticker'] == ticker.upper():
            return company['cik_str']
    return None

def get_documents_data(cik):
    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    response = requests.get(url, headers=headers)
    data = response.json()

    return data

def download_document(cik, accession_number_without_dashes, primary_document):
    document_url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number_without_dashes}/{primary_document}'
    document_response = requests.get(document_url, headers=headers)

    print(document_url)
    return True

    document_name = f'{cik}_{accession_number_without_dashes}_{primary_document.replace("/", "_")}'
    
    if document_response.status_code == 200:
        with open(DIR_NAME + document_name, 'ab') as file:
            file.write(document_response.content)
        print(f'Document {document_name} downloaded successfully.')
    else:
        print(f'Failed to download document. Status code: {document_response.status_code}')

def write_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Execution Script:
def main():
    ticker = input("Enter the ticker symbol: ")
    cik = get_cik(ticker)
    
    if cik:
        print(f"CIK for {ticker}: {cik}")
        data = get_documents_data(cik)
        write_file(f'{ticker}_files.json', data)
    else:
        print(f"CIK not found for ticker: {ticker}")

if __name__ == "__main__":
    main()