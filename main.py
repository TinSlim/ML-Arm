

##Bibliotecas
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

##Módulos

import Modulo.transformations as tr
import Modulo.basic_shapes as bs
import Modulo.scene_graph as sg
import Modulo.easy_shaders as es
import Modulo.readobj as rbj
import Modulo.lighting_shaders as ls

from controller import *
from arm import *
from ball import *

##Control para guardar variables

##Se instancia un control
brazo = Arm()
control = Controller()
ball = Ball(0,0,0)


##Para salir del programa, presionar Esc
#def on_key(window, key, scancode, action, mods):
#    if action != glfw.PRESS:
#        return
#    
#    elif key == glfw.KEY_ESCAPE:
#        sys.exit()



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    #Tamaño ventana
    width = 600
    height = 600

    window = glfw.create_window(width, height, "Bird", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, control.on_key)

    # Pipeline
    pipeline = ls.SimplePhongShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    
    t0 = 0
    camera_theta = 0
    
    brazo.create_parts()
    ball.create_parts()
    
    a = True
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        cursor_at = glfw.get_cursor_pos(window)

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        #Para rotar la cámara
        control.set_dt(dt * 6)

        #brazo.rotate_arm0(control.angle,control.rotation)
        #brazo.rotate_arm1(control.angle,control.rotation)
        #10.5 en y
        if a:
            a = False
            ball.move(0.5,0.2,6) #10.5 brazo radio

        brazo.actualizate_arms()
        largo_brazo0 = 6-0.5
        largo_brazo1 = 10.5-6
        brazo.arm0_angle = control.angle0
        brazo.arm1_rotation = control.rotation1
        arm_final = [np.sin(brazo.arm0_rotation) * np.cos(brazo.arm0_angle) * (largo_brazo0 + largo_brazo1*np.cos(brazo.arm1_rotation))
        ,np.sin(brazo.arm0_rotation) * np.sin(brazo.arm0_angle) * (largo_brazo0 + largo_brazo1*np.cos(brazo.arm1_rotation)),
        np.cos(brazo.arm0_rotation)  * (largo_brazo0 + largo_brazo1*np.cos(brazo.arm1_rotation))
        ]
        ball.translate(arm_final[1],-arm_final[0],arm_final[2]) #10.5 brazo radio
        print(arm_final)               
        #print(brazo.arm1_rotation)
        brazo.arm0_rotation = control.rotation0
        
        #Manejo de la cámara
        R = 20
        camX = R * np.sin(control.camera_angle+3)
        camY = R * np.cos(control.camera_angle+3)
        viewPos = np.array([camX, camY,10])
        view = tr.lookAt(
            viewPos,
            np.array([0,0,5]), # a dnd mira
            np.array([0,0,1])
        )

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        
        

        # Drawing shapes
        glUseProgram(pipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), -3, 0, 3)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(3))


        #Se usa el pipeline de sombras y luz para el dibujo del pájaro
        sg.drawSceneGraphNode(brazo.big_node, pipeline, "model")
        sg.drawSceneGraphNode(ball.big_node, pipeline, "model")

        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.matmul([
                tr.uniformScale(3),
                tr.rotationX(np.pi/2),
                tr.translate(1.5,-0.25,0)])
        )
    

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
