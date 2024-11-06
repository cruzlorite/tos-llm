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
from schema import Schema, SchemaError
import yaml


class ConfigLoader:
    """Class to load the configuration file and validate it"""
    
    CONFIG_SCHEMA = Schema({
        "huggingface": {
            "access_token": str,
        },
        "llm": {
            "provider": lambda s: s in ("OpenAI", "Llama"),
            "endpoint": str,
            "api_key": str,
            "model_name": lambda s: s in ("gpt-4-turbo"),
        }
    })
    
    def load_config(self, config_file):
        """Load the configuration file and validate it"""
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        
        try:
            self.CONFIG_SCHEMA.validate(config)
        except SchemaError as e:
            raise ValueError(f"Invalid configuration: {e}")
        
        return config