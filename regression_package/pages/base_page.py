import re
import os
import json
from http.client import responses
from urllib.parse import urlparse
from playwright.sync_api import BrowserContext



def get_domain(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"

def get_slug_from_url(url, domain):
    if url == domain :
        return "Home_Page"
    else:
        parsed_url = urlparse(url)
        return parsed_url.path.lstrip('/')


class PageInstance:
    def __init__(self, context : BrowserContext, url):
        self.context = context
        self.page = context.new_page()
        self.url = url
        self.domain = get_domain(url)
        self.slug = get_slug_from_url(url, self.domain)
        self.response = None
        self.open_status = None
        self.open_url()



    def log_response(self, response):
        status = {}
        if response.url == self.url:
            status_code = response.status
            status_message = responses.get(status_code, "Unknown Status")
            self.response = f"{status_code} ({status_message})"
            status['message'] = status_message
            print(f"URL: {self.url}\nResponse: {status_code} {status_message}")


    def open_url(self):
        try:
            self.page.on("response", lambda response: self.log_response(response))
            self.page.goto(self.url)
            self.wait_for_page_load()
            self.open_status = "success"
        except Exception as e:
            print(f"Error open url '{self.url}': {e}")
            self.open_status = f"{e}"



    def terminate(self):
        self.page.close()


    @staticmethod
    def safe_get_attribute(element, attribute_name):
        try:
            value = element.get_attribute(attribute_name)

            # Encode the value to handle any special characters
            return value.encode('utf-8').decode('utf-8') if value else None

        except Exception as e:
            print(f"Error getting attribute '{attribute_name}': {e}")
            return None

    @staticmethod
    def safe_get_text_content(element):
        try:
            value = element.text_content()

            # Encode the value to handle any special characters
            return value.encode('utf-8').decode('utf-8') if value else None

        except Exception as e:
            print(f"Error getting text of '{element}': {e}")
            return None

    def wait_for_page_load(self):
        try:
            self.page.wait_for_load_state('networkidle')
        except Exception as e:
            return f"Network_idle error: {e}"

    def wait_for_time(self, timeout):
        try:
            self.page.wait_for_timeout(timeout)
        except Exception as e:
            return f"Time_out error: {e}"


    def accept_cookies(self, accept_cookie_selector):
        try:
            self.page.locator(accept_cookie_selector).click()
            return 'T'
        except Exception as e:
            return f"{e}"

    def close_email_signup_popup(self, close_email_popup_selector):
        try:
            self.page.locator(close_email_popup_selector).click()
            return 'T'
        except Exception as e:
            return f"{e}"

    def close_pop_ups(self):
        cookie = self.accept_cookies('button#onetrust-accept-btn-handler')
        mail_signup = self.close_email_signup_popup('button.vds-self_flex-end')

        if cookie == 'T':
            print('Accepted cookies')
        if mail_signup == 'T':
            print('Closed email signup popup')

        return cookie, mail_signup



    def get_page_type(self):
        try:
            locator = self.page.locator("head script")
            count = locator.count()
            cc_element = None

            for i in range(count):
                element = locator.nth(i)

                # Get the text content of the current script element
                sc_content = element.text_content()

                # Check if 'careClubConfig' is in the script content
                if "page_type" in sc_content:
                    cc_element = element
                    break

            if cc_element:
                script_content = cc_element.text_content()

                data_layer_main_str = script_content.split('window[\'dataLayer\'] = window[\'dataLayer\'] || [];')[1]
                data_layer_push = data_layer_main_str.split('window[\'dataLayer\'].push(')
                data_layer = None

                for i in range(len(data_layer_push)):
                    data_layer_str = data_layer_push[i].split(");")[0]
                    if "page_type" in data_layer_str:
                        data_layer = json.loads(data_layer_str)
                        break

                if data_layer:
                    page_data = data_layer.get("page_data", {})
                    page_type = page_data.get("page_type", None)
                    return page_type
                else:
                    print("\n\n Page_type not found\n\n")
                    return None
        except Exception as e:
            print(f"Error processing: {e}")