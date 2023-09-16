# thanks chatgpt

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import json

rotate_multi = 4

# Define the 3D cube vertices
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
], dtype=np.float32)

# Define the cube's edges
edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
)

# Initialize Pygame
pygame.init()
display = (500, 500)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set the camera position
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glFrustum(-1, 1, -1, 1, 1, 50)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0, 0, -5)
glRotatef(45, 60, 60, 60)

screen_positions = []

# Main render loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Write the screen positions to a JSON file
            with open('bombie/anim_3d.json', 'w') as json_file:
                json.dump(screen_positions, json_file)
            running = False

    glRotatef(1*rotate_multi, 3*rotate_multi, 1*rotate_multi, 3*rotate_multi)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Render the cube
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Get the screen positions of vertices
    viewport = glGetIntegerv(GL_VIEWPORT)
    
    screen_positions.append([])
    for vertex in vertices:
        vertex_homogeneous = np.append(vertex, 1.0)
        modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
        screen_vertex = np.dot(np.dot(vertex_homogeneous, modelview_matrix), projection_matrix)
        screen_vertex /= screen_vertex[3]
        x, y, z, w = screen_vertex
        x = int((x + 1) * 0.5 * viewport[2] + viewport[0])
        y = int((y + 1) * 0.5 * viewport[3] + viewport[1])
        screen_positions[-1].append((x, y))

    pygame.display.flip()
    pygame.time.wait(1)

pygame.quit()
