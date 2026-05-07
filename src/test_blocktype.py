import unittest

from blocks import *

class TestBlockType(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is **bolded** paragraph


   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        blocks = [
            "# This is a heading",
            "## This is also a heading",
            "### And so it goes",
            "#### And it must never stop",
            "##### Except iff",
            "###### We reach the very last heading",
        ]
        block_types = list(map(block_to_block_type, blocks))
        self.assertListEqual(
            block_types,
            [BlockType.HEADING] * 6
        )

    def test_block_to_block_type_code(self):
        block = """```
if this_be_code do:
    nuffin. We din' do nuffin.
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        block = """>This is a quote
>by Albert Einstein, who said once:
>fldsmdfrrrrfllffmfrr mllmmmmfllm mlllffllm flllmmm fr fr"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_list(self):
        block = """- This is an unordered list
- by Albert Einstein, who said once:
- fldsmdfrrrrfllffmfrr mllmmmmfllm mlllffllm flllmmm fr fr"""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        block = """1. This is an ordered list
2. by Albert Einstein, who said once:
3. fldsmdfrrrrfllffmfrr mllmmmmfllm mlllffllm flllmmm fr fr
4. After he said that
5. it is said that
6. he denied he ever said that
7. which is sad, that..."""
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_strip_markdown_formatting_ordered_list(self):
        block = """1. This is an ordered list
2. by Albert Einstein, who said once:
3. fldsmdfrrrrfllffmfrr mllmmmmfllm mlllffllm flllmmm fr fr
4. After he said that
5. it is said that
6. he denied he ever said that
7. which is sad, that..."""
        stripped_block = strip_markdown_formatting(block, BlockType.ORDERED_LIST)
        self.assertEqual(
            stripped_block,
            [
                "This is an ordered list",
                "by Albert Einstein, who said once:",
                "fldsmdfrrrrfllffmfrr mllmmmmfllm mlllffllm flllmmm fr fr",
                "After he said that",
                "it is said that",
                "he denied he ever said that",
                "which is sad, that..."
            ]
        )

    def test_strip_markdown_formatting_heading(self):
        blocks = [
            "# This is a heading",
            "## This is a heading",
            "### This is a heading",
            "#### This is a heading",
            "##### This is a heading",
            "###### This is a heading",
        ]
        block_stripped = [strip_markdown_formatting(b, BlockType.HEADING) for b in blocks]
        self.assertListEqual(
            block_stripped,
            [["This is a heading"]] * 6
        )
    
    def test_block_to_html_code_oneline_paragraph(self):
        block = "Some paragraph with some **FAT** lettering"
        block_type = BlockType.PARAGRAPH
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<p>Some paragraph with some <b>FAT</b> lettering</p>"
        )
    
    def test_block_to_html_code_twoline_paragraph(self):
        block = "Some paragraph with some **FAT** lettering\nand an enter"
        block_type = BlockType.PARAGRAPH
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<p>Some paragraph with some <b>FAT</b> lettering and an enter</p>"
        )
    
    def test_block_to_html_code_code(self):
        block = """```
Some code block with some **NOT FAT** lettering
which _shouldn't_ be fat.
```"""
        block_type = BlockType.CODE
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<pre><code>Some code block with some **NOT FAT** lettering\nwhich _shouldn't_ be fat.\n</code></pre>"
        )

    def test_block_to_html_code_heading(self):
        block = "## Some heading with some **FAT** lettering"
        block_type = BlockType.HEADING
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<h2>Some heading with some <b>FAT</b> lettering</h2>"
        )

    def test_block_to_html_code_quote(self):
        block = """>**This** is a quote
>by Albert Einstein, who said once:
>fldsmdfrrrrfllffmfrr"""
        block_type = BlockType.QUOTE
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<blockquote><b>This</b> is a quote by Albert Einstein, who said once: fldsmdfrrrrfllffmfrr</blockquote>"
        )

    def test_block_to_html_code_unordered_list(self):
        block = """- **This** is an unordered list
- by Albert Einstein, who said once:
- fldsmdfrrrrfllffmfrr"""
        block_type = BlockType.UNORDERED_LIST
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<ul><li><b>This</b> is an unordered list</li><li>by Albert Einstein, who said once:</li><li>fldsmdfrrrrfllffmfrr</li></ul>"
        )

    def test_block_to_html_code_ordered_list(self):
        block = """1. **This** is an ordered list
2. by Albert Einstein, who said once:
3. fldsmdfrrrrfllffmfrr"""
        block_type = BlockType.ORDERED_LIST
        parentnode = block_to_html_node(block, block_type)
        self.assertEqual(
            parentnode.to_html(),
            "<ol><li><b>This</b> is an ordered list</li><li>by Albert Einstein, who said once:</li><li>fldsmdfrrrrfllffmfrr</li></ol>"
        )
    

    def test_markdown_to_html(self):
        md = """
# This is a heading

This is **bolded** paragraph


   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

- This is a list
- with items
"""
        html = markdown_to_html(md)
        self.assertEqual(
            html.to_html(),
            "<div><h1>This is a heading</h1><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here This is the same paragraph on a new line</p><ul><li>This is a list</li><li>with items</li></ul></div>"
        )

if __name__ == "__main__":
    unittest.main()