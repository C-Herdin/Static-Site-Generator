from enum import Enum

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
    if len(by_line) == len(list(filter(None, [l.startswith(">") for l in by_line]))):
        return BlockType.QUOTE
    if len(by_line) == len(list(filter(None, [l.startswith("- ") for l in by_line]))):
        return BlockType.UNORDERED_LIST
    if len(by_line) == len(list(filter(None, [l.startswith(f"{i+1}. ") for i, l in enumerate(by_line)]))):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH