from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from blocktype import BlockType, block_to_block_type
import re

def text_node_to_html_node(text_node):
    if text_node.text_type is not TextType.CODE:
        text_node.text = text_node.text.replace("\n", " ")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        temp_nodes = []
        split_old_node = node.text.split(delimiter)
        if (len(split_old_node) % 2) == 0:
            raise Exception("invalid Markdown syntax")
        for i in range(0, len(split_old_node)):
            if i % 2 == 0:
                temp_nodes.append(TextNode(split_old_node[i], node.text_type))
            else:
                temp_nodes.append(TextNode(split_old_node[i], text_type))
        new_nodes.extend(temp_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        temp_nodes = [node]
        image_alt = ""
        image_link = ""
        markdown_images = extract_markdown_images(node.text)
        for image in markdown_images:
            image_alt, image_link = image[0], image[1]
            split_old_node = temp_nodes.pop().text.split(f"![{image_alt}]({image_link})", 1)
            temp_nodes.append(TextNode(split_old_node[0], TextType.TEXT))
            temp_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if len(split_old_node) > 1:
                if len(split_old_node[1]) > 0:
                    temp_nodes.append(TextNode(split_old_node[1], TextType.TEXT))
        new_nodes.extend(temp_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        temp_nodes = [node]
        link_alt = ""
        link_link = ""
        markdown_links = extract_markdown_links(node.text)
        for link in markdown_links:
            link_alt, link_link = link[0], link[1]
            split_old_node = temp_nodes.pop().text.split(f"[{link_alt}]({link_link})", 1)
            temp_nodes.append(TextNode(split_old_node[0], TextType.TEXT))
            temp_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            if len(split_old_node) > 1:
                if len(split_old_node[1]) > 0:
                    temp_nodes.append(TextNode(split_old_node[1], TextType.TEXT))
        new_nodes.extend(temp_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for i in range(0, len(text)):
        match text[i]:
            case "*":
                if text[i - 1] == "*":
                    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
            case "_":
                nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
            case "`":
                nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
            case "[":
                if text[i - 1] == "!":
                    nodes = split_nodes_image(nodes)
                else:
                    nodes = split_nodes_link(nodes)
                
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(0, len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == "":
            blocks.remove("")
    return blocks

def get_heading_level(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    return block[level + 1:], level

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes = text_to_children(block)
        match block_type:
            case BlockType.PARAGRAPH:
                node = paragraph_to_html_node(block)
            case BlockType.HEADING:
                node = heading_to_html_node(block)
            case BlockType.QUOTE:
                node = quote_to_html_node(block)
            case BlockType.CODE:
                node = code_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                node = ulist_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = olist_to_html_node(block)
            case _:
                raise ValueError("invalid block type")        
        html_nodes.append(node)
    parent_node = ParentNode("div", html_nodes, None)
    return parent_node

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    lines = block.split("\n")
    text = "\n".join(lines[1:-1]) + "\n"
    raw_text_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(raw_text_node)
    return ParentNode("pre", [child])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)

main()
