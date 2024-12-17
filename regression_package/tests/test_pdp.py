import os
import random as rand
import atexit
import regression_dxp.regression_package.utils.json_utility as j
from regression_dxp.regression_package.pages.base_page import PageInstance
# from regression_dxp.regression_package.pages.pdp_page import PDPInstance


class PDPTest:
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
        # atexit.register(self.generate_seo_report)

    def run_pdp_test(self, page_instance: PageInstance):
        try:
            # self.instance = PDPInstance(page_instance)

            self.url = self.instance.instance.url
            self.slug = self.instance.instance.slug

            self.global_test_result[f'{self.slug}'] = {"url": self.url}
            self.global_pass_result[f'{self.slug}'] = {"url": self.url}

            viewport_width = self.instance.page.evaluate("window.innerWidth")

            # image carousel test start
            image_count = self.instance.product_images.count()
            if image_count > 1:
                self.image_carousel_test(viewport_width)
                self.image_button_test(viewport_width, image_count)

            '''
            if self.testing_data:
                test_result = self.compare_seo_data(slug, url, seo_data)
                return test_result
            else:
                return {"Failed_Result": f"No SEO testing data has been found for this '{self.brand.strip().upper()}'. Wrong path for SEO testing data, '{self.testing_data_path}'"}
            '''

        except Exception as e:
            return {"Failed_Result": f"Error run_PDP_test on'{page_instance.url}': {e}"}


    def image_carousel_test(self, viewport_width):
        test_result = {}
        errors = {}
        passing = {}
        try:
            if viewport_width > 1024 :
                init_x = self.instance.get_first_image_x_coordinates()
                next_button = self.instance.get_next_button()
                prev_button = self.instance.get_prev_button()
                next_button.click()
                self.instance.instance.wait_for_time(10000)
                current_x = self.instance.get_first_image_x_coordinates()
                if init_x == current_x:
                    errors.update({"next_button": "Image carousel next button not working"})
                else:
                    passing.update({"next_button": "passed"})
                prev_x = current_x
                prev_button.click()
                self.instance.instance.wait_for_time(10000)
                current_x = self.instance.get_first_image_x_coordinates()
                if prev_x == current_x:
                    errors.update({"prev_button": "Image carousel prev button not working"})
                else:
                    passing.update({"prev_button": "passed"})

            elif  viewport_width <= 1024:
                init_x = self.instance.get_first_image_x_coordinates()
                self.instance.image_left_slide()
                current_x = self.instance.get_first_image_x_coordinates()
                if init_x == current_x:
                    errors.update({"left_slide": "Image carousel left slide not swiped image"})
                else:
                    passing.update({"left_slide": "passed"})
                prev_x = current_x
                self.instance.image_right_slide()
                current_x = self.instance.get_first_image_x_coordinates()
                if prev_x == current_x:
                    errors.update({"right_slide": "Image carousel right slide not swiped image"})
                else:
                    passing.update({"right_slide": "passed"})

            if errors is None:
                self.global_pass_result[f'{self.slug}'] = {"image_carousel": passing}
                test_result.update({"Passed_Result": passing})
            else:
                if self.global_error_result[f'{self.slug}'] is None:
                    self.global_error_result[f'{self.slug}'] = {"url": self.url}
                self.global_error_result[f'{self.slug}'] = {"image_carousel": errors}
                test_result.update({"Failed_Result": errors})

            self.global_test_result[f'{self.slug}'] = {"image_carousel_test": test_result}

            return test_result

        except Exception as e:
            return {"Failed_Result": f"Error run_image_carousel_test on'{self.url}': {e}"}

    def image_button_test(self, viewport_width, max_count):
        test_result = {}
        errors = {}
        passing = {}
        try:
            i = rand.randint(1, max_count-1)
            if viewport_width > 1024 :
                self.instance.get_images_button_desktop()
                image_button = self.instance.image_buttons.nth(i)
                init_x = self.instance.get_first_image_x_coordinates()
                init_class = self.instance.get_desktop_button_class(i)
                image_button.click()
                self.instance.instance.wait_for_time(10000)
                new_class = self.instance.get_desktop_button_class(i)
                current_x = self.instance.get_first_image_x_coordinates()

                if init_x == current_x:
                    errors.update({"image_button": "Image thubnail button not switching the image"})
                else:
                    passing.update({"image_button": "passed"})
                if 'active' in new_class and 'active' not in init_class:
                    passing.update({"image_button_highlighting": "passed"})
                else:
                    errors.update({"image_button_highlighting": "Image thubnail button is not highlighted"})

            elif viewport_width <= 1024:
                self.instance.get_images_button_responsive()
                image_button = self.instance.image_buttons.nth(i)
                init_x = self.instance.get_first_image_x_coordinates()
                init_aria = self.instance.get_response_button_aria(i)
                image_button.click()
                self.instance.instance.wait_for_time(10000)
                new_aria = self.instance.get_response_button_aria(i)
                current_x = self.instance.get_first_image_x_coordinates()
                if init_x == current_x:
                    errors.update({"image_button": "Image thubnail button not switching the image"})
                else:
                    passing.update({"image_button": "passed"})
                if 'true' in new_aria and 'false' in init_aria:
                    passing.update({"image_button_highlighting": "passed"})
                else:
                    errors.update({"image_button_highlighting": "Image thubnail button is not highlighted"})

            if errors is None:
                self.global_pass_result[f'{self.slug}'] = {"image_button": passing}
                test_result.update({"Passed_Result": passing})
            else:
                if self.global_error_result[f'{self.slug}'] is None:
                    self.global_error_result[f'{self.slug}'] = {"url": self.url}
                self.global_error_result[f'{self.slug}'] = {"image_button": errors}
                test_result.update({"Failed_Result": errors})

            self.global_test_result[f'{self.slug}'] = {"image_button_test": test_result}

            return test_result

        except Exception as e:
            return {"Failed_Result": f"Error run_PDP_test on'{self.url}': {e}"}

    def compare_seo_data(self, slug, url, seo_data):
        test_result = {}
        errors = {}
        passing = {}
        title = None
        description = None
        image = None
        title_items = ["og_title", "twitter_title"]
        description_items = ["og_description", "twitter_description"]
        url_items = ["canonical_link", "og_url"]

        if slug in self.testing_data:
            check_url = self.testing_data[slug].get("url")
            url_for_items = check_url
            if self.env == "stage":
                check_url = check_url.replace(self.prod_domain,self.stage_domain)
            seo_test_data = self.testing_data[slug].get("seo_data", {})

            if check_url != url :
                errors.update({"error_data": f"urls not matching.\nCurrent:{url}\nTest_data:{check_url}"})
            else:
                for key in seo_data:
                    val_1 = seo_data.get(key)
                    val_2 = seo_test_data.get(key)

                    if key == 'meta_title':
                        title = val_1
                    if key == 'meta_description':
                        description = val_1
                    if key == 'og_image':
                        image = val_1

                    if key not in seo_test_data:
                        result = 'Fail'
                        result_text = f'Items not found in Testing Data: {val_1}'
                    elif val_1 is None and val_2 is None:
                        result = 'Pass'
                        result_text = "Value is none in Both"
                    elif val_1 is None:
                        result = "Fail"
                        result_text = f"Value has been removed. previous: {val_2}"
                    elif val_2 is None:
                        result = "Fail"
                        result_text = f"New Value has been added: {val_1}"
                    elif val_1 != val_2:
                        result = "Fail"
                        result_text = f"Not matched. Data found: {val_1}, Testing Data: {val_2} "
                    else:
                        result = "Pass"
                        result_text = f"Passed. Data: {val_1}"

                    if key in title_items and val_1 == title and result == "Fail":
                        result = "Pass"
                        result_text = f"Passed. Data: {val_1}"
                    if key in description_items and val_1 == description and result == "Fail":
                        result = "Pass"
                        result_text = f"Passed. Data: {val_1}"
                    if key in url_items and val_1 == url_for_items and result == "Fail":
                        result = "Pass"
                        result_text = f"Passed. Data: {val_1}"
                    if key == 'twitter_image' and val_1 == image and result == "Fail":
                        result = "Pass"
                        result_text = f"Passed. Data: {val_1}"
                    if key == 'h1' and val_1 == "Multiple items" and result == "Pass":
                        result = "Fail"
                        result_text = "Multiple \"h1\" data available in the Page."

                    if result == "Pass":
                        passing.update({f"{key}": "Passed"})
                    elif result == "Fail":
                        errors.update({f"{key}": "Fail", f"{key}_details": result_text})
        else:
            errors.update({"error_data": f"No Data found in the Testing Data for this Page. Url:{url}"})

        if passing:
            test_result.update({"Passed_Result": passing})
            self.global_pass_result[f'{slug}'] = {"url": url, "Passed_Result": passing}
        if errors:
            self.global_error_result[f'{slug}'] = {"url": url, "Failed_Result": errors}
            test_result.update({"Failed_Result": errors})

        self.global_test_result[f'{slug}'] = {"url": url, "seo_test_result": test_result}

        return test_result

    def generate_seo_report(self):
        report = f"{self.report_directory}/SEO_Report"
        os.makedirs(report, exist_ok=True)
        if self.global_result_data:
            j.save_json(self.global_result_data, f"{report}/{self.brand.strip().upper()}_[{self.env.strip().upper()}]_seo_data.json")
        if self.global_test_result:
            j.save_json(self.global_test_result, f"{report}/{self.brand.strip().upper()}_[{self.env.strip().upper()}]_seo_test_result.json")
        if self.global_pass_result:
            j.save_json(self.global_pass_result, f"{report}/{self.brand.strip().upper()}_[{self.env.strip().upper()}]_seo_pass_result.json")
        if self.global_error_result:
            j.save_json(self.global_error_result, f"{report}/{self.brand.strip().upper()}_[{self.env.strip().upper()}]_seo_error_result.json")
