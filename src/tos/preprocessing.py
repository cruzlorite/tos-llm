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

from html import unescape
from bs4 import BeautifulSoup, NavigableString, Comment

from tos.scraping.utils import xpath_for_bs4


class TextElementsExtractor:
    """Extract all text elements from a HTML page."""
    
    DECOMPOSE_ELEMENTS = [
        'iframe', 'script', 'style', 'svg', 'input', 'select', 'textarea', 'noscript']
    
    BREAKING_ELEMENTS = [
        'div', 'p', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol', 'ul', 'table',
        'tr', 'td', 'th', 'thead', 'tbody', 'tfoot', 'caption', 'colgroup', 'col', 'dl', 'dt',
        'dd', 'address', 'article', 'aside', 'blockquote', 'details', 'dialog', 'figcaption',
        'figure', 'footer', 'header', 'main', 'nav', 'section', 'summary'
    ]
    
    def __init__(self, strip=True):
        self.strip = strip

    def _extract_content(self, parent, page_element, elements):
        """Recursively extract all string elements from a page element."""
        if page_element.name in self.BREAKING_ELEMENTS:
            elements += [{"text": "\n", "xpath": None}]
        if isinstance(page_element, Comment):
            # Comments are not considered as text elements
            return
        if isinstance(page_element, NavigableString):
            if self.strip:
                page_element = " ".join([line.strip() for line in page_element.splitlines()])
            if len(page_element) > 0:
                elements += [{
                    "text": page_element,
                    "xpath": xpath_for_bs4(parent)
                }]
        else:
            for child in page_element.children:
                self._extract_content(page_element, child, elements)
                
    def _shared_prefix(self, xpaths):
        """Return the shared prefix of a list of xpaths."""
        prefix = xpaths[0]
        for xpath in xpaths[1:]:
            for i in range(min(len(prefix), len(xpath))):
                if prefix[i] != xpath[i]:
                    prefix = prefix[:i]
                    break
        return prefix

    def extract(self, html):
        """Extract all string elements from a HTML page."""
        soup = BeautifulSoup(unescape(html), "html.parser")
        
        for element in soup.find_all():
            if element.name in self.DECOMPOSE_ELEMENTS:
                element.decompose()
        
        elements = []
        self._extract_content(None, soup, elements)
        return elements
    
    def simplify_elements(self, elements):
        """The process of simplifying the elements consists in three steps:
        1. Remove all elements that are empty.
        2. Merge all elements that are separated by a newline character.
           The xpath of the merged element is the xpath of the first element.
        3. Remove contiguous elements that have xpath=None.
        """
        elements = [element for element in elements if element["text"].strip() != "" or element["text"] == "\n"]
        
        grouped_elements = [[]]
        for element in elements:
            if element["xpath"] == None:
                grouped_elements.append([])
            else:
                grouped_elements[-1].append(element)
        
        simplified_elements = []
        for group in grouped_elements:
            if len(group) == 0:
                continue
            text = "".join([element["text"] for element in group])
            xpath = self._shared_prefix([element["xpath"] for element in group])
            # remove trailing '[' if it exists
            if xpath[-1] == "[":
                xpath = xpath[:-1]
            simplified_elements.append({"text": text, "xpath": xpath})
        
        return simplified_elements

    def extract_and_simplify(self, html):
        """Extract and simplify all string elements from a HTML page."""
        elements = self.extract(html)
        return self.simplify_elements(elements)
        
