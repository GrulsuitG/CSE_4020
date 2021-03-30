import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    drawFrame()
    glColor3ub(255,255,255)
    drawTriangle()

    glColor3ub(0,0,255)
    glTranslate(0.6,0,0)
    glRotate(30, 0, 0, 1)
    drawTriangle()
    drawFrame()

    glLoadIdentity()
    glColor3ub(255,0,0)
    glRotate(30, 0, 0, 1)
    glTranslate(0.6, 0, 0)
    drawTriangle()
    drawFrame()
    


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.]))
    glEnd()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([.5,0.]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025205", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


