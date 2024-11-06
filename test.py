from docling.document_converter import DocumentConverter
from docling_core.types.doc import GroupItem, DocItem
from docling_core.transforms.chunker import HierarchicalChunker

source = "https://es.overleaf.com/legal#Cookies"
converter = DocumentConverter()
result = converter.convert(source)

chunks = list(HierarchicalChunker().chunk(result.document))

for chunk in chunks:
    if chunk.meta.headings:
        for ix, header in enumerate(chunk.meta.headings):
            print("#" * (ix + 1), header)
    else:
        print("# No headings")
    print(chunk.text)

# for ix, (item, level) in enumerate(result.document.iterate_items(with_groups=False)):
#     if isinstance(item, GroupItem):
#         print(" " * level, f"{ix}: {item.label.value} with name={item.name}")
#     elif isinstance(item, DocItem):
#         print(" " * level, f"{ix}: {item.label.value}")
        