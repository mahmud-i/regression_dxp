import os
from regression_package.pages.base_page import PageInstance


class MenuNavInstance:
    def __init__(self, page_instance : PageInstance):
        self.instance = page_instance
        self.page = page_instance.page


    def get_menu_list(self):
        try:
            header = self.page.locator('header')
            menu_nav = header.locator('nav[aria-label="Main"][data-sb-field-path=".primaryNavigation"]')
            menu_list = menu_nav.locator('li')

            print(f"{menu_list.count()}")

            for i in range(menu_list.count()):
                self.page.mouse.move(0, 0)
                self.page.wait_for_timeout(timeout=1000)
                primary_item = menu_list.nth(i)
                attribute_value = primary_item.get_attribute('data-sb-object-id')
                #print(f"{primary_item} -> {attribute_value}")
                if attribute_value is not None:
                    primary_button = primary_item.locator('button')
                    primary_menu = primary_button.inner_text()
                    primary_menu_anchor = primary_button.locator('a')
                    print(f"{primary_menu} : {primary_menu_anchor.count()}")
                    if primary_menu_anchor.count() > 0:
                        primary_menu_link = primary_menu_anchor.get_attribute('href')
                        primary_menu_status = self.instance.open_page_new_tab(primary_menu_link)
                        print(f"   {primary_menu} -> {primary_menu_link} -> {primary_menu_status}")
                        self.page.bring_to_front()
                    else:
                        print(f"   {primary_menu}")
                        '''button_area = primary_button.bounding_box()
                        x = button_area['x'] + button_area['width'] / 2
                        y = button_area['y'] + button_area['height'] / 2
                        self.page.mouse.move(x, y)'''
                    #self.page.wait_for_timeout(timeout=1000)
                    parent_locator = primary_item.locator('..')
                    primary_button.hover(timeout=1000)
                    self.page.wait_for_timeout(timeout=1000)
                    secondary_nav = parent_locator.locator('div[dir="ltr"]')
                    print(f"secondary nav: {secondary_nav.count()}")
                    secondary_nav_type = secondary_nav.get_attribute('data-sb-field-path') if secondary_nav.count() > 0 else None
                    print(f"secondary nav type: {secondary_nav_type}")
                    if secondary_nav_type == ".subNavigation":
                        secondary_nav_list = secondary_nav.locator('li')
                        for j in range(secondary_nav_list.count()):
                            primary_button.hover(timeout=1000)
                            self.page.wait_for_timeout(timeout=1000)
                            secondary_item = secondary_nav_list.nth(j)
                            secondary_menu_item = secondary_item.locator('a')
                            secondary_menu = secondary_menu_item.inner_text()
                            secondary_menu_link = secondary_menu_item.get_attribute('href')
                            secondary_menu_item.hover(timeout=1000)
                            self.page.wait_for_timeout(timeout=1000)
                            secondary_menu_status = self.instance.open_page_new_tab(secondary_menu_link)
                            print(f"   {primary_menu} -> {secondary_menu} -> {secondary_menu_link} -> {secondary_menu_status}")
                            self.page.bring_to_front()
                    elif secondary_nav_type == ".megaMenu":
                        mega_menu_section = secondary_nav.locator('ul > li > div')
                        for j in range(mega_menu_section.count()):
                            primary_button.hover(timeout=1000)
                            self.page.wait_for_timeout(timeout=1000)
                            mega_item = mega_menu_section.nth(j)
                            mega_menu_item = mega_item.locator('//div//span')
                            mega_menu = mega_menu_item.inner_text().strip()
                            mega_menu_anchor = mega_item.locator('span >a')
                            if mega_menu_anchor.count() > 0:
                                mega_menu_anchor.hover(timeout=1000)
                                self.page.wait_for_timeout(timeout=1000)
                                mega_menu_link = mega_menu_anchor.get_attribute('href')
                                mega_menu_status = self.instance.open_page_new_tab(mega_menu_link)
                                print(f"   {primary_menu} -> {mega_menu} -> {mega_menu_link} -> {mega_menu_status}")
                                self.page.bring_to_front()
                            sub_menu = mega_item.locator('li > a')
                            for k in range(sub_menu.count()):
                                primary_button.hover(timeout=1000)
                                self.page.wait_for_timeout(timeout=1000)
                                sub_menu_item = sub_menu.nth(k)
                                sub_menu_text = sub_menu_item.inner_text().strip()
                                sub_menu_link = sub_menu_item.get_attribute('href')
                                sub_menu_item.hover(timeout=1000)
                                self.page.wait_for_timeout(timeout=1000)
                                sub_menu_status = self.instance.open_page_new_tab(sub_menu_link)
                                print(f"   {primary_menu} -> {mega_menu} -> {sub_menu_text} -> {sub_menu_link} -> {sub_menu_status}")
                                self.page.bring_to_front()

                    else:
                        continue
                self.page.wait_for_timeout(100)

        except Exception as e:
            print(f"Error getting menu list: {e}")

