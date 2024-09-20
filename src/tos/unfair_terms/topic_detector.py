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







class UnfairTermTopicDetector:
    """This class is used to detect the topic of a given term"""
    
    def __init__(self, model_name="term_topic_detection"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dataset = None
        self._load_dataset()
    
    
class UnfairTermTopicSentenceTransformerFinetuning:
    """This class is used to finetune a Sentence Transformer model on the Term Topic dataset."""
    
    def __init__(self, model_name="roberta-base"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dataset = None
        self._load_dataset()
        
    def _load_dataset(self):
        dataset_path = os.path.join(os.getcwd(), "tos", "unfair_terms", "dataset.json")
        if os.path.exists(dataset_path):
            with open(dataset_path, "r") as f:
                self.dataset = json.load(f)
        else:
            print("Dataset file not found")
            exit(1)