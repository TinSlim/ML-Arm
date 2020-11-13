import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

class Ball:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def setX(self,new_x):
        self.x = new_x
    
    def setY(self,new_y):
        self.y = new_y

    def setZ(self,new_z):
        self.z = new_z
    
    def create_parts(self):
        gpu_cube = es.toGPUShape(bs.createColorNormalsCube(1, 1, 0))
        
        node_cube = sg.SceneGraphNode("cube")
        node_cube.transform =([tr.translate(1,1,0),tr.scale(0.5,0.5,0.5)]) 
        node_cube.childs += [gpu_cube]
        
        
        node_all = sg.SceneGraphNode("all")
        node_all.childs += [node_cube]
        
        self.big_node = node_all
    
    def move(self,x,y,z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        cube = sg.findNode(self.big_node, "cube")
        cube.transform =([tr.translate(self.x,self.y,self.z),tr.scale(0.5,0.5,0.5)]) 
    
    def translate(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        cube = sg.findNode(self.big_node, "cube")
        cube.transform =([tr.translate(self.x,self.y,self.z),tr.scale(0.5,0.5,0.5)]) 