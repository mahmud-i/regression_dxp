


def run_pdp_tests(page, url):

    page_type = page.get_page_type()
    print(f"Page type: {page_type}\n\n\n")
    page.terminate()  # Close the page after testing
