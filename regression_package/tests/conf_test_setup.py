import os
import configparser as cp
import regression_package.utils.json_utility as j
from regression_package.tests.test_site_integration import IntegrationCheck
from regression_package.utils.browser_utility import ConfigurePlatform
from regression_package.pages.base_page import PageInstance
from regression_package.tests.test_seo import SEOTest
from datetime import datetime
import regression_package.tests.test_pdp as pdp_test



class TestInstance:
    def __init__(self, brand_name, config_path, integration: IntegrationCheck):
        self.global_config = cp.ConfigParser()
        self.global_config.read(config_path)
        self.config = cp.ConfigParser()
        self.config.read(f"./config_files/{brand_name}.ini")
        self.prod_domain_url = self.config['urls_data']['prod_domain_url']
        self.brand_name = brand_name
        current_time = datetime.now()
        self.time = current_time.strftime("%H-%M")
        self.date = current_time.strftime("%d-%m-%Y")
        self.integration = integration
        self.testing_error = {}
        self.test_result = {}





    def page_setup(self, context):
        page = PageInstance(context, self.prod_domain_url)
        cookie, mail_signup = page.close_pop_ups()
        if cookie == 'T' and mail_signup == 'T':
            print("Site context setup was successful.\n")
        elif cookie == 'T':
            print(f"Error in Email signup PoPUp: {mail_signup} ")
        else:
            print(f"Error in Cookie Accepting: {cookie} ")

        self.integration.run_site_integration_test(self.brand_name,page)
        page.terminate()
        print("Site Integration parameter checking done.\n")



    def execute_test(self, urls_to_check):
        with ConfigurePlatform(self.global_config).browser() as (browser, context):
            c = 0
            self.page_setup(context)

            if urls_to_check:
                seo_test_instance = SEOTest(self.brand_name, self.config)

                total = len(urls_to_check)
                print(f"\n\n\nRunning tests for: {self.brand_name}\nTotal urls to check: {total}")

                # Now loop through each URL and run tests
                for url in urls_to_check:
                    c += 1
                    print(f"\npage: {c}/{total}")
                    page = PageInstance(context, url)

                    if page.open_status == "success":
                        seo_result = seo_test_instance.run_seo_test(page)
                        pdp_test.run_pdp_tests(page, url)

                        self.test_result[f'{page.slug}'] = {"url": url, "SEO_result": seo_result}
                        page.terminate() # Close the page after testing

                    else:
                        self.testing_error[f'{url}'] = {"error" : f"page opening error: {page.open_status}"} #Exeption handling in case of Page error due to network or any other reason.



                report_directory = f"Tests_data_result/{self.date}/{self.brand_name}/{self.time}"
                os.makedirs(report_directory, exist_ok=True)

                seo_test_instance.generate_seo_report(report_directory, self.brand_name) #SEO Test Report Generation

                if self.test_result:
                    j.save_json(self.test_result,f"{report_directory}/{self.brand_name}_test_result.json")  #Full test report generation
                if self.testing_error:
                    j.save_json(self.testing_error, f"{report_directory}/{self.brand_name}error_page_testing.json") #Page with error report generation

            else:
                print("No urls to run test")