import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

class World(DirectObject):
   def __init__(self):
      base.setBackgroundColor(1, 1, 1)
      base.disableMouse()
      self.environmentModel = loader.loadModel("models/environment")
      self.environmentModel.reparentTo(render)
      self.environmentModel.setPos(0, 20, -10)

      self.cameraModel = loader.loadModel("models/camera")
      self.cameraModel.reparentTo(render)
      self.cameraModel.setPos(0, 15, 0)

      base.camera.reparentTo(self.cameraModel)
      base.camera.setY(base.camera, 5)

      self.keyMap = {"w" : False, "s" : False, "a" : False, "d" : False,}

      self.accept("w", self.setKey, ["w", True])
      self.accept("s", self.setKey, ["s", True])
      self.accept("a", self.setKey, ["a", True])
      self.accept("d", self.setKey, ["d", True])

      self.accept("w-up", self.setKey, ["w", False])
      self.accept("s-up", self.setKey, ["s", False])
      self.accept("a-up", self.setKey, ["a", False])
      self.accept("d-up", self.setKey, ["d", False])

      taskMgr.add(self.cameraControl, "Camera Control")

   def setKey(self, key, value):
      self.keyMap[key] = value

   def cameraControl(self, task):
      dt = globalClock.getDt()
      if(dt > .20):
         return task.cont

      if(base.mouseWatcherNode.hasMouse() == True):
         mpos = base.mouseWatcherNode.getMouse()
         base.camera.setP(mpos.getY() * 30)
         base.camera.setH(mpos.getX() * -50)
         if (mpos.getX() < 0.1 and mpos.getX() > -0.1 ):
            self.cameraModel.setH(self.cameraModel.getH())
         else:
            self.cameraModel.setH(self.cameraModel.getH() + mpos.getX() * -1)

      if(self.keyMap["w"] == True):
         self.cameraModel.setY(self.cameraModel, 15 * dt)
         print("camera moving forward")
         return task.cont
      elif(self.keyMap["s"] == True):
         self.cameraModel.setY(self.cameraModel, -15 * dt)
         print("camera moving backwards")
         return task.cont
      elif(self.keyMap["a"] == True):
         self.cameraModel.setX(self.cameraModel, -10 * dt)
         print("camera moving left")
         return task.cont
      elif(self.keyMap["d"] == True):
         self.cameraModel.setX(self.cameraModel, 10 * dt)
         print("camera moving right")
         return task.cont
      else:
         return task.cont
w = World()
run()
