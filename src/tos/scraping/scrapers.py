# ToS: A tool to analyze Terms of Service.
# Copyright (C) 2024 José María Cruz Lorite
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class HtmlTermsScraper:
    """This class is used to scrape terms from a given URL.
    
    Make sure to call the init method before scraping and the close method after scraping.
    
    Attributes:
        url (str): The URL to scrape.
        wait_time (int): The time to wait for the page to load.
        headless (bool): Whether to run the browser in headless mode.
        driver (WebDriver): The Selenium WebDriver.
    """
    
    def __init__(self, wait_time: int = 3, headless: bool = True):
        self.wait_time = wait_time
        self.headless = headless
        self.driver = None
    
    def init(self):
        options = Options()
        options.headless = self.headless
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(self.wait_time)
    
    def get(self, url: str):
        self.driver.get(url)
    
    def get_page_source(self, url: str):
        self.get(url)
        return self.driver.page_source
    
    def select_element(self, xpath, class_name="__tos_selected__"):
        """Add a class ('__tos_selected__' by default) to the element, its
        descendants and its parents.
        
        Args:
            xpath (str): The XPath of the element to select.
            class_name (str): The class name to add to the element.
        """
        element = self.driver.find_element(By.XPATH, xpath)
        descendants = element.find_elements(By.XPATH, ".//*")
        ancestors = self.driver.find_elements(By.XPATH, xpath + "/ancestor::*")
        for ele in descendants + ancestors + [element]:
            self.driver.execute_script(f"arguments[0].classList.add('{class_name}')", ele)
    
    def close(self):
        self.driver.quit()