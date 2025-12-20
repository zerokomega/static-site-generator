from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("missing tag")
        if self.children == None:
            raise ValueError("missing children")
        child_line = ""
        for child in self.children:
            child_line = child_line + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_line}</{self.tag}>"