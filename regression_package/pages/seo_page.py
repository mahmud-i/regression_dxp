import os
from tkinter import image_names

from regression_dxp.regression_package.pages.base_page import PageInstance


class SEOInstance:
    def __init__(self, page_instance : PageInstance):
        self.instance = page_instance
        self.page = page_instance.page

    def get_title(self):
        try:
            return self.page.title()
        except Exception as e:
            return f"Page Title found error: {e}"

    def get_meta_description(self):
        try:
            element = self.page.query_selector("meta[name='description']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting meta_description '{self.instance.url}': {e}")
            return None

    def get_canonical_link(self):
        try:
            element = self.page.query_selector("link[rel='canonical']")
            return self.instance.safe_get_attribute(element, 'href') if element else None
        except Exception as e:
            print(f"Error getting canonical_link '{self.instance.url}': {e}")
            return None

    def get_og_title(self):
        try:
            selector = self.page.query_selector_all("meta[property='og:title']")
            element = selector[0] if len(selector) < 2 else selector[1]
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting og_title '{self.instance.url}': {e}")
            return None

    def get_og_description(self):
        try:
            element = self.page.query_selector("meta[property='og:description']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting og_description '{self.instance.url}': {e}")
            return None

    def get_og_type(self):
        try:
            element = self.page.query_selector("meta[name='og:type']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting og_type '{self.instance.url}': {e}")
            return None

    def get_og_site(self):
        try:
            element = self.page.query_selector("meta[name='og:site_name']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting og_site '{self.instance.url}': {e}")
            return None

    def get_og_url(self):
        try:
            element = self.page.query_selector("meta[name='og:url']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting og_url '{self.instance.url}': {e}")
            return None

    def get_og_image(self):
        try:
            selector = self.page.query_selector_all("meta[property='og:image']")
            if selector:
                image_path = None
                for i in range(len(selector)):
                    element = selector[i]
                    image_path = self.instance.safe_get_attribute(element, 'content') if element else None
                    if image_path.startswith('http://localhost'):
                        continue
                    if image_path.startswith('https://images'):
                        break

                image_name = os.path.basename(image_path) if image_path else None

                return image_name
            else:
                return None

        except Exception as e:
            print(f"Error getting og_image '{self.instance.url}': {e}")
            return None

    def get_twitter_title(self):
        try:
            selector = self.page.query_selector_all("meta[name='twitter:title']")
            element = selector[0] if len(selector) < 2 else selector[1]
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting twitter_title '{self.instance.url}': {e}")
            return None

    def get_twitter_description(self):
        try:
            element = self.page.query_selector("meta[name='twitter:description']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting twitter_description '{self.instance.url}': {e}")
            return None

    def get_twitter_card(self):
        try:
            element = self.page.query_selector("meta[name='twitter:card']")
            return self.instance.safe_get_attribute(element, 'content') if element else None
        except Exception as e:
            print(f"Error getting twitter_card '{self.instance.url}': {e}")
            return None

    def get_twitter_image(self):
        try:
            selector = self.page.query_selector_all("meta[name='twitter:image']")

            if selector:
                image_path = None
                for i in range(len(selector)):
                    element = selector[i]
                    image_path = self.instance.safe_get_attribute(element, 'content') if element else None
                    if image_path.startswith('http://localhost'):
                        continue
                    if image_path.startswith('https://images'):
                        break

                image_name = os.path.basename(image_path) if image_path else None

                return image_name

            else:
                return None

        except Exception as e:
            print(f"Error getting twitter_image '{self.instance.url}': {e}")
            return None

    def get_h1(self):
        try:
            parent_locator = self.page.locator("main")
            selector = parent_locator.locator("h1")
            if selector.count() > 1 :
                return "Multiple items"
            else:
                element = selector

            return self.instance.safe_get_text_content(element) if element else None

        except Exception as e:
            print(f"Error getting h1 '{self.instance.url}': {e}")
            return None
