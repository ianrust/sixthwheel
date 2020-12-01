import pybullet as p
import time
import pybullet_data
import os

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase.InputStateGlobal import inputState

from math import copysign 
sign = lambda x : copysign(1, x) 


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.setBackgroundColor(0.0, 0.0, 0.0)
        self.disableMouse()

        self.camLens.setNearFar(1.0, 100.0)
        self.camLens.setFov(75.0)

        self.root = self.render.attachNewNode("Root")
        self.root.setPos(0.0, 0.0, 0.0)
        
        self.taskMgr.add(self.physicsTask, "physicsTask")
        self.taskMgr.add(self.egoUpdateTask, "egoUpdateTask")

        self.modelCube = loader.loadModel("cube.egg")

        self.cube = self.modelCube.copyTo(self.root)
        self.cube.setPos((0,0,0))

        physicsClient = p.connect(p.DIRECT)#or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
        p.setGravity(0,0,-10)
        planeId = p.loadURDF("plane.urdf")
        cubeStartPos = [0,0,1]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        p.setAdditionalSearchPath(os.path.dirname(os.path.abspath(__file__))) #optionally
        self.boxId = p.loadURDF("car.urdf",cubeStartPos, cubeStartOrientation)

        p.enableJointForceTorqueSensor(self.boxId, 0)
        p.enableJointForceTorqueSensor(self.boxId, 1)

        p.changeDynamics(self.boxId, -1, lateralFriction=0.1)
        p.changeDynamics(self.boxId, 0, lateralFriction=0.1)
        p.changeDynamics(self.boxId, 1, lateralFriction=0.1)

        self.control_force = 0
        self.semi_force = 1

        inputState.watchWithModifiers("throttle", "w")
        inputState.watchWithModifiers("brake", "s")
        inputState.watchWithModifiers("exit", "escape")
        inputState.watchWithModifiers("oobe", "o")

        self.prev_control_force = 0
        self.control_alpha = 0.9999

        self.integrator = 0


    def physicsTask(self, task):

        # pull force on the first joint
        js0 = p.getJointState(self.boxId, 0)
        # pull force on the second joint
        js1 = p.getJointState(self.boxId, 1)
        
        F_t = js0[2][1]
        F_l = js1[2][1]

        self.integrator += F_t * 0.1

        # Very hacked, no theoretical basis but it works!
        control_force_desired = (12 * F_t + F_l - self.integrator) / 0.001
        control_force_desired = control_force_desired
        self.control_force = self.control_alpha * self.prev_control_force + (1-self.control_alpha) * control_force_desired

        p.applyExternalForce(self.boxId, -1, (0, self.semi_force, 0), (0, 0, 0), p.WORLD_FRAME)
        p.applyExternalForce(self.boxId, 0, (0, self.control_force, 0), (0, 0, 0), p.WORLD_FRAME)

        print("6 tension", F_t,
                "trailer tension", F_l,
                "integrator", self.integrator,
             "control force", self.control_force,
             "control force desired", control_force_desired,
             "semi force", self.semi_force,
             "control force ratio", self.control_force / (self.control_force + self.semi_force) if self.semi_force!=0 else 0)
        
        p.stepSimulation()

        pos = p.getBasePositionAndOrientation(self.boxId)[0]
        vel = p.getBaseVelocity(self.boxId)[0]
        self.cube.setPos(pos)

        delta = 6 + 10 * abs(vel[1])
        cam_pos = (pos[0], pos[1] - delta, pos[2] + delta)

        self.camera.setPos(cam_pos)
        self.camera.lookAt(pos)

        self.prev_control_force = self.control_force

        return Task.cont

    def egoUpdateTask(self, task):

        self.semi_force = 0
        if inputState.isSet("throttle"):
            self.semi_force = 5.0
        if inputState.isSet("brake"):
            self.semi_force = -5.0
        if inputState.isSet("exit"):
            sys.exit()
        if inputState.isSet("oobe"):
            self.oobe()

        return Task.cont


app = MyApp()
app.run()

# p.disconnect()
