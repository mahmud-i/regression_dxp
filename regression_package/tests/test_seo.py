import os
import regression_package.utils.json_utility as j
from regression_package.pages.base_page import PageInstance
from regression_package.pages.seo_page import SEOInstance



class SEOTest:
    def __init__(self, brand_name, config):
        self.brand = brand_name
        self.global_seo_result_data = {}
        self.seo_testing_data_path = config['testing_data_path'].get('seo_data_path', None)
        self.seo_testing_data = j.load_json(self.seo_testing_data_path ) if self.seo_testing_data_path else None
        self.global_seo_test_result = {}
        self.global_seo_pass_result = {}
        self.global_seo_error_result = {}



    def run_seo_test(self, page_instance: PageInstance):
        try:
            instance = SEOInstance(page_instance)

            url = page_instance.url
            slug = page_instance.slug

            seo_data = {
                "page_response" : page_instance.response,
                "meta_title" : instance.get_title(),
                "meta_description" : instance.get_meta_description(),
                "canonical_link" : instance.get_canonical_link(),
                "og_title" : instance.get_og_title(),
                "og_description" : instance.get_og_description(),
                "og_type" : instance.get_og_type(),
                "og_site" : instance.get_og_site(),
                "og_url" : instance.get_og_url(),
                "og_image" : instance.get_og_image(),
                "twitter_title" : instance.get_twitter_title(),
                "twitter_description" : instance.get_twitter_description(),
                "twitter_card" : instance.get_twitter_card(),
                "twitter_image" : instance.get_twitter_image(),
                "h1" : instance.get_h1()
                }
            self.global_seo_result_data[f'{slug}'] = {"url": url, "seo_data": seo_data}
            print(f"SEO Data: {seo_data}")

            if self.seo_testing_data:
                test_result = self.compare_seo_data(slug, url, seo_data)
                return test_result

        except Exception as e:
            return {"Failed_Result": f"Error run_SEO_test on'{page_instance.url}': {e}"}



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

        if slug in self.seo_testing_data:
            check_url = self.seo_testing_data[slug].get("url")
            seo_test_data = self.seo_testing_data[slug].get("seo_data",{})

            if check_url != url:
                errors.update({'url_check': f"Page url not Matched with: '{check_url}'"})
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
                        result_text = f"Value is deleted. previous: {val_2}"
                    elif val_2 is None:
                        result = "Fail"
                        result_text = f"Value is added: {val_1}"
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
                    if key in url_items and val_1 == url and result == "Fail":
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
            self.global_seo_pass_result[f'{slug}'] = {"url": url, "Passed_Result": passing}
        if errors:
            self.global_seo_error_result[f'{slug}'] = {"url": url, "Failed_Result": errors}
            test_result.update({"Failed_Result": errors})

        self.global_seo_test_result[f'{slug}'] = {"url": url, "seo_test_result": test_result}

        return test_result





    def generate_seo_report(self, report_directory, brand_name):
        seo_directory = f"{report_directory}/SEO_Report"
        os.makedirs(seo_directory, exist_ok=True)
        if self.global_seo_result_data:
            j.save_json(self.global_seo_result_data, f"{seo_directory}/{brand_name}_seo_data.json")
        if self.global_seo_test_result:
            j.save_json(self.global_seo_test_result, f"{seo_directory}/{brand_name}_seo_test_result.json")
        if self.global_seo_pass_result:
            j.save_json(self.global_seo_pass_result, f"{seo_directory}/{brand_name}_seo_pass_result.json")
        if self.global_seo_error_result:
            j.save_json(self.global_seo_error_result, f"{seo_directory}/{brand_name}_seo_error_result.json")