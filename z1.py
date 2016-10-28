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


from math import pi, sin, cos
import numpy as np
from scipy import misc as misc
import matplotlib.pyplot as plt
import png

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        loadPrcFileData('', 'bullet-enable-contact-events true')
        world = BulletWorld()
        self.world = world
        world.setGravity(Vec3(0, 0, -9.81))
        base.cam.setPos(0,-50,1)

        # Plane
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 0, 0)
        self.world.attachRigidBody(node)
        scene = loader.loadModel('Ground2/Ground2')
        scene.reparentTo(render)
        self.newGame()

        taskMgr.add(self.update, 'update')

    def newGame(self):
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
        base.cam.reparentTo(playerNP)
        base.cam.setPos(0,-10,0)
        base.accept('u',self.up)
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
        print "Tryint to destroy"
        self.world.removeRigidBody(self.playerNP.node())
        render.node().removeChild(self.playerNP.node())
        print "Reparent camera"
        print "Destroyed"
        base.ignoreAll()
        self.newGame()

    def update(self,task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        return task.cont

    def up(self):
        self.playerNode.applyCentralImpulse(Vec3(0,0,10))
        print "YO"

    def forward(self):
        self.playerNode.applyCentralImpulse(Vec3(0,5,0))

    def back(self):
        self.playerNode.applyCentralImpulse(Vec3(0,-5,0))

    def rotLeft(self):
        self.playerNode.applyTorqueImpulse(Vec3(0,0,0.05))

    def rotRight(self):
        self.playerNode.applyTorqueImpulse(Vec3(0,0,-0.05))

    def rotUp(self):
        self.playerNode.applyTorqueImpulse(Vec3(0.05,0,0))

    def rotDown(self):
        self.playerNode.applyTorqueImpulse(Vec3(-0.05,0,0))


    def onContactAdded(self,node1,node2):
        self.destroyPlayer()


app = Game()
app.run()
