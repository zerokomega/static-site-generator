from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    match block[0]:
        case "#":
            return BlockType.HEADING
        case "`":
            if block.startswith("```") and block.endswith("```"):
                return BlockType.CODE
            else:
                return BlockType.PARAGRAPH
        case ">":
            return BlockType.QUOTE
        case "-":
            if block[1] == " ":
                return BlockType.UNORDERED_LIST
            else:
                return BlockType.PARAGRAPH
        case "1":
            if block.startswith("1. "):
                return BlockType.ORDERED_LIST
            else:
                return BlockType.PARAGRAPH
        case _:
            return BlockType.PARAGRAPH