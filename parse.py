from display import *
from matrix import *
from draw import *

def parse(name, edges, triangles, m, s, c):
    f = open(name)
    lines = f.readlines()
    i = 0
    while i < len(lines):
        if lines[i] == "line\n":
            k = lines[i+1].split()
            add_edge(edges, [int(k[0]), int(k[1]), int(k[2])], [int(k[3]), int(k[4]), int(k[5])])
            i += 1
        elif lines[i] == "circle\n":
            k = lines[i+1].split()
            add_circle(edges, int(k[0]), int(k[1]), int(k[2]), int(k[3]), 0.01)
        elif lines[i] == "hermite\n":
            k = lines[i+1].split()
            add_hermite(edges, int(k[0]), int(k[1]), int(k[2]), int(k[3]), int(k[4]), int(k[5]), int(k[6]), int(k[7]), 0.01)
        elif lines[i] == "bezier\n":
            k = lines[i+1].split()
            add_bezier(edges, int(k[0]), int(k[1]), int(k[2]), int(k[3]), int(k[4]), int(k[5]), int(k[6]), int(k[7]), 0.01)
        elif lines[i] == "clear\n":
            edges = [[], [], [], []]
            triangles = [[], [], [], []]
        elif lines[i] == "box\n":
            k = lines[i+1].split()
            add_box(triangles, int(k[0]), int(k[1]), int(k[2]), int(k[3]), int(k[4]), int(k[5]))
        elif lines[i] == "sphere\n":
            k = lines[i+1].split()
            add_sphere(triangles, int(k[0]), int(k[1]), int(k[2]), int(k[3]), 0.05)
        elif lines[i] == "torus\n":
            k = lines[i+1].split()
            add_torus(triangles, int(k[0]), int(k[1]), int(k[2]), int(k[3]), int(k[4]), 0.05)
        elif lines[i] == "ident\n":
            m = identity(4)
        elif lines[i] == "scale\n":
            k = lines[i+1].split(" ")
            m = matrix_multiply(scale(float(k[0]), float(k[1]), float(k[2])), m)
            i += 1
        elif lines[i] == "move\n":
            k = lines[i+1].split(" ")
            m = matrix_multiply(translate(int(k[0]), int(k[1]), int(k[2])), m)
            i += 1
        elif lines[i] == "rotate\n":
            k = lines[i+1].split(" ")
            if k[0] == "x":
                m = matrix_multiply(rotatex(float(k[1])), m)
            elif k[0] == "y":
                m = matrix_multiply(rotatey(float(k[1])), m)
            elif k[0] == "z":
                m = matrix_multiply(rotatez(float(k[1])), m)
            i += 1
        elif lines[i] == "apply\n":
            edges = matrix_multiply(m, edges)
            triangles = matrix_multiply(m, triangles)
        elif lines[i] == "display\n":
            clear_screen(s)
            draw_2D_edges(edges, s, c)
            draw_3D_triangles(triangles, s, c)
            display(s)
        elif lines[i] == "save\n":
            clear_screen(s)
            draw_2D_edges(edges, s, c)
            draw_3D_triangles(triangles, s, c)
            save_ppm_ascii(s, lines[i+1])
        i += 1
