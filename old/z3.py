import direct.directbase.DirectStart
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

loadPrcFileData('', 'bullet-enable-contact-events true')
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))

height = 1.75
radius = 0.4

# player
shape3 = BulletBoxShape(Vec3(0.5,0.5,0.5))
playerNode = BulletRigidBodyNode('Player')
playerNode.addShape(shape3)
playerNode.setMass(1.0)
playerNP = render.attachNewNode(playerNode)
playerNP.setPos(0, 0, 14)
playerNP.node().notifyCollisions(True)
# playerNP.setH(45)
# playerNP.setCollideMask(BitMask32.allOn())
world.attachRigidBody(playerNP.node())

# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, 0)
world.attachRigidBody(node)

scene = loader.loadModel('Ground2/Ground2')
scene.reparentTo(render)

base.cam.setPos(0,0,1)
base.cam.reparentTo(playerNP)

# Update
def update(task):
    dt = globalClock.getDt()
    world.doPhysics(dt)
    return task.cont

def up():
    playerNode.applyCentralImpulse(Vec3(0,0,10))
    print "YO"

def onContactAdded(node1,node2):
    print 'x'
    exit()
base.accept('a',up)
base.accept('bullet-contact-added', onContactAdded)
taskMgr.add(update, 'update')
run()
