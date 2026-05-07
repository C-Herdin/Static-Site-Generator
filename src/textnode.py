from enum import Enum
import re

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def _split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type is not TextType.TEXT:
            new_nodes.append(n)
            continue
        split_text = n.text.split(delimiter)
        if len(split_text) % 2 != 1:
            raise Exception("invalid Markdown syntax")
        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def _extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def _split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        md_images = _extract_markdown_images(n.text)
        if len(md_images) < 1:
            new_nodes.append(n)
            continue
        split_text = []
        current_text = n.text
        for desc, url in md_images:
            split_text.extend(current_text.split(f"![{desc}]({url})"))
            current_text = split_text.pop()
        split_text.append(current_text)
        for i, im in enumerate(md_images):
            if split_text[i] != "":
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            new_nodes.append(TextNode(im[0], TextType.IMAGE, im[1]))
        if split_text[-1] != "":
            new_nodes.append(TextNode(split_text[-1], TextType.TEXT))
    return new_nodes

def _split_nodes_links(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        md_links = _extract_markdown_links(n.text)
        if len(md_links) < 1:
            new_nodes.append(n)
            continue
        split_text = []
        current_text = n.text
        for desc, url in md_links:
            split_text.extend(current_text.split(f"[{desc}]({url})"))
            current_text = split_text.pop()
        split_text.append(current_text)
        for i, im in enumerate(md_links):
            if split_text[i] != "":
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            new_nodes.append(TextNode(im[0], TextType.LINK, im[1]))
        if split_text[-1] != "":
            new_nodes.append(TextNode(split_text[-1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    textnodes = _split_nodes_image([TextNode(text, TextType.TEXT)])
    textnodes = _split_nodes_links(textnodes)
    textnodes = _split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = _split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = _split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    return textnodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("unknown TextType")