#!/usr/bin/env python3
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

import os
import json
import argparse

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

import PySimpleGUI as sg

from tos.core.utils import read_resource_file
from tos.scraping.utils import xpath_for_element


def parse_args():
    parser = argparse.ArgumentParser(description='Annotate real world HTML documents to generate a dataset for the model.')
    parser.add_argument('-i', '--input-list', required=False, type=str, help='The file containing the list of URLs to annotate. Each URL should be in a new line.')
    parser.add_argument('-o', '--output', required=False, type=str, help='The file where to save the annotated data.')
    return parser.parse_args()

def render_url(driver, url):
    """Render the URL in the browser and return the page source
    Args:
        driver: Selenium WebDriver
        url: URL to render
    """
    driver.get(url)
    import time
    time.sleep(2)

    # get all elements, excluding html, body, style, script and head, or their children
    elements = driver.find_elements(By.XPATH, "//*[not(self::html or self::style or self::script or self::head or self::body) and not(ancestor::style or ancestor::script or ancestor::head)]")

    # set the class __selected__ with background color purple. Add !important
    driver.execute_script("""\
    var style = document.createElement('style');
    style.innerHTML = '.__selected__ {border-radius: 3px !important; border-style: solid !important; border-color: purple !important; background-color: rgba(128, 0, 128, 0.2) !important;}';
    document.head.appendChild(style);
    """)

    for element in elements:
        driver.execute_script("""\
        arguments[0].addEventListener("click", function onclick(e) {
            if (e.ctrlKey && (e.target === e.currentTarget)) {
                if (this.classList.contains("__selected__")) {
                    this.classList.remove("__selected__");
                } else {
                    this.classList.add("__selected__");
                }
            }
        });
        """, element)

def get_selected_elements(driver):
    """Get XPATH of selected elements
    Args:
        driver: Selenium WebDriver
    Returns:
        List of selected elements xpath
    """
    selected_elements = driver.find_elements(By.CSS_SELECTOR, '.__selected__')
    return [xpath_for_element(elm) for elm in selected_elements]

def export_dataset(output_file, data):
    """Export the annotated data to a file
    Args:
        output_file: The file to save the annotated data
        data: The annotated data
    """
    with open(output_file, 'w') as f:
        f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    args = parse_args()
    
    # if the input file does not exist, use the default file
    if args.input_list is None:
        print('Input file does not exist, using the default file: tos.resources.datasets.tos_url_list.txt')
        urls = read_resource_file('tos.resources.datasets', 'tos_url_list.txt').splitlines()
    else:
        with open(args.input_list) as f:
            urls = f.readlines()
            
    # if the output file does not exist, use the default file
    if args.output is None:
        print('Output file not provided, using the default file: tos_content_dataset.json')
        args.output = 'tos_content_dataset.json'
    
    # strip the urls
    urls = [x.strip() for x in urls]
    
    # Instantiate the Firefox WebDriver
    options = Options()
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(3)
    
    # define layout
    layout = [
        [sg.Button('Next URL'),
         sg.Button('Finish and Export Dataset')]
    ]

    # Create the Window
    window = sg.Window('ToS annotation tool', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    dataset = {}
    index = -1
    attempt = 0
    while True:
        event, values = window.read()
        
        # if event is not None save the selected elements
        is_event = event == sg.WIN_CLOSED or event == 'Finish and Export Dataset' or event == 'Next URL'
        if is_event and index >= 0 and index < len(urls):
            dataset[urls[index]] = get_selected_elements(driver)
            
        if event == sg.WIN_CLOSED or event == 'Finish and Export Dataset':
            export_dataset(args.output, dataset)
            break
        elif event == 'Next URL' and (index+1) < len(urls):
            index += 1
            try:
                render_url(driver, urls[index])
                print('Rendered URL ', urls[index])
                attempt = 0
            except:
                print('Error rendering URL ', urls[index], ' retrying... (attempt ', attempt, '/5)')
                import traceback
                traceback.print_exc()
                
                attempt += 1
                if attempt == 5:
                    print('Failed to render URL ', urls[index], ' skipping...')
                    attempt = 0
                else:
                    index -= 1

    driver.quit()
    window.close()