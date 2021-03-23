import glfw
from OpenGL.GL import *
import numpy as np

input_key = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    
    ###########################
    for i in input_key:
        if i == 'q':
            glTranslatef(-0.1, 0., 0.)
        elif i == 'e':
            glTranslatef(0.1, 0., 0.)
        elif i == 'a':
             
            glRotatef(10,0,0,1)
        elif i == 'd':
            glRotatef(-10,0,0,1)
        elif i == '1':
            glLoadIdentity()
    
    ###########################

    drawTriangle()
 
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5])) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global input_key
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_Q:
            input_key.insert(0,'q')
        elif key == glfw.KEY_E:
            input_key.insert(0,'e')
        elif key == glfw.KEY_A:
            input_key.insert(0,'a')
        elif key == glfw.KEY_D:
            input_key.insert(0,'d')
        elif key == glfw.KEY_1:
            input_key =[]
            input_key.append('1')


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025205", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)


    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


