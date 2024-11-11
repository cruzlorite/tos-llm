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

from tos.utils import load_dataset_tos30
from tos.readers import TosHierarchicalReader


def read_tos(url: str):
    """Read the Terms of Service from the URL.
    
    Args:
        url (str): The URL to read.
    """
    reader = TosHierarchicalReader()
    return reader.read(url)
    
    
if __name__ == "__main__":
    # get list of URLs
    urls = load_dataset_tos30()
    
    
    
    
    print(urls)