import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Click here",
            props={"href": "https://example.com", "target": "_blank"}
        )
        expected = 'href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="Content")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="img", props={"src": "image.png"})
        self.assertEqual(node.props_to_html(), 'src="image.png"')

    def test_node_initialization(self):
        node = HTMLNode(
            tag="p",
            value="Test content",
            children=[],
            props={"class": "test"}
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "test"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_node_initialization(self):
        node = LeafNode(
            tag="p",
            value="Test content",
            props={"class": "test"}
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Test content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "test"})

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_repeated_grandchildren_and_props(self):
        grandchild_node1 = LeafNode("img", "Ich bin ein Mensch", {"src": "image.png"})
        child_node1 = ParentNode("span", [grandchild_node1], {"some": "thing"})
        parent_node = ParentNode("p", [grandchild_node1, child_node1])
        self.assertEqual(
            parent_node.to_html(),
            '<p><img src="image.png">Ich bin ein Mensch</img><span some="thing"><img src="image.png">Ich bin ein Mensch</img></span></p>'
        )

if __name__ == "__main__":
    unittest.main()