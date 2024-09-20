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
import time
import argparse

import bs4

from selenium.webdriver.common.by import By

from tos.core.config import ConfigLoader
from tos.core.utils import print_disclaimer, read_resource_file
from tos.scraping.scraper import HtmlTermsScraper
from tos.scraping.preprocessing import TextElementsExtractor


def parse_args():
    parser = argparse.ArgumentParser(description="ToS: A tool to analyze Terms of Service.")
    parser.add_argument("-c", "--config", type=str, default="config.yaml", help="The configuration file.")
    parser.add_argument("-o", "--output-file", type=str, default="tso_content_text_elements.json", help="The output file.")
    return parser.parse_args()

def main():
    print_disclaimer()
    
    args = parse_args()
    config_file = args.config
    output_file = args.output_file
    
    # load the configuration file
    config = ConfigLoader().load_config(config_file)
    print("Configuration loaded successfully from", config_file)
    
    # load resouce file tos.resources.datasets.tos_content_dataset.json
    tos_content_dataset = read_resource_file("tos.resources.datasets", "tos_content_dataset.json")
    tos_content_dataset = json.loads(tos_content_dataset)
    print("Resource tos_content_dataset.json loaded successfully")
    
    # check if output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory {output_dir} does not exist. Please create it and try again.")
    
    # scrape the terms of service
    scraper = HtmlTermsScraper()
    extractor = TextElementsExtractor()
    scraper.init()
    page_sources = {}
    for url, xpaths in tos_content_dataset.items():
        try:
            scraper.get(url)
            time.sleep(3)

            for xpath in xpaths:
                scraper.select_element(xpath)
            
            source = scraper.get_page_source()
            text_elements = extractor.extract_and_simplify(source)
            
            for te in text_elements:
                # if te["xpath"] starts with one of the xpaths in xpaths, then te["is_selected"] = True
                is_selected = False
                for xpath in xpaths:
                    if te["xpath"] and te["xpath"].startswith(xpath):
                        is_selected = True
                        break
                te["is_selected"] = is_selected

            page_sources[url] = {
                "page_source": source,
                "text_elements": text_elements
            }
        except Exception as e:
            print(f"Error while scraping {url}: {e}")
        
    # save the scraped data
    with open(output_file, "w") as f:
        json.dump(page_sources, f, indent=4)

    scraper.close()
    
if __name__ == "__main__":
    main()