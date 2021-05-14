# A class module for a 3D model and material

##    An adaption of Will McGugan's code for Beginning Game Development with Python and Pygame
##
##    Copyright 2007 Will McGugan
##
##    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##
##    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
##
##    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
##
##    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
##    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
##    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
##    TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##

# A few imports we will need for later
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
import os.path
from m_matrix44 import Matrix44 as Matrix
from m_vector3 import Vector3 as Vector3

class Material(object):

    def __init__(self):
        self.name = ""
        self.texture_fname = None
        self.texture_id = None

class FaceGroup(object):

    def __init__(self):

        self.tri_indices = []
        self.material_name = ""

class Model3D(object):

    def __init__(self):

        self.vertices = []
        self.tex_coords = []
        self.normals = []
        self.materials = {}
        self.face_groups = []
        # Display list id for quick rendering
        self.display_list_id = None

    def read_obj(self, fname):

        current_face_group = None
        file_in = open(fname) # changed file to open()

        for line in file_in:

            # Parse command and data from each line
            words = line.split()
            command = words[0]
            data = words[1:]

            if command == "mtllib": # Material Library

                # find the file name of the texture
                model_path = os.path.split(fname)[0]
                mtllib_path = os.path.join(model_path, data[0])
                self.read_mtllib(mtllib_path)

            elif command == "v":    # Vertex
                x, y, z = data
                vertex = (float(x), float(y), float(z))
                self.vertices.append(vertex)

            elif command == "vt":   # Texture coordinate
                s, t = data
                tex_coord = (float(s), float(t))
                self.tex_coords.append(tex_coord)

            elif command == "vn":   # Normal
                x, y, z = data
                normal = (float(x), float(y), float(z))
                self.normals.append(normal)

            elif command == "usemtl":   # Use material
                current_face_group = FaceGroup()
                current_face_group.material_name = data[0]
                self.face_groups.append(current_face_group)

            elif command == "f":

                assert len(data) == 3, "Sorry only triangles are supported"

                # Parse indices from triples
                for word in data:
                    vi, ti, ni = word.split('/')
                    # Subtract 1 because Obj indexes start at one rather than zero
                    indices = (int(vi)-1, int(ti)-1, int(ni)-1)
                    current_face_group.tri_indices.append(indices)

        # Read all the textures used in the model
        for material in iter(self.materials.values()):  # changed itervalues() to iter()

            model_path = os.path.split(fname)[0]
            print("model_path: ", model_path)
            texture_path = os.path.join(model_path, material.texture_fname)
            print("texture_path: ", texture_path)
            texture_surface = pygame.image.load(texture_path)
            texture_data = pygame.image.tostring(texture_surface, 'RGB', True)

            # Create and bind a texture id
            material.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, material.texture)

            glTexParameteri(GL_TEXTURE_2D,
                            GL_TEXTURE_MAG_FILTER,
                            GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,
                            GL_TEXTURE_MIN_FILTER,
                            GL_LINEAR_MIPMAP_LINEAR)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

            # Upload texture and build map-maps
            width, height = texture_surface.get_rect().size
            gluBuild2DMipmaps(GL_TEXTURE_2D,
                              3,
                              width,
                              height,
                              GL_RGB,
                              GL_UNSIGNED_BYTE,
                              texture_data)

    def read_mtllib(self, mtl_fname):
        # Parsing the material library
        file_mtllib = open(mtl_fname) # changed file() to open()
        for line in file_mtllib:
            words = line.split()
            command = words[0]
            data = words[1:]

            if command == "newmtl":
                material = Material()
                material.name = data[0]
                self.materials[data[0]] = material

            elif command == "map_Kd":
                material.texture_fname = data[0]

    def draw(self):
        vertices = self.vertices
        tex_coords = self.tex_coords
        normals = self.normals

        for face_group in self.face_groups:

            # Bind the texture for this face group
            material = self.materials[face_group.material_name]
            glBindTexture(GL_TEXTURE_2D, material.texture)

            # Send the geometry to OpenGL
            glBegin(GL_TRIANGLES)
            for vi, ti, ni in face_group.tri_indices:
                glTexCoord2fv(tex_coords[ti])
                glNormal3fv(normals[ni])
                glVertex3fv(vertices[vi])
            glEnd()

    def draw_quick(self):

        if self.display_list_id is None:
            # Generate and compile a display list that renders the geometry
            self.display_list_id = glGenLists(1)
            glNewList(self.display_list_id, GL_COMPILE)
            self.draw()
            glEndList()

        glCallList(self.display_list_id)

    def __del__(self):

        # Called when the model is cleaned up by Python
        self.free_resources()

    def free_resources(self):

        # Delete the display list
        if self.display_list_id is not None:
            glDeleteLists(self.display_list_id, 1)
            self.display_list_id = None

        # Delete any textures we used
        for material in iter(self.materials.values()): # changed itervalues() to iter()
            if material.texture_id is not None:
                glDeleteTextures(material.texture_id)

        # Clear all the materials
        self.materials.clear()

        # Clear all the geometry lists
        del self.vertices[:]
        del self.tex_coords[:]
        del self.normals[:]
        del self.face_groups[:]

    def scale_object(self, x_factor=1, y_factor=1, z_factor=1):
        new_vertices = []
        for vertex in self.vertices:
            new_vertex = (vertex[0]*x_factor, vertex[1]*y_factor, vertex[2]*z_factor)
            new_vertices.append(new_vertex)
        self.vertices = new_vertices

    def translate_object_y(self):
        y_points = []
        for vertex in self.vertices:
            y_points.append(vertex[1])
        max_height = max(y_points)
        translation_matrix = Matrix.translation(0, max_height, 0)

        new_points = []
        for vertex in self.vertices:
            old_vertex = Vector3(vertex)
            new_vertex = translation_matrix.transform(old_vertex)
            new_points.append(new_vertex)
        self.vertices = new_points

    def translate_object(self, x_factor=0, y_factor=0, z_factor=0):
        # this only definitely works in the y direction
        x_points = []
        y_points = []
        z_points = []
        for vertex in self.vertices:
            # split up the measurements of the object
            x, y, z = vertex
            x_points.append(x)
            y_points.append(y)
            z_points.append(z)
        # find the maximum dimensions
        max_x = max(x_points) - min(x_points)
        max_y = max(y_points) - min(y_points)
        max_z = max(z_points) - min(z_points)
        # find the translation distance
        translate_x = max_x * x_factor
        translate_y = max_y * y_factor
        translate_z = max_z * z_factor
        # create the translation matrix
        translation_matrix = Matrix.translation(translate_x,
                                                translate_y,
                                                translate_z)
        # transform each individual vertex
        new_points = []
        for vertex in self.vertices:
            old_vertex = Vector3(vertex)
            new_vertex = translation_matrix.transform(old_vertex)
            new_points.append(new_vertex)
        self.vertices = new_points
        

if __name__ == "__main__":
    print ("Import as a module")
