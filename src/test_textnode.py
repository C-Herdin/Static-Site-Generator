import unittest

from textnode import (TextNode, TextType,
                      text_node_to_html_node,
                      _split_nodes_delimiter,
                      _extract_markdown_links,
                      _extract_markdown_images,
                      _split_nodes_image,
                      _split_nodes_links,
                      text_to_textnodes,
                      )


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node!", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.LINK, "somelink.com")
        node5 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node4, node5)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "link.com"})
    
    def test_image(self):
        node = TextNode("This is an image description", TextType.IMAGE, "image/url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image/url", "alt": "This is an image description"})

    def test_delimiter_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        split_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [TextNode("This is a text node", TextType.TEXT)])

    def test_delimiter_bold(self):
        node = TextNode("This is a **bold text** node with **two bold** texts.", TextType.TEXT)
        split_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" node with ", TextType.TEXT),
            TextNode("two bold", TextType.BOLD),
            TextNode(" texts.", TextType.TEXT)
            ])
        
    def test_delimiter_italic(self):
        node = TextNode("This is a node with _italic_ text.", TextType.TEXT)
        split_nodes = _split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes, [
            TextNode("This is a node with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
            ])
        
    def test_delimiter_code(self):
        node = TextNode("This is a node with `some code`", TextType.TEXT)
        split_nodes = _split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("This is a node with ", TextType.TEXT),
            TextNode("some code", TextType.CODE)
            ])

    def test_extract_markdown_images(self):
        matches = _extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = _extract_markdown_links(
            "This is text with a [link](http://globalskywatch.com/chemtrails/ubbthreads.php?ubb=showflat&Number=45#Post45)"
        )
        self.assertListEqual([("link", "http://globalskywatch.com/chemtrails/ubbthreads.php?ubb=showflat&Number=45#Post45")], matches)

    def test_split_images_multi(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), with a dot to end it all.",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", with a dot to end it all.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_empty_begin(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is the image to behold.",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is the image to behold.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multi(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png), with a dot to end it all.",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(", with a dot to end it all.", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_link_empty_begin(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) is the link to behold.",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is the link to behold.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()