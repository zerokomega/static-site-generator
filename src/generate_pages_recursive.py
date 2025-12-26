import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) :
    os.makedirs(dest_dir_path, exist_ok=True)

    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(content_path) and item.endswith('.md'):
            html_path = dest_path.replace('.md', '.html')
            generate_page(content_path, template_path, html_path)
        elif os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path)
    

    
    