import os
import atexit
import regression_dxp.regression_package.utils.json_utility as j
from regression_dxp.regression_package.pages.base_page import PageInstance
from regression_dxp.regression_package.pages.integration_page import IntegrationInstance


class IntegrationCheck:
    def __init__(self, report_directory, env):
        self.global_result_data = {}
        self.report_directory = report_directory
        self.env = env
        # self.seo_testing_data = j.load_json(self.seo_testing_data_path)
        self.global_test_result = {}
        self.global_pass_result = {}
        self.global_error_result = {}
        atexit.register(self.generate_report)

    def run_site_integration_test(self, brand_name, config, page_instance: PageInstance):
        try:

            instance = IntegrationInstance(page_instance)

            integration_data ={
                "OT_ID" : instance.get_ot_id(),
                "BV_Data" : instance.get_bv_env_data(),
                "CareClub_Data" : instance.get_cc_data(),
                "UCU_Link" : self.ucu_test(config, instance),
                "DSAR_Link" : self.dsar_test(config, instance)
            }

            self.global_result_data [f'{brand_name.strip().upper()} [{self.env.strip().upper()}]'] = {"url": f'{page_instance.domain}', "site_integration_data": integration_data}
            print(f"Integration_Data: {integration_data}")

        except Exception as e:
            return {"Failed_Result": f"Error run_site_integration_test on'{brand_name}': {e}"}

    @staticmethod
    def ucu_test(config, instance):
        try:
            ucu_data = {}
            result = {}

            ucu_slug = config['integration_check'].get('ucu_slug', None)
            result.update({'ucu_slugs' : ucu_slug})
            slug_list = ucu_slug.split(',')
            slug_list = [slug.strip() for slug in slug_list]

            for slug in slug_list:
                ucu_text = config['integration_check'].get(slug, "email us")
                link = instance.get_ucu_data(slug, ucu_text)
                ucu_data.update({f'ucu_link_on_{slug}': link})

            if ucu_data:
                links = list(ucu_data.values())
                if all(value == links[0] for value in links):
                    result.update({"uniform_link": f"{links[0]}"})
                    return f"{links[0]}"
                else:
                    result.update({"multiple_link": ucu_data})
                    return result
            else:
                return None

        except Exception as e:
            return {"error": f"error finding UCU link: {e}"}

    @staticmethod
    def dsar_test(config, instance):
        try:
            dsar_data = {}
            result = {}
            error = {}

            dsar_text = config['integration_check'].get('dsar_text', None)
            result.update({'DSAR_items': dsar_text})
            dsar_list = dsar_text.split(',')
            dsar_list = [val.strip() for val in dsar_list]

            for text in dsar_list:
                link = instance.get_dsar_data(text)
                if link.startswith("error"):
                    error.update({f'{text}': f'{link}'})
                else:
                    dsar_data.update({f'{text}': f'{link}'})

            if dsar_data or error:
                links = list(dsar_data.values())
                if error:
                    result['error'] = {"error data": error, "good data": dsar_data}
                if all(value == links[0] for value in links):
                    result.update({"uniform_link": f"{links[0]}"})
                    return f"{links[0]}"
                else:
                    result.update({"multiple_link": dsar_data})
                    return result
            else:
                return None

        except Exception as e:
            return {"error": f"error finding DSAR link: {e}"}

    def generate_report(self):
        report = self.report_directory
        if self.global_result_data:
            os.makedirs(report, exist_ok=True)
            j.save_json(self.global_result_data, f"{report}/JnJ_US_[{self.env.strip().upper()}]_sites_integration_data.json")
        if self.global_test_result:
            j.save_json(self.global_test_result, f"{report}/JnJ_US_[{self.env.strip().upper()}]_sites_integration_test_result.json")
        if self.global_pass_result:
            j.save_json(self.global_pass_result, f"{report}/JnJ_US_[{self.env.strip().upper()}]_sites_integration_pass_result.json")
        if self.global_error_result:
            os.makedirs(report, exist_ok=True)
            j.save_json(self.global_error_result, f"{report}/JnJ_US_[{self.env.strip().upper()}]_sites_integration_error_result.json")
