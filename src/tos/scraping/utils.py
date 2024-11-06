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

import typing

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def xpath_for_bs4(element):
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: bs4.element.Tag
    :return: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = (
    ...     '<?xml version="1.0" encoding="UTF-8"?>'
    ...     '<doc xmlns:ns1="http://localhost/ns1"'
    ...     '     xmlns:ns2="http://localhost/ns2">'
    ...     '<ns1:elm/><ns2:elm/><ns2:elm/></doc>'
    ...     )
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.find('ns2:elm').next_sibling)
    '/doc/ns2:elm[2]'
    """
    components = []
    target = element if element.name else element.parent
    for node in (target, *target.parents)[-2::-1]:
        tag = '%s:%s' % (node.prefix, node.name) if node.prefix else node.name
        siblings = node.parent.find_all(tag, recursive=False)
        components.append(tag if len(siblings) == 1 else '%s[%d]' % (tag, next(
            index
            for index, sibling in enumerate(siblings, 1)
            if sibling is node
            )))
    return ('/%s' % '/'.join(components)).replace("[1]", "")

def xpath_for_element(element: WebElement) -> str:
    """Get the xpath of an element
    Args:
        element: Selenium WebElement
    Returns:
        str: The xpath of the element
    """
    e = element
    xpath = ""
    while e.tag_name != "html":
        parent = e.find_element(By.XPATH, "..")
        neighbours = parent.find_elements(By.XPATH, e.tag_name)
        level = e.tag_name + "[" + str(neighbours.index(e)+1) + "]"
        xpath = level + "/" + xpath
        e = parent
    return ("/html/" + xpath[:-1]).replace("[1]", "")
