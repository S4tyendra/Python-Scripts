import os
import re
import requests
from PIL import Image
from bs4 import BeautifulSoup

class ImageScraper:
    def __init__(self):
        self.home = os.getcwd()
    
    @staticmethod
    def is_valid_url(url):
        return url.startswith('http') or url.startswith('https')

    def grab_all_image_links(self, url):
        valid_links = []
        try:
            url_protocol = url.split('/')[0]
            url_html = requests.get(url).text
            image_urls = re.findall(r'((http\:|https\:)?\/\/[^"\' ]*?\.(png|jpg))', url_html, flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
            for image in image_urls:
                image_url = image[0]
                if not image_url.startswith(url_protocol):
                    image_url = url_protocol + image_url
                valid_links.append(image_url)
            print('Done grabbing image links')
        except Exception as grab_error:
            print('An error occurred while getting image links')
            print(grab_error)
        return valid_links

    @staticmethod
    def extract_image_name(url):
        return url.split('/')[-1]

    @staticmethod
    def extract_site_name(url):
        return url.split('/')[2]
    
    def save_images(self, image_links, site_name):
        for link in image_links:
            try:
                raw_image = requests.get(link, stream=True).raw
                img = Image.open(raw_image)
                image_name = self.extract_image_name(link)
                img.save(os.path.join(site_name, image_name))
                print(f'Saved: {image_name}')
            except Exception as save_error:
                print(f'Error while saving {link}')
                print(save_error)

    def grab_all_links(self, url):
        links = [url]
        link_html = requests.get(url).text
        all_links = BeautifulSoup(link_html, 'html.parser').findAll('a')
        for link in all_links:
            href = link.get('href')
            if href and self.is_valid_url(href):
                links.append(href)
        return links

    def download_images(self):
        url = input('Enter URL with images: ')
        try:
            if not self.is_valid_url(url):
                print('Invalid URL format')
                return

            sitename = self.extract_site_name(url)
            print(f'Extracting from {sitename} ...')
            os.makedirs(sitename, exist_ok=True)
            print('\nShould we scan the entire site or just the home page?')
            option = int(input('1. Entire site\n2. Just this page\nOption: '))
            if option == 1:
                all_available_links = set(self.grab_all_links(url))
            else:
                all_available_links = [url]
            self.save_images(self.grab_all_image_links(url), sitename)

            for link in all_available_links:
                try:                        
                    self.save_images(self.grab_all_image_links(link), sitename)
                except:
                    continue

        except Exception as error:
            print('An error occurred while scraping')
            print(error)

        finally:
            print('Scraping finished')
            os.chdir(self.home)

scraper = ImageScraper()
scraper.download_images()
