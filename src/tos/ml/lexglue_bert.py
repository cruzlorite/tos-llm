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

from typing import List

import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

from tos.models import TermUnfairnessType
from tos.models import TermUnfairnessScoring
from tos.ml import TermUnfairnessClassifier


class LexglueBertClassifier(TermUnfairnessClassifier):
    """This classifier uses a fined-tuned version of BERT on the LEXGLUE dataset
    to classify terms."""
    
    HF_MODEL = "marmolpen3/lexglue-unfair-tos"
    
    def __init__(self):
        super().__init__()
        self._tokenizer = AutoTokenizer.from_pretrained(self.HF_MODEL)
        self._model = AutoModelForSequenceClassification.from_pretrained(self.HF_MODEL)

    def classify(self, term: str) -> TermUnfairnessScoring:
        inputs = self._tokenizer(term, return_tensors="pt")
        outputs = self._model(**inputs)
        logits = torch.sigmoid(outputs.logits)
        return TermUnfairnessScoring({
            TermUnfairnessType.LTD: logits[0][0].item(),
            TermUnfairnessType.TER: logits[0][1].item(),
            TermUnfairnessType.CH:  logits[0][2].item(),
            TermUnfairnessType.CR:  logits[0][3].item(),
            TermUnfairnessType.USE: logits[0][4].item(),
            TermUnfairnessType.LAW: logits[0][5].item(),
            TermUnfairnessType.J:   logits[0][6].item(),
            TermUnfairnessType.A:   logits[0][7].item(),
        })
    
    def classify_batch(self, terms: List[str]) -> List[TermUnfairnessScoring]:
        inputs = self._tokenizer(terms, return_tensors="pt", padding=True, truncation=True)
        outputs = self._model(**inputs)
        logits = outputs.logits
        return [TermUnfairnessScoring(logits=logit) for logit in logits]
    
    
    