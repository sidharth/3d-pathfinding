from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import GraphicsWindow
from panda3d.core import Filename
from pandac.PandaModules import *


from math import pi, sin, cos
import numpy as np
from scipy import misc as misc
import matplotlib.pyplot as plt
import png
# import PIL
# import Image

class Sim(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.useDrive()
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8, 42, 0)
        self.pandaActor = Actor("models/panda-model", {"walk":"models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")

        pandaPosInterval1 = self.pandaActor.posInterval(13, Point3(0, -10, 0), startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13, Point3(0, 10, 0), startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")

        myWindow = base.win
        # base.win.saveScreenShot()
        activeDisplay = myWindow.getActiveDisplayRegions()
        texture = activeDisplay[0].getScreenshot()

        self.extract_image(texture)
        # myWindow.saveScreenShot(Filename('hello.png'),"yo")

        # print type(myWindow)
        self.pandaPace.loop()
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi/180.0)
        # self.camera.node().setLens(PerspectiveLens())
        # t = self.camera.getCameraMask()
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        p = PNMImage()
        base.win.getScreenshot(p)
        # p.write(Filename("a.jpg"))

        return Task.cont

    def extract_image(self, texture):
        # pointer = output_tex.get_ram_image()
        # img_array = np.fromstring(pointer.get_data())
        # FIXME: The lines above do work. The ones below do not.
        pointer = texture.getRamImage()
        buf = pointer.getData()
        print type(buf)
        # print pointer
        # print texture
        img_array = np.frombuffer(buf, np.uint32)
        img_array_2 = img_array.reshape((800,1200))
        print type(img_array)
        print img_array.shape
        print img_array_2.shape
        plt.imshow(img_array_2, cmap=plt.cm.gray, vmin=30, vmax=200)
        # misc.imsave('f.png', img_array)
        # rescaled = np.uint8(img_array)
        # print rescaled
        # print len(rescaled)
        # png.from_array(img_array).save("smiley.png")
        return Task.cont

app = Sim()
app.run()
