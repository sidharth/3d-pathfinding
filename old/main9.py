from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *

from panda3d.core import Filename
from panda3d.core import BitMask32, CardMaker, Vec4, Quat
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom
from random import randint, random
from panda3d.physics import AngularEulerIntegrator


counter = 0
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModels()
        self.putGravity()
        # self.initWorld()
        # self.initGround()




        base.camera.reparentTo(self.agent)
        base.camera.setPos(0,0,4.5)
        base.camera.setP(10)
        # Set the camera position
        base.disableMouse()
        # base.camera.setPos(40, 40, 20)
        # base.camera.lookAt(0, 0, 0)

        self.accept('a', self.fun)
        self.accept('r', self.rFun)
        self.accept('u',self.up)
        # self.accept('u-up',self.uFun2)


    def rFun(self):
        moveForwardFN=ForceNode('world1-forces')
        moveForwardFNP=render.attachNewNode(moveForwardFN)
        angularForce = AngularVectorForce(.2,0,0)
        moveForwardFN.addForce(angularForce)
        base.physicsMgr.addAngularForce(angularForce)
        self.actor_node.getPhysical(0).addAngularForce(angularForce)

    def uFun(self):
        moveForwardFN=ForceNode('world-forces')
        moveForwardFNP=render.attachNewNode(moveForwardFN)
        moveForwardForce=LinearVectorForce(0,0,15) #gravity acceleration
        moveForwardFN.addForce(moveForwardForce)
        base.physicsMgr.addLinearForce(moveForwardForce)
        # moveForwardForce = LinearVectorForce(0,1,0)
        self.actor_node.getPhysical(0).addLinearForce(moveForwardForce)

    def uFun2(self):
        moveForwardFN=ForceNode('world-forces')
        moveForwardFNP=render.attachNewNode(moveForwardFN)
        moveForwardForce=LinearVectorForce(0,0,-15) #gravity acceleration
        moveForwardFN.addForce(moveForwardForce)
        base.physicsMgr.addLinearForce(moveForwardForce)
        # moveForwardForce = LinearVectorForce(0,1,0)
        self.actor_node.getPhysical(0).addLinearForce(moveForwardForce)
        self.actor_node.getPhysical(0).addLinearForce(moveForwardForce)


    def fun(self):

        moveForwardFN=ForceNode('world-forces')
        moveForwardFNP=render.attachNewNode(moveForwardFN)
        moveForwardForce=LinearVectorForce(0,1,0) #gravity acceleration
        moveForwardFN.addForce(moveForwardForce)
        base.physicsMgr.addLinearForce(moveForwardForce)
        # moveForwardForce = LinearVectorForce(0,1,0)
        self.actor_node.getPhysical(0).addLinearForce(moveForwardForce)


    def loadModels(self):
        base.enableParticles()

        self.scene = loader.loadModel("Ground2/Ground2")
        self.scene.reparentTo(render)
        self.scene.setPos(0, 0, -1)


        physics_node = NodePath("PhysicsNode")
        physics_node.reparentTo(render)
        self.actor_node = ActorNode("Raft")
        self.actor_node.getPhysicsObject().setMass(100)
        self.actor_node_path = physics_node.attachNewNode(self.actor_node)
        base.physicsMgr.attachPhysicalNode(self.actor_node)

        self.agent = loader.loadModel("raft/raft")
        self.agent.reparentTo(self.actor_node_path)
        self.agent.setPos(0,0,1)
        angleInt = AngularEulerIntegrator() # Instantiate an AngleIntegrator()
        base.physicsMgr.attachAngularIntegrator(angleInt) # Attatch the AngleIntegrator to the PhysicsManager

    def putGravity(self):
        base.enableParticles()

        physics_node = NodePath("PhysicsNode")
        physics_node.reparentTo(render)
        actor_node = ActorNode("jetpack-guy-physics")
        actor_node.getPhysicsObject().setMass(100)
        self.actor_node_path = physics_node.attachNewNode(actor_node)
        base.physicsMgr.attachPhysicalNode(actor_node)

        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-19.81) #gravity acceleration
        gravityFN.addForce(gravityForce)
        base.physicsMgr.addLinearForce(gravityForce)


    # 3D Movement functions
    # def forward(self):
    #
    # def backward(self):

    def up(self):
        moveForwardFN=ForceNode('world-forces-yo')
        moveForwardFNP=render.attachNewNode(moveForwardFN)
        moveForwardForce=LinearVectorForce(0,0,15) #gravity acceleration
        moveForwardFN.addForce(moveForwardForce)
        # base.physicsMgr.addLinearForce(moveForwardForce)
        # moveForwardForce = LinearVectorForce(0,1,0)
        self.actor_node.getPhysical(0).addLinearForce(moveForwardForce)

    # def down(self):
    #
    # def rotLeft(self):
    #
    # def rotRight(self):
    #
    # def rotUp(self):
    #
    # def rotDown(self):



app = MyApp()
app.run()
