from direct.showbase.ShowBase import ShowBase
from panda3d.core import PNMImage, Texture
from panda3d.core import GraphicsOutput as go
from panda3d.core import PTAUchar
from panda3d.core import CardMaker

import numpy as np


s = ShowBase()

# output_tex will be the "screenshot" texture that I want to use to stream
# Panda3D's output to OpenCV for video encoding.
output_img = PNMImage(base.win.get_x_size(), base.win.get_y_size())
output_tex = Texture()
output_tex.load(output_img)
base.win.add_render_texture(output_tex, go.RTM_copy_ram, go.RTP_color)


def extract_image(task):
    # pointer = output_tex.get_ram_image()
    # img_array = np.fromstring(pointer.get_data())
    # FIXME: The lines above do work. The ones below do not.
    pointer = output_tex.getRamImage().getData()
    img_array = np.frombuffer(pointer, np.uint32)
    return task.cont


# input_tex is the texture of a quad in the scene, on which the numpy array will
# be visible as coloration.
input_img = PNMImage(512, 512)  # It's RGB.
input_tex = Texture()
input_tex.load(input_img)
screen = render.attach_new_node(CardMaker('in_scene_screen').generate())
screen.set_pos(-0.5, 2, -0.5)
screen.set_texture(input_tex)

# Some functions that generate texture data on the numpy side. Each image is an
# x_size x y_size x color_depth matrix, with the last dimension being in BGR.
# Also, the x axis goes upwards in texture space. Y is still left to right.

def numpy_image_a(x_size, y_size, color_depth):
    return np.random.randint(0, 255, size=(x_size, y_size, color_depth), dtype=np.uint8)


def numpy_image_b(x_size, y_size, color_depth):
    return np.ones((x_size, y_size, color_depth), dtype=np.uint8) * 255


def numpy_image_c(x_size, y_size, color_depth):
    imgs = np.array([np.ones((x_size, y_size), dtype=np.uint8) * 255
                     for _ in range(color_depth)])
    print(imgs.shape)
    return imgs.transpose(1, 2, 0)


def numpy_image_d(x_size, y_size, color_depth):
    indices = np.indices((x_size, y_size))
    red = (indices[0] / float(x_size) * 255.0).astype(np.uint8)
    green = np.random.randint(0, 63, size=(x_size, y_size), dtype=np.uint8)
    # green = (indices[0] / float(y_size) * 255.0).astype(np.uint8)
    blue = (indices[1] / float(y_size) * 255.0).astype(np.uint8)
    return np.array([blue, green, red]).transpose(1, 2, 0)


def numpy_image_z(x_size, y_size, color_depth):
    red = np.ones((x_size, y_size), dtype=np.uint8) * 255
    green = np.zeros((x_size, y_size), dtype=np.uint8)
    blue = np.random.randint(0, 255, size=(x_size, y_size), dtype=np.uint8)
    return np.array([red, green, blue]).transpose(1, 2, 0)


def noise_image(task):
    color_depth = input_img.getNumChannels()
    x_size, y_size = input_img.getXSize(), input_img.getYSize()

    # FIXME: Why does this need to be copied? Is the array, as given, some kind
    # of non-transparently nested data structure?
    np_array = numpy_image_d(x_size, y_size, color_depth).copy()

    assert np_array.shape == (x_size, y_size, color_depth) and np_array.dtype == np.uint8
    input_tex.set_ram_image(PTAUchar(np_array))
    return task.cont


base.taskMgr.add(extract_image, "screen to numpy", sort=55)
base.taskMgr.add(noise_image, "numpy to screen", sort=56)

s.run()
