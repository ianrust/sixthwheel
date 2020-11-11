import pybullet as p
import time
import pybullet_data
import os



physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
print(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
p.setAdditionalSearchPath(os.path.dirname(os.path.abspath(__file__))) #optionally
print(os.path.dirname(os.path.abspath(__file__)))
boxId = p.loadURDF("car.urdf",cubeStartPos, cubeStartOrientation)

p.enableJointForceTorqueSensor(boxId, 0)
p.enableJointForceTorqueSensor(boxId, 1)

p.changeDynamics(boxId, -1, lateralFriction=0)
p.changeDynamics(boxId, 0, lateralFriction=0)
p.changeDynamics(boxId, 1, lateralFriction=0)

control_force = 0
semi_force = 1.0

for i in range (10000):
    p.applyExternalForce(boxId, -1, (0, semi_force, 0), (0, 0, 0), p.WORLD_FRAME)
    p.applyExternalForce(boxId, 0, (0, control_force, 0), (0, 0, 0), p.WORLD_FRAME)

    # pull force on the first joint
    js0 = p.getJointState(boxId, 0)
    # pull force on the second joint
    js1 = p.getJointState(boxId, 1)
    print("tension", js0[2][1], "control force ratio", control_force / (control_force + semi_force))
    
    p.stepSimulation()
    time.sleep(1./240.)

    control_force = 2.5*js0[2][1]
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
p.disconnect()
