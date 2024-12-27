
import random
import requests
import configparser
import xml.etree.ElementTree as ET
import pandas as pd

class GetUrls:
    def __init__(self, brand_name, method):
        self.config =  configparser.ConfigParser()
        self.config.read(f"config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.parse_method = method


    def get_urls_from_sitemap(self):
        # Fetch the sitemap XML
        sitemap_url = self.prod_domain_url + 'sitemap.xml'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(sitemap_url, headers=headers)

        if response.status_code == 200:
            # Parse the XML content
            root = ET.fromstring(response.content)

            # Extract URLs from <url><loc> tags
            urls_list = [url_elem.text for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
            return urls_list
        else:
            print(f"Failed to fetch sitemap: {response.status_code}")
            return []


    def get_urls_from_list(self):
        urls = self.config['urls_data']['urls_list'].split(',')
        urls = [url.strip() for url in urls]
        return urls


    def get_urls_from_csv(self):
        file_path = self.config['urls_data']['csv_file_path']
        try:
            df = pd.read_csv(file_path)
            if 'url' in df.columns:
                urls = df['url'].tolist()
                return urls
            else:
                raise ValueError("The CSV file does not contain a 'url' column.")

        except Exception as e:
            print(f"Error reading the CSV file: {e}")
            return []

    @staticmethod
    def sample_from_array(arr, min_items=3, max_items=5):
        # Ensure the sample size is within the array length
        sample_size = min(max_items, len(arr))

        # If there are enough elements, sample between min_items and sample_size
        if sample_size >= min_items:
            return random.sample(arr, random.randint(min_items, sample_size))
        else:
            print(f"Array contains fewer than {min_items} elements. Returning the full array.")
            return arr

    def get_random_urls_from_sitemap(self):
        full_url_list = self.get_urls_from_sitemap()
        url_list = self.sample_from_array(full_url_list)
        return url_list


    def get_urls_from_others(self):
        urls = None
        method = self.parse_method
        if method == '1':
            urls = self.get_urls_from_csv()
        elif method == '2':
            urls = self.get_urls_from_list()
        elif method == '3':
            urls = self.get_random_urls_from_sitemap()
        elif method == '0':
            urls = None
        return urls