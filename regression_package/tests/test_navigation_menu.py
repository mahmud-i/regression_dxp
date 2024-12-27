import os
import random as rand
import atexit
import regression_package.utils.json_utility as j
from regression_package.pages.base_page import PageInstance
from regression_package.pages.menu_navigation import MenuNavInstance



class MenuNavTest:
    def __init__(self, brand_name, config, prod_domain, stage_domain, report_directory):
        self.brand = brand_name
        self.global_result_data = {}
        self.testing_data_path = config['testing_data_path'].get('seo_data_path', None)
        self.testing_data = j.load_json(self.testing_data_path) if self.testing_data_path else None
        self.env = "stage" if stage_domain is not None else "prod"
        self.prod_domain = prod_domain
        self.stage_domain = stage_domain
        self.global_test_result = {}
        self.global_pass_result = {}
        self.global_error_result = {}
        self.report_directory = report_directory
        self.instance = None
        self.slug = None
        self.url = None
        #atexit.register(self.generate_pdp_report)


    def run_menu_navigation_test(self, page_instance: PageInstance):
        try:
            self.instance = MenuNavInstance(page_instance)

            self.instance.get_menu_list()

        except Exception as e:
            print(e)

    def navigation_test(self, page_instance: PageInstance):
        try:
            self.instance = MenuNavInstance(page_instance)

            self.url = self.instance.instance.url
            self.slug = self.instance.instance.slug

            self.global_result_data[f'{self.slug}'] = {"url": self.url}
            self.global_test_result[f'{self.slug}'] = {"url": self.url}
            self.global_pass_result[f'{self.slug}'] = {"url": self.url}
            self.global_error_result[f'{self.slug}'] = {"url": self.url, "test_error_result": None}
            test_result = {}

            viewport_width = self.instance.page.evaluate("window.innerWidth")

            self.global_result_data[f'{self.slug}']['Product_name'] = self.instance.product_title
            self.global_result_data[f'{self.slug}']['Product_Short_Description'] = self.instance.get_product_short_description()

            #image carousel test start
            image_count = self.instance.product_images.count()
            self.global_result_data[f'{self.slug}']['Product_image_count'] = image_count
            if image_count > 1:
                test_result['image_carousel_test'] = self.image_carousel_test(viewport_width)
                test_result['image_button_test'] = self.image_button_test(viewport_width, image_count)

            bv_id, test_result['bv_review_form_test'] = self.bv_review_test()
            self.global_result_data[f'{self.slug}']['BV_ID'] = bv_id

            ps_sku, test_result['wtb_ps_test'] = self.wtb_ps_test()
            self.global_result_data[f'{self.slug}']['PS_SKU'] = ps_sku

            jump_links, test_result['jump_links_test'] = self.jump_links_test()
            self.global_result_data[f'{self.slug}']['Jump_Links'] = jump_links


            if not self.global_error_result[f'{self.slug}']['test_error_result']:
                del self.global_error_result[f'{self.slug}']

            '''
            if self.testing_data:
                test_result = self.compare_seo_data(slug, url, seo_data)
                return test_result
            else:
                return {"Failed_Result": f"No SEO testing data has been found for this '{self.brand.strip().upper()}'. Wrong path for SEO testing data, '{self.testing_data_path}'"}
            '''

        except Exception as e:
            return {"Failed_Result": f"Error run_PDP_test on'{page_instance.url}': {e}"}

