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

from tos.unfair_terms.topic_detector import UnfairTermTopicDetector


class UnfairTermChecker:
    """This class is used to check if a given term is unfair"""
    
    def __init__(self, model_name="term_topic_detection"):
        self.topic_detector = UnfairTermTopicDetector(model_name)
        self.prompts = {}
        self._load_prompts()
        
    def _load_prompts(self):
        """Load the prompts from res/prompts/unfair_terms/*.txt"""
        pass
    
    def check(self, term):
        """Check if a given term is unfair"""
        topic = self.topic_detector.detect(term)
        
        prompt = self.prompts.get(topic, None)
        
        if not prompt:
            print(f"No prompt found for this term (topic: {topic}): '{term}'")
        
        pass
    