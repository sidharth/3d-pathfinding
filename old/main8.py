from direct.directbase import DirectStart
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom
from panda3d.core import BitMask32, CardMaker, Vec4, Quat
from random import randint, random

world = OdeWorld()
world.setGravity(0, 0, -9.81)
# The surface table is needed for autoCollide
world.initSurfaceTable(1)
world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

# Create a space and add a contactgroup to it to add the contact joints
space = OdeSimpleSpace()
space.setAutoCollideWorld(world)
contactgroup = OdeJointGroup()
space.setAutoCollideJointGroup(contactgroup)

scene = loader.loadModel("Ground2/Ground2")
scene.reparentTo(render)
scene.setPos(0, 0, -1)

agent = loader.loadModel("raft/raft")
agent.setPos(10,10,10)
agent.reparentTo(render)

# Set the camera position
base.disableMouse()
base.camera.setPos(40, 40, 20)
base.camera.lookAt(0, 0, 0)

def simulationTask(task):
  space.autoCollide() # Setup the contact joints
  # Step the simulation and set the new positions
  world.quickStep(globalClock.getDt())
  # for np, body in boxes:
  #   np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
  contactgroup.empty() # Clear the contact joints
  return task.cont

taskMgr.doMethodLater(0.5, simulationTask, "Physics Simulation")
run()
