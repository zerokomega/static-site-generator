import os
from extract_title import extract_title
from markdown_to_html import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath='/') :
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    from_md = ""
    template = ""
    with open(from_path, 'r') as f:
        from_md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    node = markdown_to_html_node(from_md)
    from_html = node.to_html()
    title = extract_title(from_md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", from_html)
    template = template.replace('href="/', 'href="{basepath}')
    template = template.replace('src="/', 'src="{basepath}')
    abs_dest_path = os.path.abspath(dest_path)
    if not os.path.exists(os.path.dirname(abs_dest_path)):
        os.makedirs(os.path.dirname(abs_dest_path))
    with open(abs_dest_path, 'w') as f:
        f.write(template)
    
    