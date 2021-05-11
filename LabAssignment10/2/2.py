import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.
tr =0

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    if l == 0:
        return np.array([0,0,0])
    return (1/l) * np.array(v)

def render(t):
    global gCamAng, gCamHeight, tr
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    objectColor = (1.,.0,.0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    Ma1, Ma2 = draw(20,30,30,15,30,25)

    objectColor = (1.,1.,.0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    Mb1, Mb2 = draw(45,60,40,25,40,40)

    objectColor = (.0,1.,.0,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    Mc1, Mc2 = draw(60,70,40,40,60,50)

    objectColor = (.0,.0,.1,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    Md1, Md2 = draw(80,85,70,55,80,65)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor) 
    
    R1 = np.identity(4)
    if tr <= 1:
        M = slerp(Ma1[:3,:3], Mb1[:3,:3], tr)
    elif 1 <= tr and tr <= 2 :
        M = slerp(Mb1[:3,:3], Mc1[:3,:3], tr-1)
    elif 2 <= tr :
        M = slerp(Mc1[:3,:3], Md1[:3,:3], tr-2)
    R1[:3,:3] = M
    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R2 = np.identity(4)
    T1 = np.identity(4)
    T1[0][3] = 1.

    if tr < 1.:
        M = slerp(Ma2[:3,:3], Mb2[:3,:3], tr)
    elif 1 <= tr and tr < 2 :
        M = slerp(Mb2[:3,:3], Mc2[:3,:3], tr-1)
    elif 2 <= tr :
        M = slerp(Mc2[:3,:3], Md2[:3,:3], tr-2)
    R2[:3,:3] = M

    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    tr = (tr+0.05)%3

    glDisable(GL_LIGHTING)

def draw(x1,y1,z1,x2,y2,z2):  
    R1 = np.identity(4)
    M1 = CalcMatrix(x1,y1,z1)
    R1[:3,:3] = M1
    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R2 = np.identity(4)
    M2 = CalcMatrix(x2, y2, z2)
    R2[:3,:3] = M2
    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    return R1, R2


def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def exp(rv):
    theta = l2norm(rv)
    rv = normalized(rv)
    cos = np.cos(theta)
    sin = np.sin(theta)
    x = rv[0]
    y = rv[1]
    z = rv[2]
    R = np.array([[cos+x*x*(1-cos), x*y*(1-cos)-z*sin, x*z*(1-cos)+y*sin],
                  [y*x*(1-cos)+z*sin, cos+y*y*(1-cos), y*z*(1-cos)-x*sin],
                  [z*x*(1-cos)-y*sin, z*y*(1-cos)+x*sin, cos+z*z*(1-cos)]])
    return R

def log(R):
    tr = R[0][0] + R[1][1] +R[2][2]
    if tr == 3:
        return np.array([0, 0, 0])
    elif tr == -1:
        theta = 180
        w = (1/np.sqrt(2*(1+R[2][2])))*(R[0][2], R[1][2], 1+R[2][2])
        normalized(w)
        return np.array(theta*w)
    else :
        theta = np.arccos((tr-1)/2) 
        rv = np.array([(R[2][1] - R[1][2])/(2*np.sin(theta)), 
                        (R[0][2] - R[2][0])/(2*np.sin(theta)), 
                        (R[1][0] - R[0][1])/(2*np.sin(theta))])
        return theta*rv

def slerp(R1, R2, t):
    temp = R1.T @ R2
    r = t * log(temp)
    M = R1 @ exp(r)
    return M   

def CalcMatrix(x,y,z):
    xr = np.radians(x)
    yr = np.radians(y)
    zr = np.radians(z)
    X = np.array([[1, 0 ,0],
                  [0, np.cos(xr), -np.sin(xr)],
                  [0, np.sin(xr), np.cos(xr)]])
    Y = np.array([[np.cos(yr), 0,np.sin(yr)],
                 [0 , 1, 0],
                 [-np.sin(yr), 0, np.cos(yr)]])
    Z = np.array([[np.cos(zr), -np.sin(zr),0],
                  [np.sin(zr), np.cos(zr), 0],
                  [0 , 0, 1]])
    return X @ Y @ Z
    #  return X


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016025205', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = glfw.get_time()
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()


