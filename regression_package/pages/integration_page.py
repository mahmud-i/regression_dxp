import os
from regression_package.pages.base_page import PageInstance
from regression_package.utils.extract_pages_json import extract_json_object

class IntegrationInstance:
    def __init__(self, page_instance : PageInstance):
        self.instance = page_instance
        self.context = page_instance.context
        self.page = page_instance.page


    def get_ot_id(self):
        try:
            locator= self.page.locator('script#otHelmet')
            if locator.count() > 0:
                ot_id = locator.get_attribute('data-domain-script')
                return ot_id
            else:
                return None
        except Exception as e:
            return f"error finding{e}"


    def get_bv_env_data(self):
        try:
            locator= self.page.locator('script#bvHelmet')
            if locator.count() > 0:
                src = locator.get_attribute('src')
                parts = src.split('/')
                bv_env_data = {
                    'bv_brand' : parts[4],
                    'bv_env' : parts[6]
                }
                return bv_env_data
            else:
                return None

        except Exception as e:
            return {"error": f"error finding{e}"}


    def get_cc_data(self):
        try:
            locator= self.page.locator("script")
            count = locator.count()
            cc_element = None

            for i in range(count):
                element = locator.nth(i)

                # Get the text content of the current script element
                sc_content = element.text_content()

                # Check if 'careClubConfig' is in the script content
                if "careClubConfig" in sc_content:
                    cc_element = element
                    break

            if cc_element:
                script_content = cc_element.text_content()
                cc_data_raw = extract_json_object(script_content,'careClubConfig')

                if cc_data_raw :
                    cc_data = {
                        'api_url' : cc_data_raw.get("apiUrl"),
                        'cc_brand' : cc_data_raw.get("brandName"),
                        'secret_key' : cc_data_raw.get("secretKey")
                    }
                    return cc_data
                else:
                    print()
                    return None

        except Exception as e:
            return {"error": f"error finding: {e}"}


    def get_ucu_data(self, url, slug, text):
        try:
            if slug == "Home":
                slug = ""
            url = url+slug
            page_1 = self.context.new_page()
            page_1.goto(url)
            page_1.wait_for_timeout(1000)
            locator = page_1.locator('a', has_text= text)

            if  locator:
                if locator.count() > 1:
                    element = locator.nth(1)
                else:
                    element = locator.nth(0)

                ucu_link = element.get_attribute('href')
                page_1.close()
                return ucu_link

            else:
                page_1.close()
                return None
        except Exception as e:
            return f"error finding: {e}"


    def get_dsar_data(self, text):
        try:
            parent_locator = self.page.locator('footer')
            locator = parent_locator.locator('a', has_text= text)

            if locator:
                element = locator.nth(0)
                dsar_link = element.get_attribute('href')
                return dsar_link
            else:
                return None
        except Exception as e:
            return f"error finding: {e}"