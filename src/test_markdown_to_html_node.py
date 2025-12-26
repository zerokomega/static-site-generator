import unittest


from blocktype import BlockType, block_to_block_type
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_headers(self):
        md = """
## This is a header 2 line

#### And this is a header 4 line

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a header 2 line</h2><h4>And this is a header 4 line</h4></div>"
        )

    def test_quotes(self):
        md = """
> Are we doing quotes now?

> Fine, let's do quotes now.

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Are we doing quotes now?</blockquote><blockquote>Fine, let's do quotes now.</blockquote></div>"
        )

    if __name__ == "__main__":
        unittest.main()