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

import io

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from docling_core.types.doc import GroupItem, DocItem
from docling_core.transforms.chunker import HierarchicalChunker

from tos.datamodel import TermMeta, Term, TosDocumentMeta, TosDocument
from tos.scraping import HtmlTermsScraper



class TosHierarchicalReader:
    """Reads a Terms of Service document and returns a TosDocument."""
    
    def __init__(self):
        """Initialize the reader."""
        self._scraper = HtmlTermsScraper()
        self._scraper.init()
        
    def __del__(self):
        self._scraper.close()

    def read_url(self, url: str) -> TosDocument:
        """Read the Terms of Service from the URL.
        
        Args:
            url (str): The URL to read.
        """
        html_content = self._scraper.get_page_source(url)
        bytesio = io.BytesIO(bytes(html_content, "utf-8"))
        dstream = DocumentStream(name=url, stream=bytesio)
        
        converter = DocumentConverter()
        result = converter.convert(dstream)
        chunks = list(HierarchicalChunker().chunk(result.document))

        terms = []
        for chunk in chunks:
            term = Term(
                text=chunk.text,
                meta=TermMeta(
                    word_count=len(chunk.text.split()),
                    headings=chunk.meta.headings if chunk.meta.headings else [])
            )
            terms.append(term)
        
        doc_meta = TosDocumentMeta(
            name=url,
            word_count=sum([term.meta.word_count for term in terms]),
            section_count=len(set([heading for term in terms for heading in term.meta.headings]))
        )
        
        return TosDocument(terms=terms, meta=doc_meta)
