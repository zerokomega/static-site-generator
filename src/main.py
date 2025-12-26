

from copy_contents import copy_contents
from generate_pages_recursive import generate_pages_recursive





def main():
    # text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(text_node)
    source = "./static"
    dest = "./public"
    copy_static_to_public = copy_contents(source, dest)
    print(copy_static_to_public)
    content_dir = "./content"
    template_html = "./template.html"
    public_dir = "./public"
    generate_pages_recursive(content_dir, template_html, public_dir)


main()
