from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *

from panda3d.core import Filename
from panda3d.core import BitMask32, CardMaker, Vec4, Quat
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom
from random import randint, random

counter = 0
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.putGravity()
        # world = OdeWorld()
        # world.setGravity(0, 0, -9.81)
        self.loadModels()
        # self.useDrive()

        base.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()

        cnode = CollisionNode('actor_node_path')
        cnode.addSolid(CollisionSphere(0, 0, 0, 10))
        agentc = self.agent.attachNewNode(cnode)
        agentc.show()

        cnode2 = CollisionNode('plane')
        cnode2.addSolid(CollisionSphere(0, 1600, 10, 5))
        scenec = self.scene.attachNewNode(cnode2)
        scenec.show()

        base.cTrav.addCollider(scenec, pusher)
        pusher.addCollider(scenec, self.scene, base.drive.node())

        # self.taskMgr.add(self.exampleTask, "ExampleTask")

    def exampleTask(self, task):
        p = PNMImage()
        base.win.getScreenshot(p)
        p.write(Filename("test2"))
        return Task.cont

    def loadModels(self):
        self.scene = loader.loadModel("Ground2/Ground2")
        self.scene.reparentTo(render)
        self.scene.setPos(0, 0, -1)

        self.agent = loader.loadModel("raft/raft")
        self.agent.reparentTo(self.actor_node_path)
        self.agent.setPos(0,1600,380)



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

app = MyApp()
app.run()
