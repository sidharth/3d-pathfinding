# Way too many imports tho
import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import ZUp

from pandac.PandaModules import loadPrcFileData

from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import GraphicsWindow
from panda3d.core import Filename
from pandac.PandaModules import *
import numpy as np
import matplotlib.pyplot as plt
import Stereo_conv_net_Mac

pred_fn = Stereo_conv_net_Mac.get_pred_fn() 

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        loadPrcFileData('', 'bullet-enable-contact-events true')
        loadPrcFileData("", "win-size 300 100")
        winProp = WindowProperties()
        winProp.setSize(300,100)
        base.win.requestProperties(winProp)
        world = BulletWorld()
        self.world = world

        # Cameras
        base.camNode.setActive(0)
        self.cam1 = base.makeCamera(base.win, displayRegion=(0,.5,0,1))
        self.cam2 = base.makeCamera(base.win, displayRegion=(.5,1,0,1))
        self.cam1.setPos(-10,-50,1)
        self.cam2.setPos(10,-50,1)

        # Plane ground
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)
        scene = loader.loadModel('Ground2/Ground2')
        scene.reparentTo(render)

        # Repeat every new game
        self.newGame()
        self.skip = True
        plt.ion()        
        # Repeat tasks every frame
        taskMgr.add(self.update, 'update')

    def newGame(self):

        # Instantiates dabba in the world.
        # Makes it rigid too.
        boxmodel = loader.loadModel("models/box.egg")
        boxmodel.setPos(-0.5, -0.5, -0.5)
        boxmodel.flattenLight()
        shape3 = BulletBoxShape(Vec3(0.5,0.5,0.5))
        playerNode = BulletRigidBodyNode('Player')
        playerNode.addShape(shape3)
        playerNode.setMass(1.0)
        playerNP = render.attachNewNode(playerNode)
        playerNP.setPos(0, 0, 10)
        playerNP.node().notifyCollisions(True)
        self.playerNP = playerNP
        self.world.attachRigidBody(playerNP.node())
        self.playerNode = playerNode
        boxmodel.copyTo(playerNP)


        # Connects cam to dabba
        self.cam1.reparentTo(playerNP)
        self.cam2.reparentTo(playerNP)
        self.cam1.setPos(-0.15,10,0)
        self.cam2.setPos( 0.15,10,0)

        base.accept('u',self.up)
        base.accept('j',self.down)
        base.accept('w',self.forward)
        base.accept('s',self.back)
        base.accept('a',self.rotLeft)
        base.accept('d',self.rotRight)
        base.accept('t',self.rotUp)
        base.accept('g',self.rotDown)
        base.acceptOnce('bullet-contact-added', self.onContactAdded)

    def destroyPlayer(self):
        self.playerNP.setPos(0,0,100)
        
        base.cam.reparentTo(render)
        self.cam1.reparentTo(render)
        self.cam2.reparentTo(render)
        self.world.removeRigidBody(self.playerNP.node())
        render.node().removeChild(self.playerNP.node())
        base.ignoreAll()
        self.newGame()

    def update(self,task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        if self.skip:
            self.skip = False
            return task.cont

        # screenshot
        tex = base.win.getScreenshot()
        l,r = self.get_camera_image()
        
        if(l.shape[0] != 100):
            return task.cont
        l = l.reshape(1,1,100,150)
        r = r.reshape(1,1,100,150)
        inp = np.concatenate((l,r),axis=1)
        op  = pred_fn(inp)[0]
        # print op[0].shape
        # dim = self.get_camera_depth_image()
        plt.clf()
        plt.imshow(op[0,0,...],cmap = plt.get_cmap('gray'))
        plt.draw()

        # x = raw_input()
        return task.cont

    def up(self):
        self.playerNP.setZ(self.playerNP.getZ()+1)

    def down(self):
        self.playerNP.setZ(self.playerNP.getZ()-1)

    def forward(self):
        self.playerNP.setY(self.playerNP.getY()+1)

    def back(self):
        self.playerNP.setY(self.playerNP.getY()-1)

    def rotLeft(self):
        self.playerNode.applyTorqueImpulse(Vec3(0,0,0.05))

    def rotRight(self):
        self.playerNode.applyTorqueImpulse(Vec3(0,0,-0.05))

    def rotUp(self):
        self.playerNode.applyTorqueImpulse(Vec3(0.05,0,0))

    def rotDown(self):
        self.playerNode.applyTorqueImpulse(Vec3(-0.05,0,0))


    def onContactAdded(self,node1,node2):
        print 'touch'
        self.destroyPlayer()

    def get_camera_image(self, requested_format=None):
        """
        Returns the camera's image, which is of type uint8 and has values
        between 0 and 255.
        The 'requested_format' argument should specify in which order the
        components of the image must be. For example, valid format strings are
        "RGBA" and "BGRA". By default, Panda's internal format "BGRA" is used,
        in which case no data is copied over.
        """
        tex = base.win.getScreenshot()
        if requested_format is None:
            data = tex.getRamImage()
        else:
            data = tex.getRamImageAs(requested_format)
        image = np.frombuffer(data.get_data(), np.uint8)  # use data.get_data() instead of data in python 2
        image.shape = (tex.getYSize(), tex.getXSize(), tex.getNumComponents())
        image = np.flipud(image)
        image = self.rgb2gray(image)
        # print "lol",image.shape
        return np.hsplit(image,2)

    def rgb2gray(self,rgb):
        return np.dot(rgb[...,:3], [  0.114,0.587,0.299])

    def get_camera_depth_image(self):
        """
        Returns the camera's depth image, which is of type float32 and has
        values between 0.0 and 1.0.
        """
        data = self.depthTex.getRamImage()
        depth_image = np.frombuffer(data, np.float32)
        depth_image.shape = (self.depthTex.getYSize(), self.depthTex.getXSize(), self.depthTex.getNumComponents())
        depth_image = np.flipud(depth_image)
        return depth_image

  


app = Game()
app.run()
