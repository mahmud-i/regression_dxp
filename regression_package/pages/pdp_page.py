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
        self.first_image_div = None
        self.page_accordions = None
        self.get_product_overview()
        self.get_product_images()


    def get_product_overview(self):
        try:
            product_overview = self.page.locator("div[class*='productOverview.background.base']")
            self.product_overview = product_overview if product_overview else None
        except Exception as e:
            print(f"Error getting product overview section on'{self.instance.url}': {e}")


    def get_product_images(self):
        try:
            image_carousel = self.product_overview.locator('.keen-slider.vds-d_flex')
            self.image_carousel = image_carousel if image_carousel else None
            product_images = self.image_carousel.locator('img[loading="eager"]')
            if product_images:
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
            return next_button
        except Exception as e:
            print(f"Error getting image next button on'{self.instance.url}': {e}")
            return None

    def get_prev_button(self):
        try:
            prev_button = self.product_overview.locator('[aria-label="Previous slide"]')
            return prev_button
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


    '''
    def get_product_details_accordions(self):
        try:
            product_details_locator = self.page.locator("div[class*='productOverview.background.base']")
    '''