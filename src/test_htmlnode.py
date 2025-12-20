import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_default_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_eq_tag(self):
        node = HTMLNode("a")
        node2 = HTMLNode(tag="a")
        self.assertEqual(node.tag, node2.tag)
    
    def test_not_eq_tag(self):
        node = HTMLNode()
        node2 = HTMLNode(tag="a")
        self.assertNotEqual(node.tag, node2.tag)

    if __name__ == "__main__":
        unittest.main()