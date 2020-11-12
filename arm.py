import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

class Arm:

    def __init__(self):
        self.arm0_x = 0
        self.arm0_y = 0
        self.arm0_z = 0

    def create_parts(self):
        gpu_base = es.toGPUShape(bs.createColorNormalsCube(1, 0, 0))
        gpu_arm0 = es.toGPUShape(bs.createColorNormalsCube(0, 1, 0))
        gpu_arm1 = es.toGPUShape(bs.createColorNormalsCube(0, 0, 1))
        
        node_arm1 = sg.SceneGraphNode("arm1")
        node_arm1.transform = tr.scale(1,1,3)#tr.matmul([tr.scale(1,1,3),tr.translate(0,0,0)]) 
        node_arm1.childs += [gpu_arm1]
        
        node_arm0 = sg.SceneGraphNode("arm0")
        node_arm0.transform = tr.scale(1,1,3)#tr.matmul([tr.scale(1,1,3),tr.identity()]) 
        node_arm0.childs += [gpu_arm0]

        node_arms1 = sg.SceneGraphNode("arms1")
        node_arms1.transform = tr.translate(0,0,3)
        node_arms1.childs += [node_arm1]

        node_arms0 = sg.SceneGraphNode("arms0")
        node_arms0.transform = tr.matmul([tr.rotationX(self.arm0_x),tr.translate(0,0,2)])
        node_arms0.childs += [node_arm0,node_arms1]

        node_base = sg.SceneGraphNode("base")
        node_base.transform = tr.scale(3,3,1) 
        node_base.childs += [gpu_base]
        
        node_all = sg.SceneGraphNode("all")
        node_all.childs += [node_arms0, node_base]
        
        self.big_node = node_all
    
    def rotate_arm0(self,value,value2):
        arm0 = sg.findNode(self.big_node, "arms0")
        arm0.transform = tr.matmul([tr.rotationZ(value),tr.rotationX(value2),tr.translate(0,0,2)])







