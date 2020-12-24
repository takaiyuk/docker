from PIL import Image

path = "tests/images/capybara_horizontal_rotation_trim.jpg"


def test_image_open():
    Image.open(path)
