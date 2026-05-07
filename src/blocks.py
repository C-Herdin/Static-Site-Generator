from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    r"""Return a list of blocks split at \n\n and stripped of trailing \n and spaces"""
    return [p.strip("\n ") for p in markdown.split("\n\n")]

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    by_line = block.split("\n")
    if len(by_line) == len([1 for l in by_line if l.startswith(">")]):
        return BlockType.QUOTE
    if len(by_line) == len([1 for l in by_line if l.startswith("- ")]):
        return BlockType.UNORDERED_LIST
    if len(by_line) == len([1 for i,l in enumerate(by_line) if l.startswith(f"{i+1}. ")]):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def strip_markdown_formatting(block, block_type):
    by_line = block.split("\n")
    match block_type:
        case BlockType.PARAGRAPH:
            return [block.replace("\n", " ")]
        case BlockType.HEADING:
            return [block.strip("# ")]
        case BlockType.CODE:
            return [block.removeprefix("```\n").removesuffix("```")]
        case BlockType.QUOTE:
            return [" ".join([line.lstrip("> ") for line in by_line])]
        case BlockType.UNORDERED_LIST:
            return [line.removeprefix("- ") for line in by_line]
        case BlockType.ORDERED_LIST:
            return [line.split(None, 1)[1] for line in by_line]
        case _:
            raise ValueError("unknown Block Type")


def block_to_html_node(block, block_type):
    raw_text_list = strip_markdown_formatting(block, block_type)
    if block_type == BlockType.CODE:
        # avoid unnecessary conversion of childnodes
        return ParentNode("pre", [LeafNode("code", *raw_text_list)])
    
    # list of (lists of textnodes for each line)
    textnodes_by_line = list(map(text_to_textnodes, raw_text_list))
    # list of (lists of leafnodes for each line)
    childnodes_by_line = [list(map(text_node_to_html_node, l)) for l in textnodes_by_line]
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", *childnodes_by_line)
        case BlockType.HEADING:
            heading_number = len(block.split(None, 1)[0])
            return ParentNode(f"h{heading_number}", *childnodes_by_line)
        case BlockType.QUOTE:
            return ParentNode("blockquote", *childnodes_by_line)
        case BlockType.UNORDERED_LIST:
            list_members = [ParentNode("li", line) for line in childnodes_by_line]
            return ParentNode("ul", list_members)
        case BlockType.ORDERED_LIST:
            list_members = [ParentNode("li", line) for line in childnodes_by_line]
            return ParentNode("ol", list_members)
        case _:
            raise ValueError("unknown Block Type")
        
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.removeprefix("# ").strip()
    raise Exception("no header found")

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown) # a list of strings
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(block_to_html_node(block, block_type))
    return ParentNode("div", html_nodes)