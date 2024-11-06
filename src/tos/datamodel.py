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

import enum

from pydantic import BaseModel


class TermUnfairnessType(str, enum.Enum):
    """Defines the type of unfair term"""
    
    LTD = "limitation_of_liability"
    TER = "termination"
    CH  = "unilateral_change"
    CR  = "content_removal"
    USE = "contract_by_using"
    LAW = "choice_of_law"
    J   = "jurisdiction"
    A   = "arbitration"


class TermUnfairnessScoring(dict[TermUnfairnessType, float]):
    """TermUnfairness class is a dictionary that maps a float value from
    0 to 1 to a TermUnfairnessType, which is an enum that defines the type of
    unfair term.
    """

    def __setitem__(self, key: TermUnfairnessType, value: float):
        if not isinstance(key, TermUnfairnessType):
            raise ValueError(f"Value '{key}' is not a valid TermUnfairnessType")
        if not isinstance(value, float):
            raise ValueError(f"Key '{value}' is not a valid float")
        if value < 0 or value > 1:
            raise ValueError(f"Key '{value}' is not between 0 and 1")
        super().__setitem__(key, value)


class TermMeta(BaseModel):
    """Metadata for a term."""
    word_count: int
    headings: list[str]


class Term(BaseModel):
    """A term in a document."""
    text: str
    meta: TermMeta


class TosDocumentMeta(BaseModel):
    """Metadata for a document."""
    
    name: str
    word_count: int
    section_count: int


class TosDocument(BaseModel):
    """A document containing terms of service."""
    
    terms: list[Term]
    meta: TosDocumentMeta

