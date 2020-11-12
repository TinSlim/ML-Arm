
class Arm:

    def __init__(self):
        self.rotation = 0
        self.angle_1 = 0
        self.angle_2 = 0
    
    def rotation(self,add_rotation,add_angle_1,add_angle_2):
        




def pajaro():
    gpuCabeza = es.toGPUShape(rbj.readOBJ("Model/cabeza.obj", (0,1,0.8)))
    gpuTorso = es.toGPUShape(rbj.readOBJ("Model/torso.obj", (0,0.8,1)))
    gpuAlaSupDer = es.toGPUShape(rbj.readOBJ("Model/alasupder.obj", (0,1,1)))
    gpuAlaInfDer = es.toGPUShape(rbj.readOBJ("Model/alainfder.obj", (0,0.7,1)))
    gpuAlaSupIzq = es.toGPUShape(rbj.readOBJ("Model/alasupizq.obj", (0,1,1)))
    gpuAlaInfIzq = es.toGPUShape(rbj.readOBJ("Model/alainfizq.obj", (0,0.7,1)))

    #################Ala Derecha
    #Ala inf derecha
    AlaInfDerecha = sg.SceneGraphNode("AlaInfDerecha")
    AlaInfDerecha.transform = tr.translate(0,0,0)  #Ajustar bn
    AlaInfDerecha.childs+=[gpuAlaInfDer]

    #Rotación ala inf derecha
    RotacionAlaInfDerecha = sg.SceneGraphNode("RotacionAlaInfDerecha")
    RotacionAlaInfDerecha.transform = tr.matmul([tr.translate(-1.5,-2,-2),tr.rotationY(np.pi/3),tr.translate(1,2,2)])
    RotacionAlaInfDerecha.childs+= [AlaInfDerecha]

    #Ala sup derecha
    AlaSupDerecha = sg.SceneGraphNode("AlaSupDerecha")
    AlaSupDerecha.childs+=[gpuAlaSupDer]
   
    #Ala derecha
    AlaDerecha = sg.SceneGraphNode("AlaDerecha")
    AlaDerecha.childs+=[AlaSupDerecha]
    AlaDerecha.childs+=[RotacionAlaInfDerecha]
    AlaDerecha.transform = tr.matmul([tr.translate(-1,-2.5,0),tr.rotationY(np.pi),tr.rotationX(np.pi),tr.translate(1,2.5,0)])  #AlaDerecha.transform = tr.matmul([tr.translate(0,-2,0),tr.rotationX(np.pi*(2/3)),tr.translate(0,2,0.5)])#

    ################# Ala Izquierda
    #Ala inf izquierda
    AlaInfIzquierda = sg.SceneGraphNode("AlaInfIzquierda")
    AlaInfIzquierda.transform = tr.translate(0,0,0)  #Ajustar bn
    AlaInfIzquierda.childs+=[gpuAlaInfIzq]

    #Rotación ala inf izquierda
    RotacionAlaInfIzquierda = sg.SceneGraphNode("RotacionAlaInfIzquierda") 
    RotacionAlaInfIzquierda.transform = tr.matmul([tr.translate(1.5,-2,-2),tr.rotationY(-np.pi/3),tr.translate(-1,2,2)])
    RotacionAlaInfIzquierda.childs+= [AlaInfIzquierda]

    #Ala sup izquierda
    AlaSupIzquierda = sg.SceneGraphNode("AlaSupIzquierda")
    AlaSupIzquierda.childs+=[gpuAlaSupIzq]

    #Ala izquierda
    AlaIzquierda = sg.SceneGraphNode("AlaIzquierda")
    AlaIzquierda.childs+=[AlaSupIzquierda]
    AlaIzquierda.childs+=[RotacionAlaInfIzquierda]
    
    ################# Ambas Alas
    #Alas
    Alas = sg.SceneGraphNode("Alas")
    Alas.childs+=[AlaDerecha]
    Alas.childs+=[AlaIzquierda]

    ################# Cuerpo
    #Torso
    Torso = sg.SceneGraphNode("Torso")
    Torso.childs+= [gpuTorso]
    #Torso.transform=tr.matmul([tr.rotationX(np.pi/2),tr.uniformScale(1)])
    #Torso.transform=tr.matmul([tr.rotationZ(90),tr.translate(0,0,0)])

    #Cabeza
    Cabeza = sg.SceneGraphNode("Cabeza")
    Cabeza.childs+= [gpuCabeza]
    #Cabeza.transform=tr.rotationX(np.pi/2)

    #Cuerpo
    Cuerpo = sg.SceneGraphNode("Cuerpo")
    Cuerpo.childs+= [Torso]
    Cuerpo.childs+= [Cabeza]

    ################# Pájaro
    #Pajaro Total1
    Pajaro1 = sg.SceneGraphNode("Pajaro1")
    Pajaro1.childs+=[Alas]
    Pajaro1.childs+=[Cuerpo]
    Pajaro1.transform=tr.matmul([tr.uniformScale(0.1),tr.rotationX(np.pi*(1/2))])

    #Pajaro
    Pajaro = sg.SceneGraphNode("Pajaro")
    Pajaro.childs+=[Pajaro1]
    return Pajaro



