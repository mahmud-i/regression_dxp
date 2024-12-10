import os
import atexit
import configparser as cp
import regression_package.utils.json_utility as j
from regression_package.tests.test_pdp import PDPTest
from regression_package.tests.test_site_integration import IntegrationCheck
from regression_package.utils.browser_utility import ConfigurePlatform
from regression_package.pages.base_page import PageInstance
from regression_package.tests.test_seo import SEOTest
from datetime import datetime



class TestInstance:
    def __init__(self, brand_name, config_path, integration: IntegrationCheck):
        self.global_config = cp.ConfigParser()
        self.global_config.read(config_path)
        self.config = cp.ConfigParser()
        self.config.read(f"./config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.brand_name = brand_name
        self.env = self.global_config['settings'].get('env', 'prod').strip().lower()
        current_time = datetime.now()
        self.time = current_time.strftime("%H_%M")
        self.date = current_time.strftime("%m-%d-%Y")
        self.integration = integration
        self.testing_error = {}
        self.test_result = {}
        self.test_failed_result = {}
        self.stage_domain_url = self.stage_domain() if self.env == "stage" else None
        tests =['site_integration', 'seo']
        test_list = self.global_config['tests'].get('tests_to_run', None).strip().lower()
        items = test_list.split(',') if test_list else None
        self.tests_list = [test.strip() for test in items] if items else tests
        self.report_directory = None
        atexit.register(self.save_reports)


    def stage_domain(self):
        brand_name = self.prod_domain_url.replace('https://www.', '').split('.')[0].strip()
        domain_url = 'https://na-' + brand_name + '-us.staging.dxp.kenvue.com/'
        return domain_url


    def page_setup(self, context):
        if self.env == "stage" :
            domain_url = self.stage_domain_url.replace('https://', 'https://kenvueuser:KenvuePassword2024!@')
        else:
            domain_url = self.prod_domain_url
        print("\n")
        page = PageInstance(context, domain_url)
        cookie, mail_signup = page.close_pop_ups()
        if cookie == 'T' and mail_signup == 'T':
            print("Site context setup was successful.\n")
        elif cookie == 'T':
            print(f"Error in Email signup PoPUp: {mail_signup} ")
        else:
            print(f"Error in Cookie Accepting: {cookie} ")

        if 'site_integration' in self.tests_list:
            self.integration.run_site_integration_test(self.brand_name, self.config, page)
        page.terminate()
        print("Site Integration parameter checking done.\n")



    def execute_test(self, urls_to_check):
        with ConfigurePlatform(self.global_config).browser() as (browser, context):
            c = 0
            self.page_setup(context)

            if urls_to_check:
                total = len(urls_to_check)
                print(f"\n\n\nRunning tests for: {self.brand_name.strip().upper()} [{self.env.strip().upper()}]\nTotal urls to check: {total}")

                self.report_directory = f"Tests_data_result/{self.date}/{self.brand_name.strip().upper()}_[{self.env.strip().upper()}]/{self.time}"
                os.makedirs(self.report_directory, exist_ok=True)

                if 'seo' in self.tests_list:
                    seo_test_instance = SEOTest(self.brand_name, self.config, self.prod_domain_url, self.stage_domain_url, self.report_directory)

                pdp_test_instance = PDPTest(self.brand_name, self.config, self.prod_domain_url, self.stage_domain_url, self.report_directory)

                # Now loop through each URL and run tests
                for url in urls_to_check:
                    if self.env == "stage" :
                        url = url.replace(self.prod_domain_url, self.stage_domain_url)

                    c += 1
                    print(f"\nPage: {c}/{total}")
                    page = PageInstance(context, url)

                    if page.open_status == "success":
                        page_type = page.get_page_type()
                        self.test_result[f'{page.slug}'] = {}
                        self.test_result[f'{page.slug}'] = {"url": url, "Page_type": page_type }

                        if 'seo' in self.tests_list:
                            seo_result = seo_test_instance.run_seo_test(page)
                            self.test_result[f'{page.slug}']["SEO_result"] = seo_result
                            if "Failed_Result" in seo_result and seo_result["Failed_Result"]:
                                self.test_failed_result[f'{page.slug}'] = {}
                                self.test_failed_result[f'{page.slug}']["SEO_result"] = {"Failed_Result": seo_result["Failed_Result"] }

                        if page_type == "productPage" and 'pdp' in self.tests_list:
                            pdp_test_instance.run_pdp_test(page)


                        page.terminate() # Close the page after testing


                    else:
                        self.testing_error[f'{url}'] = {"error" : f"page opening error: {page.open_status}"} #Exeption handling in case of Page error due to network or any other reason.
                        self.test_result[f'{page.slug}'] = {"url": url, "Failed_Result": f"page opening error: {page.open_status}"}

            else:
                print("No urls to run test")



    def save_reports(self):
        if self.test_result:
            j.save_json(self.test_result,
                        f"{self.report_directory}/{self.brand_name.strip().upper()}_[{self.env.strip().upper()}]_test_result.json")  # Full test report generation

            if self.global_config['settings'].get('full_site_testing', 'Y').strip().upper() == 'Y':
                data = []
                for key, value in self.test_result.items():
                    url = value.get("url", "")  # Default to an empty string if "url" is missing
                    page_type = value.get("Page_type", "Unknown")  # Default to "Unknown" if "Page_type" is missing
                    data.append({"url": url, "Page_type": page_type})
                saving_path = f"test_urls/{self.brand_name}/[{self.env.strip().upper()}]"
                os.makedirs(saving_path, exist_ok=True)
                j.create_csv(data, f"{saving_path}/urls_with_page_type_{self.date}_{self.time}.csv")

        if self.test_failed_result:
            j.save_json(self.test_failed_result,
                        f"{self.report_directory}/{self.brand_name.strip().upper()}_[{self.env.strip().upper()}]_test_Failure_result.json")


        if self.testing_error:
            j.save_json(self.testing_error,
                        f"{self.report_directory}/{self.brand_name.strip().upper()}_[{self.env.strip().upper()}]_error_page_testing.json")  # Page with error report generation

