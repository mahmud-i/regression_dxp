import os
from regression_package.pages.base_page import PageInstance


class PDPInstance:
    def __init__(self, page_instance : PageInstance):
        self.instance = page_instance
        self.page = page_instance.page
        self.product_images = None
        self.image_buttons = None
        self.image_carousel = None
        self.product_overview = None
        self.product_description = None
        self.product_title = None
        self.first_image_div = None
        self.main = None
        self.page_accordions = None
        self.get_product_overview()
        self.get_product_images()


    def get_product_overview(self):
        try:
            main_section = self.page.locator('main')
            self.main = main_section if main_section.count() > 0 else None
            product_overview = self.page.locator("div[class*='productOverview.background.base']")
            if product_overview:
                self.product_overview = product_overview
                product_description = product_overview.locator("div#overview")
                if product_description:
                    self.product_description = product_description
                    self.product_title = product_description.locator("h1").inner_text()

        except Exception as e:
            print(f"Error getting product overview section on'{self.instance.url}': {e}")


    def get_product_images(self):
        try:
            image_carousel = self.product_overview.locator('.keen-slider.vds-d_flex')
            self.image_carousel = image_carousel if image_carousel else None
            product_images = self.image_carousel.locator('img[loading="eager"]')
            if product_images.count() > 0:
                self.product_images = product_images
                self.first_image_div = self.product_images.nth(0).first.locator('xpath=parent::div')
        except Exception as e:
            print(f"Error getting product images on'{self.instance.url}': {e}")

    def get_images_button_desktop(self):
        try:
            image_thumbnail = self.product_overview.locator('.keen-slider.thumbnail')
            self.image_buttons = image_thumbnail.locator("button")
        except Exception as e:
            print(f"Error getting product images on'{self.instance.url}': {e}")

    def get_images_button_responsive(self):
        try:
            image_thumbnail = self.product_overview.locator('div[role="tablist"]')
            self.image_buttons = image_thumbnail.locator('button[role="tab"]')
        except Exception as e:
            print(f"Error getting product images on'{self.instance.url}': {e}")

    def get_first_image_x_coordinates(self):
        try:
            style_attribute = self.instance.safe_get_attribute(self.first_image_div, "style")

            if style_attribute and "translate3d" in style_attribute:
                start = style_attribute.find("translate3d(") + len("translate3d(")
                end = style_attribute.find(")", start)
                translate3d_value = style_attribute[start:end]

                # Split the values
                x, y, z = translate3d_value.split(", ")

                return x

        except Exception as e:
            print(f"Error getting first image coordinates on'{self.instance.url}': {e}")
            return None

    def get_next_button(self):
        try:
            next_button = self.product_overview.locator('[aria-label="Next slide"]')
            return next_button if next_button.count() > 0 else None
        except Exception as e:
            print(f"Error getting image next button on'{self.instance.url}': {e}")
            return None

    def get_prev_button(self):
        try:
            prev_button = self.product_overview.locator('[aria-label="Previous slide"]')
            return prev_button if prev_button.count() > 0 else None
        except Exception as e:
            print(f"Error getting image next button on'{self.instance.url}': {e}")
            return None

    def get_touch_positions(self):
        try:
            bbox = self.image_carousel.bounding_box()
            start_x = bbox["x"] + bbox["width"] * 0.8  # Start near the right edge
            start_y = bbox["y"] + bbox["height"] / 2  # Center vertically
            end_x = bbox["x"] + bbox["width"] * 0.2  # End near the left edge

            return start_x, start_y, end_x

        except Exception as e:
            print(f"Error getting image bound box position on '{self.instance.url}': {e}")
            return None

    def image_left_slide(self):
        try:
            start_x, start_y, end_x = self.get_touch_positions()

            self.page.mouse.move(start_x, start_y)
            self.page.mouse.down()  # Simulate touchstart (mouse down)
            self.page.mouse.move(end_x, start_y, steps=100)  # Simulate touchmove (dragging)
            self.page.mouse.up()  # Simulate touchend (mouse up)
            self.instance.wait_for_time(1000)

        except Exception as e:
            print(f"Error image left sliding on '{self.instance.url}': {e}")
            return None

    def image_right_slide(self):
        try:
            start_x, start_y, end_x = self.get_touch_positions()

            self.page.mouse.move(end_x, start_y)
            self.page.mouse.down()  # Simulate touchstart (mouse down)
            self.page.mouse.move(start_x, start_y, steps=100)  # Simulate touchmove (dragging)
            self.page.mouse.up()  # Simulate touchend (mouse up)
            self.instance.wait_for_time(1000)

        except Exception as e:
            print(f"Error image right sliding on '{self.instance.url}': {e}")
            return None

    def get_desktop_button_class(self, button_selector):
        try:
            button = self.image_buttons.nth(button_selector)
            class_attribute = self.instance.safe_get_attribute(button, "class")
            return class_attribute.split()
        except Exception as e:
            print(f"Error getting {button_selector} no. button class value on '{self.instance.url}': {e}")
            return None

    def get_response_button_aria(self, button_selector):
        try:
            button = self.image_buttons.nth(button_selector)
            aria_selected = self.instance.safe_get_attribute(button, "aria-selected")
            return aria_selected.split()
        except Exception as e:
            print(f"Error getting {button_selector} no. button aria-selected value on '{self.instance.url}': {e}")
            return None


    def get_product_short_description(self):
        try:
            product_short_description = self.product_description.locator("div[class*='pdp.productOverview.text.body']")
            return self.instance.safe_get_inner_text(product_short_description) if product_short_description else None
        except Exception as e:
            print(f"Error getting product short description on'{self.instance.url}': {e}")
            return None

    def get_bv_components(self):
        try:
            bv_section = self.product_description.locator("div.bv-inline")
            #try:
            bv_data_locator = bv_section.locator('div[data-bv-ready="true"]') #if bv_section else None
            #except TimeoutError:
                #bv_data_locator = None
            bv_footer_section = self.page.locator('#reviews')
            bv_footer_data_locator = bv_footer_section.locator('div[data-bv-ready="true"]') #if bv_footer_section and bv_data_locator is None else None
            review_form_a = self.page.locator("#bv-mbox-lightbox-list")
            review_form_b = self.page.locator('div[type="main"][role="dialog"]')

            if bv_data_locator.count() > 0:
                bv_id = bv_data_locator.get_attribute("data-bv-product-id")
                bv_write_review_button = bv_data_locator.locator('button:has-text("Write a Review")')

            elif bv_footer_data_locator.count() > 0:
                bv_id = bv_footer_data_locator.get_attribute("data-bv-product-id")
                bv_write_review_button = bv_footer_data_locator.locator('button:has-text("Write a Review")')

            else:
                bv_id = None
                bv_write_review_button = None

            if bv_id and bv_write_review_button:
                return { "success": True, "values": (bv_id, bv_write_review_button, review_form_a, review_form_b) }
            else:
                return { "success": False, "values": None }

        except Exception as e:
            print(f"Error getting BV components on'{self.instance.url}': {e}")
            return { "success": False, "values": None, "error": str(e) }



    def get_wtb_ps_components(self):
        try:
            ps_div = self.product_description.locator('div[ps-widget-type="lightbox"]')
            ps_sku = self.instance.safe_get_attribute(ps_div, "ps-sku")
            wtb_button = ps_div.locator('span.ps-button-label')
            ps_pop_up = self.page.locator('.ps-container[role="dialog"][aria-label="Shop  from other retailers with this shopping interface."]')
            if ps_sku and wtb_button:
                return { "success": True, "values": (ps_sku, wtb_button, ps_pop_up) }
            else:
                return { "success": False, "values": None }
        except Exception as e:
            print(f"Error getting wtb ps components on'{self.instance.url}': {e}")
            return { "success": False, "values": None }

    def get_jump_links(self):
        try:
            jump_nav = self.main.locator('nav[data-sb-field-path=".jumpLinks"]')
            jump_links = jump_nav.locator('a')
            return jump_links if jump_links.count() > 0 else None
        except Exception as e:
            print(f"Error getting jump links on'{self.instance.url}': {e}")
            return None


    def get_jump_link_details(self, link_selector):
        try:
            jump_link_name = link_selector.text_content()
            jump_id = self.instance.safe_get_attribute(link_selector, "href")
            jump_locator = self.main.locator(f'{jump_id}')
            return jump_link_name, jump_locator
        except Exception as e:
            print(f"Error getting jump link details on'{self.instance.url}': {e}")
            return None


