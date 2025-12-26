import os
import shutil

def copy_contents(source, destination):
    abs_src = os.path.abspath(source)
    abs_dest = os.path.abspath(destination)
    if not os.path.exists(abs_src):
        return f'Error: source "{source}" not found.'
    if not os.path.exists(abs_dest):
        os.mkdir(abs_dest)
    shutil.rmtree(abs_dest)
    shutil.copytree(abs_src, abs_dest)
    return f'Copied contents of "{source}" to "{destination}"'


