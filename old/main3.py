from direct.showbase.ShowBase import ShowBase
from panda3d.core import PNMImage, Texture
from panda3d.core import GraphicsOutput as go
from panda3d.core import PTAUchar
from panda3d.core import CardMaker

import numpy as np
import png

s = ShowBase()
# base.set_frame_rate_meter(True)

output_img = PNMImage(base.win.get_x_size(), base.win.get_y_size())
output_tex = Texture()
output_tex.load(output_img)
base.win.add_render_texture(output_tex, go.RTM_copy_ram, go.RTP_color)

def extract_image(task):
    # pointer = output_tex.get_ram_image()
    # img_array = np.fromstring(pointer.get_data())
    # FIXME: The lines above do work. The ones below do not.
    pointer = output_tex.getRamImage()
    img_array = np.frombuffer(pointer, np.uint32)
    png.from_array(img_array).save("smiley.png")
    return task.cont
