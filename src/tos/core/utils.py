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

from importlib import resources as impresources


def print_disclaimer():
    print("ToS Copyright (C) 2024 José María Cruz Lorite")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions. See the GNU GPLv3 for details.")
    print("")

def read_resource_file(package, filename):
    """Read resource file embedded in the package.
    
    Args:
        package (str): The package name.
        filename (str): The filename.
    Returns:
        str: The file content.
    """
    return impresources.read_text(package, filename)

def load_prompt_from_resource(prompt_name):
    """Load the prompt from the resource file.
    
    Args:
        prompt_name (str): The prompt filename without the extension.
    """
    template = read_resource_file("tos.resources.prompts", f"{prompt_name}.txt")