import os
import shutil

def copy_contents(source, destination):
    pass
    if not os.path.exists(os.path.abspath(source)):
        return f'Error: source "{source}" not found.'
    if not os.path.exists(os.path.abspath(destination)):
        return f'Error: destination "{destination}" not found.'
    


