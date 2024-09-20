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

from tos.core.config import ConfigLoader
from tos.core.utils import print_disclaimer, read_resource_file
from tos.scraping.scraper import HtmlTermsScraper
from tos.scraping.preprocessing import TextElementsExtractor

print(read_resource_file("tos.resources.datasets", "tos_content_dataset.json"))

exit()

print_disclaimer()

config_loader = ConfigLoader()
config = config_loader.load_config("config.template.yaml")

scraper = HtmlTermsScraper()
scraper.init()
scraper.get("https://openai.com/policies/row-terms-of-use/")
source = scraper.get_page_source()
scraper.close()

extractor = TextElementsExtractor()
extracted_elements = extractor.extract_and_simplify(source)
for element in extracted_elements:
    if element["xpath"]:
        print(f"{element['xpath']}: {element['text']}")
