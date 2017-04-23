import sys
import os
sys.path.append(os.path.join(sys.path[0], '../bginfopy'))
import __init__ as init

def test_image_class():
    test_img = init.Image('')
    assert not test_img.file_exist
    assert not test_img.file_name
    test_img.full_path = os.path.join(sys.path[0], '../tests/test_simple.py')
    assert test_img.file_exist
    assert test_img.directory_path == os.path.join(sys.path[0], '../tests')
    assert test_img.file_full_name == 'test_simple.py'
    assert test_img.file_name == 'test_simple'
    assert test_img.file_ext == '.py'