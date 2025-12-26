
import sys
from copy_contents import copy_contents
from generate_pages_recursive import generate_pages_recursive





def main():
    basepath = '/'
    if sys.argv:
        basepath = sys.argv[0]
    

    source = "./static"
    dest = "./docs"
    copy_static_to_public = copy_contents(source, dest)
    print(copy_static_to_public)
    content_dir = "./content"
    template_html = "./template.html"
    public_dir = "./docs"
    generate_pages_recursive(content_dir, template_html, public_dir, basepath)


main()
