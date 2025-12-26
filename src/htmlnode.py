

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        if self.props:
            for key in self.props:
                prop_string += f' {key}="{self.props[key]}"'
        return prop_string

    def __repr__(self):
        print(f"Tag: {self.tag} \nValue: {self.value} \nChildren: {self.children} \nProps: {self.props}")