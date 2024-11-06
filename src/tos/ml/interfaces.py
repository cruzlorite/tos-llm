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

from tos.models import TermUnfairnessScoring


class TermUnfairnessClassifier:
    """Base class for term unfairness classifiers."""
    
    def classify(self, term: str) -> TermUnfairnessScoring:
        """Evaluates the degree of unfairness of a given term."""
        raise NotImplementedError()
    
    def classify_batch(self, term: List[str]) -> List[TermUnfairnessScoring]:
        """Evaluates the degree of unfairness of a given list of terms."""
        raise NotImplementedError()
    