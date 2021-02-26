
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

import modulo.easy_shaders as es
import modulo.lighting_shaders as ls

from controller import *
from arm import *
from ball import *
from classifier import *



new_ball_value = False

ball = Ball(10,10,10)
ball.random_pos()
brazo = Arm(ball)

classifier_new = Classifier("data.csv")
classifier_new.get_data()
classifier_new.fit()

control = Controller(brazo,classifier_new)



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Catched", None, None)

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


        #10.5 en y
        if a:
            a = False
            ball.move(1,1,6) #10.5 arm radio

        brazo.actualize_arms()

        
        brazo.actualize_point()
        if ball.catched:
            ball.translate(brazo.point[0],brazo.point[1],brazo.point[2]) #10.5 arm radio
        else:
            brazo.distance_ball_point()

        if new_ball_value:
            print("nice")
            new_ball_value = False

        # Camera
        R = 20
        camX = R * np.sin(control.camera_angle+3)
        camY = R * np.cos(control.camera_angle+3)
        viewPos = np.array([camX, camY,10])
        view = tr.lookAt(
            viewPos,
            np.array([0,0,5]), # look to
            np.array([0,0,1])
        )

        # Projection
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

        # Clearing screen
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


        # Draws arm and ball
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
