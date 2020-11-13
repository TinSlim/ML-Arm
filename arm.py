import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

import numpy as np
class Arm:

    def __init__(self):
        self.arm0_angle = 0
        self.arm0_rotation = 0
        self.arm1_rotation = 0
        self.arm0_large = 6.5-0.5
        self.arm1_large = 10.5-6
        self.point = [
            (np.sin(self.arm0_rotation) * np.sin(self.arm0_angle) * self.arm0_large) + (self.arm1_large * np.sin(self.arm0_angle) * np.sin(self.arm1_rotation + self.arm0_rotation)),# * np.sin(brazo.arm1_rotation + brazo.arm0_rotation))
            -1* ( (np.sin(self.arm0_rotation) * np.cos(self.arm0_angle) * self.arm0_large) + (self.arm1_large * np.cos(self.arm0_angle) * np.sin(self.arm1_rotation + self.arm0_rotation)) ),# * -np.sin(brazo.arm1_rotation + brazo.arm0_rotation))
            (np.cos(self.arm0_rotation)  * self.arm0_large )+ (self.arm1_large* np.cos(self.arm1_rotation + self.arm0_rotation))
        ]

    def create_parts(self):
        gpu_base = es.toGPUShape(bs.createColorNormalsCube(1, 0, 0))
        gpu_arm0 = es.toGPUShape(bs.createColorNormalsCube(0, 1, 0))
        gpu_arm1 = es.toGPUShape(bs.createColorNormalsCube(0, 0, 1))
        
        node_arm1 = sg.SceneGraphNode("arm1")
        node_arm1.transform = tr.scale(0.5,0.5,5)#tr.matmul([tr.scale(1,1,3),tr.translate(0,0,0)]) 
        node_arm1.childs += [gpu_arm1]
        
        node_arm0 = sg.SceneGraphNode("arm0")
        node_arm0.transform = tr.matmul([tr.scale(0.5,0.5,6),tr.translate(0,0,0)]) 
        node_arm0.childs += [gpu_arm0]

        node_arms1 = sg.SceneGraphNode("arms1")
        #node_arms1.transform = tr.translate(0,0,4)
        node_arms1.childs += [node_arm1]

        node_arms0 = sg.SceneGraphNode("arms0")
        node_arms0.transform = tr.matmul([tr.rotationX(0),tr.translate(0,0,2)])
        node_arms0.childs += [node_arm0,node_arms1]

        node_base = sg.SceneGraphNode("base")
        node_base.transform = tr.scale(3,3,1) 
        node_base.childs += [gpu_base]
        
        node_all = sg.SceneGraphNode("all")
        node_all.childs += [node_arms0, node_base]
        
        self.big_node = node_all
    
    def rotate_arm0(self,value,value2):
        arm0 = sg.findNode(self.big_node, "arms0")
        arm0.transform = tr.matmul([tr.translate(0,0,0.5),tr.rotationZ(self.arm0_angle),tr.rotationX(self.arm0_rotation),tr.translate(0,0,3)])

    def rotate_arm1(self,value,value2):
        arm1 = sg.findNode(self.big_node, "arms1")
        #arm1.transform = tr.matmul([tr.identity(),tr.identity()])
        arm1.transform = tr.matmul([tr.translate(0,0,2.5),tr.rotationZ(value),tr.rotationX(value2),tr.translate(0,0,2)])

    def actualize_arms(self):
        arm0 = sg.findNode(self.big_node, "arms0")
        arm0.transform = tr.matmul([tr.translate(0,0,0.5),tr.rotationZ(self.arm0_angle),tr.rotationX(self.arm0_rotation),tr.translate(0,0,3)])
        arm1 = sg.findNode(self.big_node, "arms1")
        #arm1.transform = tr.matmul([tr.identity(),tr.identity()])
        arm1.transform = tr.matmul([tr.translate(0,0,2.5),tr.rotationX(self.arm1_rotation),tr.translate(0,0,2)])

    def actualize_point(self):
        self.point = [
            (np.sin(self.arm0_rotation) * np.sin(self.arm0_angle) * self.arm0_large) + (self.arm1_large * np.sin(self.arm0_angle) * np.sin(self.arm1_rotation + self.arm0_rotation)),
            -1 * ( (np.sin(self.arm0_rotation) * np.cos(self.arm0_angle) * self.arm0_large) + (self.arm1_large * np.cos(self.arm0_angle) * np.sin(self.arm1_rotation + self.arm0_rotation)) ),# * -np.sin(brazo.arm1_rotation + brazo.arm0_rotation))
            # * np.sin(brazo.arm1_rotation + brazo.arm0_rotation))
            (np.cos(self.arm0_rotation)  * self.arm0_large )+ (self.arm1_large* np.cos(self.arm1_rotation + self.arm0_rotation))
        ]






