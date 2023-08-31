import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def search_and_click(self, search_data):
        self.driver.maximize_window()
        self.driver.get("http://10.10.10.66/products/assembly-summary-table/")

        try:
            for search_item in search_data:
                element = self.driver.find_element(By.XPATH, search_item["xpath"])
                element.click()

                search_input_xpath = f'{search_item["xpath"]}/span/div/div/div[1]/input'
                search_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, search_input_xpath)))

                for query in search_item["queries"]:
                    search_input.clear()
                    search_input.send_keys(query)
                    search_input.send_keys(Keys.ENTER)
                    time.sleep(1)

                    try:
                        result = self.driver.find_element(By.XPATH, f"//*[text()='{query}']")
                        #print(f"Clicking search result: {query}")
                        result.click()

                    except (StaleElementReferenceException, NoSuchElementException):
                        #print(f"Element not found or became stale for query: {query}")

                        # Handle case where search result is not found
                        #print(f"No search result found for query: {query}")

                        pass

                exit_element_xpath = '//*[@id="post-31"]/div/h5'
                exit_element = self.wait.until(EC.presence_of_element_located((By.XPATH, exit_element_xpath)))

                # Scroll to the element
                self.driver.execute_script("arguments[0].scrollIntoView();", exit_element)

                # Click the element
                exit_element.click()

            while True:
                time.sleep(10)

        except KeyboardInterrupt:
            pass

        finally:
            self.driver.quit()
"""
if __name__ == "__main__":
    search_data = [
        {
            "xpath": '//*[@id="table_1_1_filter"]',
            "queries": ["BH513121", "BH515096", "BH512513"],
        },
        {
            "xpath": '//*[@id="table_1_5_filter"]',
            "queries": ["104412100E", "104412200E", "104412300A"],
        },
        {
            "xpath": '//*[@id="table_1_14_filter"]',
            "queries": ["1979~1985 Buick Riviera,1979~1985 Cadillac Eldorado,1980~1985 Seville,1984~1996 Chevy Corvette,1983~1993 S10"],
        }
    ]

    web_scraper = WebScraper()
    web_scraper.search_and_click(search_data)
"""
