# This chunky thing handles the overall running of the UI

SCREEN_SIZE = (800, 600)

from math import radians
import os

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from tkinter import *

# import a 4x4 matrix and vector3 for camera control
from m_matrix44 import Matrix44
from m_vector3 import Vector3

# Import the Model3D class
import m_model3d as m_model3d

# import gui application
from m_gui import Application

# import the assembly
from m_assembly import Assembly

def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.) # edited 40 from 60
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():

    # Enable the GL features we will be using
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)

    glShadeModel(GL_SMOOTH)
    glClearColor(1.0, 1.0, 1.0, 0.0)    # white

    # Set the material
    glMaterial(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glMaterial(GL_FRONT, GL_DIFFUSE, (0.2, 0.2, 0.2, 1.0))
    glMaterial(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterial(GL_FRONT, GL_SHININESS, 10.0)

    # Set the light parameters
    glLight(GL_LIGHT0, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glLight(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 1.0))
    glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Enable light 1 and set position
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSITION, (0, .5, 1, 0))

def run():
    
    # setting up the tkinter window
    root = Tk()

    embed = Frame(root, width = 800, height = 600) # creates an embed frame for a pygame window

    app = Application(root)
    root.update()

    # setting up the program sharing
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    # setting up the pygame display
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()

    clock = pygame.time.Clock()

    # initialising camera transform stuff
    # camera transformation matrix
    camera_matrix = Matrix44()
    camera_matrix.translate = (10.0, .6, 10.0)

    # initialise speeds and directions
    rotation_direction = Vector3()
    # rotation_speed = 45 - defined in the while loop to allow adjustability
    movement_direction = Vector3()
    # movement_speed = 1 - defined in the while loop to allow adjustability
    
    # initialize the position and components
    #working_position = 0 # the position where the next component will be placed
    #components = {0: None, 1: None, 2: None} # 3 empty components to begin

    # maximum number of components allowed
    #MAX_COMPONENTS = 3

    assembly = Assembly(3)

    rotation = Vector3()
    movement = Vector3()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        time_passed = clock.tick()
        time_passed_seconds = time_passed/1000.0

        pressed_keys = pygame.key.get_pressed()#

        # collect input from the GUI
        root.update()

        # set the speeds for movement for the component
        rotation_speed = 45
        movement_speed = 1

        # reset rotation and movement directions
        rotation_direction.set(0.0, 0.0, 0.0)
        movement_direction.set(0.0, 0.0, 0.0)

        if app.add_comp_b:
            # add a blue component to the working position
            if assembly.room_for_more(): # check we haven't reached the build limit
                app.update_text("adding blue component")
                assembly.add_component("b.obj")
                if assembly.need_join():
                    assembly.set_joint(app.create_joining_popup())
            else:
                app.update_text("build limit reached")
            app.add_comp_b = False

        if app.add_comp_g:
            # add a green component to the working position
            if assembly.room_for_more(): # check we haven't reached the build limit
                app.update_text("adding green component")
                assembly.add_component("g.obj")
                if assembly.need_join():
                    assembly.set_joint(app.create_joining_popup())
            else:
                app.update_text("build limit reached")
            app.add_comp_g = False

        if app.add_comp_p:
            # add a pink component to the working position
            if assembly.room_for_more(): # check we haven't reached the build limit
                app.update_text("adding pink component")
                assembly.add_component("p.obj")
                if assembly.need_join():
                    assembly.set_joint(app.create_joining_popup())                     
            else:
                app.update_text("build limit reached")
            app.add_comp_p = False

        if app.add_comp_r:
            # add a red component to the working position
            if assembly.room_for_more(): # check we haven't reached the build limit
                app.update_text("adding red component")
                assembly.add_component("r.obj")
                if assembly.need_join():
                    assembly.set_joint(app.create_joining_popup())
            else:
                app.update_text("build limit reached")
            app.add_comp_r = False

        if app.add_comp_y:
            # add a yellow component to the working position
            if assembly.room_for_more(): # check we haven't reached the build limit
                app.update_text("adding yellow component")
                assembly.add_component("y.obj")
                if assembly.need_join():
                    assembly.set_joint(app.create_joining_popup())
            else:
                app.update_text("build limit reached")
            app.add_comp_y = False

        if app.delete:
            # remove the top block
            if assembly.get_working_position() != 0:
                assembly.delete_component()
                app.update_text("removed last component")
            else:
                app.update_text("no components to remove")
            app.delete = False

# could add shift for micro movements - apparently this doesnt work at all but cba to take it back out
        if app.rot_y_pos:
            # rotate clockwise about the y axis
            if pressed_keys[K_LSHIFT]: # allows for micro adjustments
                rotation_speed = 10
                app.update_text("rotating +y")
            else:
                app.update_text("rotating +++y")
            rotation_direction.y = +1.0
            app.rot_y_pos = False
        elif app.rot_y_neg:
            # rotate anticlockwise about the y axis
            if pressed_keys[K_LSHIFT]:
                rotation_speed = 10
                app.update_text("rotating -y")
            else:
                app.update_text("rotating ---y")
            rotation_direction.y = -1.0
            app.rot_y_neg = False

        if app.rot_x_neg:
            # rotate anti-clockwise about the x axis
            if pressed_keys[K_LSHIFT]:
                rotation_speed = 10
                app.update_text("rotating -x")
            else:
                app.update_text("rotating ---x")
            rotation_direction.x = -1.0
            app.rot_x_neg = False
        elif app.rot_x_pos:
            # rotate clockwise about the x axis
            if pressed_keys[K_LSHIFT]:
                rotation_speed = 10
                app.update_text("rotating +x")
            else:
                app.update_text("rotating +++x")
            rotation_direction.x = +1.0
            app.rot_x_pos = False

        if app.rot_z_neg:
            # rotate clockwise about z axiz
            if pressed_keys[K_LSHIFT]:
                app.update_text("rotating -z")
                rotation_speed = 10
            else:
                app.update_text("rotating ---z")
            rotation_direction.z = -1.0
            app.rot_z_neg = False            
        elif app.rot_z_pos:
            # rotate anti-clockwise about z axis
            if pressed_keys[K_LSHIFT]:
                app.update_text("rotating +z")
                rotation_speed = 10
            else:
                app.update_text("rotating +++z")
            rotation_direction.z = +1.0
            app.rot_z_pos = False

        if app.mov_z_neg:
            # zoom out
            if pressed_keys[K_LSHIFT]:
                app.update_text("small zoom out")
                movement_speed = 0.2
            else:
                app.update_text("big zoom out")
            movement_direction.z = -1.0
            app.mov_z_neg = False
        elif app.mov_z_pos:
            # zoom in
            if pressed_keys[K_LSHIFT]:
                app.update_text("small zoom in")
                movement_speed = 0.2
            else:
                app.update_text("big zoom in")
            movement_direction.z = +1.0
            app.mov_z_pos = False

        # attempting the export cycle
        if app.wants_to_export:
            if assembly.ready_to_export():
                if app.create_export_popup():
                    assembly.create_save_file(app.create_save_popup())
                    app.update_text("export successful")
            else:
                app.export_error_popup()
                app.update_text("export failed")
            app.wants_to_export = False

        # calculate the rotation matrix and multiply by the camera matrix
        rotation += rotation_direction * rotation_speed #* time_passed_seconds
        # calculate movement and add it to the camera matrix translate
        heading = Vector3(camera_matrix.forward)
        movement += heading * movement_direction.z * movement_speed
        
        glLoadIdentity()
        glRotatef(15, 1, 0, 0)
        glTranslatef(0.0, -2, -5)
        
        glRotatef(rotation.x, 1, 0, 0)
        glRotatef(rotation.y, 0, 1, 0)
        glRotatef(rotation.z, 0, 0, 1)

        glTranslatef(movement.x, movement.y, movement.z)
        
        assembly.render_components()

        # show the screen
        pygame.display.flip()


if __name__ == "__main__":
    run()
