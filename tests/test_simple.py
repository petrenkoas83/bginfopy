import sys
import os
sys.path.append(os.path.join(sys.path[0], '../bginfopy'))
import __init__ as init

def test_image_class():
    test_img = init.Image('')
    assert not test_img.file_exist