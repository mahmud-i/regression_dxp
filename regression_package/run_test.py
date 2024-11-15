# execute_project.py
import argparse
import configparser as cp

from regression_package.pages.integration_page import IntegrationInstance
from regression_package.tests.test_site_integration import IntegrationCheck
from regression_package.utils.get_urls import GetUrls
from regression_package.tests.conf_test_setup import TestInstance


def initializing_test(config_path):

    parser = argparse.ArgumentParser(description="Process multiple data points.")

    # Load configuration file argument
    parser.add_argument("--config", type=str, default= config_path, help="Config file path")

    # Optional arguments
    parser.add_argument("--brands", type=str, help="Brands for test (separate with comma for multiple)")
    parser.add_argument("--full_site", type=str, help="If test run for full site")
    parser.add_argument("--parsing_method", type=str, help="Method for getting URLs (1, 2, or 3)")
    parser.add_argument("--headless", type=str, help="Headless mode")
    parser.add_argument("--browser", type=str, help="Browser type")
    parser.add_argument("--mobile", type=str, help="Test on Mobile device")
    parser.add_argument("--device_model", type=str, help="Mobile device model")

    # Parse arguments only once here
    args = parser.parse_args()

    # Load configuration file
    config_path = args.config
    config = cp.ConfigParser()
    config.read(config_path)

    # Retrieve default values from the config file, if needed
    brands = args.brands or config['settings'].get('brands', '')
    full_site_testing = args.full_site or config['settings'].get('full_site_testing', 'Y').strip().upper()
    parsing_method = args.parsing_method or config['settings'].get('parsing_method', '3')

    # Update settings in the config object based on arguments
    if args.headless is not None:
        config.set('settings', 'headless_chk', args.headless.strip().upper())

    if args.browser is not None:
        config.set('platform', 'browser_type', args.browser.strip().lower())

    if args.mobile is not None:
        responsive = args.mobile.strip().upper()
        if responsive == 'Y' and args.device_model is not None:
            config.set('platform', 'mobile_emulation', "Y")
            config.set('platform', 'mobile_model', args.device_model)
        else:
            config.set('platform', 'mobile_emulation', "N")

    # Write updated settings back to the configuration file
    with open(config_path, 'w') as configfile:
        config.write(configfile)

    # Process brand list and run tests
    brand_list = brands.split(',')
    brand_list = [brand.strip() for brand in brand_list]
    integration_test_instance = IntegrationCheck()

    for brand_name in brand_list:
        urls_parser = GetUrls(brand_name, parsing_method)

        urls_to_check = (
            urls_parser.get_urls_from_sitemap() if full_site_testing == 'Y'
            else urls_parser.get_urls_from_others()
        )

        # Running the test suite
        test_service = TestInstance(brand_name, config_path, integration_test_instance)
        test_service.execute_test(urls_to_check)