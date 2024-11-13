import configparser as cp
from playwright.sync_api import sync_playwright
from contextlib import contextmanager



class ConfigurePlatform:
    def __init__(self, config):
        self.config = config
        self.headless_chk = self.config['settings'].get('headless_chk', 'Y').strip().upper()
        self.mobile_device = self.config['platform'].get('mobile_emulation', 'N').strip().upper()
        self.browser_type = self.config['platform'].get('browser_type', 'chromium')
        self.viewport_width = self.config['platform'].getint('viewport_width', 1280)
        self.viewport_height = self.config['platform'].getint('viewport_height', 940)
        self.device_model  = self.config['platform'].get('mobile_model', 'iphone 12')



    def check_headless(self):
        return self.headless_chk == 'Y'

    @contextmanager
    def browser(self):
        headless = self.check_headless()
        with sync_playwright() as p:
            if self.mobile_device == 'N':
                if self.browser_type == 'chromium':
                    browser = p.chromium.launch(headless = headless)
                elif self.browser_type == 'firefox':
                    browser = p.firefox.launch(headless = headless)
                elif self.browser_type == 'webkit':
                    browser = p.webkit.launch(headless = headless)
                else:
                    raise ValueError(f"Unsupported browser type: {self.browser_type}")
                context = browser.new_context(viewport={'width': self.viewport_width, 'height': self.viewport_height})
            else :
                browser = p.chromium.launch(headless=headless)
                device = p.devices[self.device_model]
                context = browser.new_context(**device)

            yield browser, context
            browser.close()