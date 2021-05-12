from display import *
from matrix import *
import math

def add_point(m, p):
    for i in range(3):
        m[i].append(p[i])
    m[3].append(1)

def add_edge(m, p1, p2):
    add_point(m, p1)
    add_point(m, p2)

def add_triangle(m, p1, p2, p3):
    add_point(m, p1)
    add_point(m, p2)
    add_point(m, p3)

def add_circle(m, cx, cy, cz, r, step):
    t = 0.0
    while t < 1.0:
        add_edge(m, [cx + r * math.cos(2 * math.pi * t), cy + r * math.sin(2 * math.pi * t), cz], [cx + r * math.cos(2 * math.pi * (t+step)), cy + r * math.sin(2 * math.pi * (t+step)), cz])
        t += step

def add_hermite(m, x0, y0, x1, y1, rx0, ry0, rx1, ry1, step):
    t = 0.0
    hermite = [[2.0, -2.0, 1.0, -1.0], [-3.0, 3.0, -2.0, 1.0], [0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0]]
    px = [[x0], [x1], [rx0], [rx1]]
    py = [[y0], [y1], [ry0], [ry1]]
    while t < 1.0:
        coefx = matrix_multiply(hermite, px)
        coefy = matrix_multiply(hermite, py)
        p1 = [coefx[0][0]*t**3+coefx[1][0]*t**2+coefx[2][0]*t+coefx[3][0], coefy[0][0]*t**3+coefy[1][0]*t**2+coefy[2][0]*t+coefy[3][0], 0]
        t += step
        p2 = [coefx[0][0]*t**3+coefx[1][0]*t**2+coefx[2][0]*t+coefx[3][0], coefy[0][0]*t**3+coefy[1][0]*t**2+coefy[2][0]*t+coefy[3][0], 0]
        add_edge(m, p1, p2)

def add_bezier(m, x0, y0, x1, y1, x2, y2, x3, y3, step):
    t = 0.0
    bezier = [[-1.0, 3.0, -3.0, 1.0], [3.0, -6.0, 3.0, 0.0], [-3.0, 3.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]]
    px = [[x0], [x1], [x2], [x3]]
    py = [[y0], [y1], [y2], [y3]]
    while t < 1.0:
        coefx = matrix_multiply(bezier, px)
        coefy = matrix_multiply(bezier, py)
        p1 = [coefx[0][0]*t**3+coefx[1][0]*t**2+coefx[2][0]*t+coefx[3][0], coefy[0][0]*t**3+coefy[1][0]*t**2+coefy[2][0]*t+coefy[3][0], 0]
        t += step
        p2 = [coefx[0][0]*t**3+coefx[1][0]*t**2+coefx[2][0]*t+coefx[3][0], coefy[0][0]*t**3+coefy[1][0]*t**2+coefy[2][0]*t+coefy[3][0], 0]
        add_edge(m, p1, p2)

def add_box(m, x, y, z, w, h, d):
    x1 = x + w
    y1 = y - h
    z1 = z - d

    add_triangle(m, [x, y, z], [x, y, z1], [x, y1, z])
    add_triangle(m, [x, y, z], [x, y1, z], [x1, y, z])
    add_triangle(m, [x, y, z], [x1, y, z], [x, y, z1])
    add_triangle(m, [x1, y1, z], [x1, y, z], [x, y1, z])
    add_triangle(m, [x1, y1, z], [x, y1, z], [x1, y1, z1])
    add_triangle(m, [x1, y1, z], [x1, y1, z1], [x1, y, z])
    add_triangle(m, [x1, y, z1], [x1, y, z], [x1, y1, z1])
    add_triangle(m, [x1, y, z1], [x1, y1, z1], [x, y, z1])
    add_triangle(m, [x1, y, z1], [x, y, z1], [x1, y, z])
    add_triangle(m, [x, y1, z1], [x, y1, z], [x, y, z1])
    add_triangle(m, [x, y1, z1], [x, y, z1], [x1, y1, z1])
    add_triangle(m, [x, y1, z1], [x1, y1, z1], [x, y1, z])

def sphere_points(m, cx, cy, cz, r, step):
    spheres = []
    theta = 0.0
    while theta < 1.0:
        phi = 0.0
        while phi < 1.0:
            x = cx + r * math.cos(math.pi*phi)
            y = cy + r * math.sin(math.pi*phi) * math.cos(2*math.pi*theta)
            z = cz + r * math.sin(math.pi*phi) * math.sin(2*math.pi*theta)
            spheres.append([x, y, z])
            phi += step
        theta += step
    return spheres

def add_sphere(m, cx, cy, cz, r, step):
    spheres = sphere_points(m, cx, cy, cz, r, step)
    steps = int(1/step)
    for a in range(steps):
        for b in range(steps-1):
            i = a * steps + b
            j = i + steps
            p0 = spheres[i]
            p1 = spheres[i+1]
            p2 = spheres[j%len(spheres)]
            p3 = spheres[(j+1)%len(spheres)]

            add_triangle(m, p1, p3, p2)
            add_triangle(m, p0, p1, p2)

def torus_points(m, cx, cy, cz, r1, r2, step):
    torus = []
    theta = 0.0
    while theta <= 1.0:
        phi = 0.0
        while phi <= 1.0:
            x = cx + math.cos(2*math.pi*phi) * (r1*math.cos(2*math.pi*theta) + r2)
            y = cy + r1 * math.sin(2*math.pi*theta)
            z = cz - math.sin(2*math.pi*phi) * (r1*math.cos(2*math.pi*theta) + r2)
            torus.append([x, y, z])
            phi += step
        theta += step
    return torus

def add_torus(m, cx, cy, cz, r1, r2, step):
    torus = torus_points(m, cx, cy, cz, r1, r2, step)
    steps = int(1/step)
    for a in range(steps):
        for b in range(steps):
            i = a * steps + b
            j = i + steps
            p0 = torus[i]
            p1 = torus[(i+1)%len(torus)]
            p2 = torus[j%len(torus)]
            p3 = torus[(j+1)%len(torus)]

            add_triangle(m, p1, p3, p2)
            add_triangle(m, p0, p1, p2)

def draw_line(x0, y0, x1, y1, screen, color):
    if abs(x1 - x0) > abs(y1 - y0):
        if x1 > x0:
            draw_linex(x0, y0, x1, y1, screen, color)
        else:
            draw_linex(x1, y1, x0, y0, screen, color)
    else:
        if y1 > y0:
            draw_liney(x0, y0, x1, y1, screen, color)
        else:
            draw_liney(x1, y1, x0, y0, screen, color)

def draw_linex(x0, y0, x1, y1, screen, color):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    A = abs(y1 - y0)
    a = y1 - y0
    k = 1 if A == a else -1
    B = x1 - x0
    Z = 2 * B - A
    y = y0
    for x in range(x0, x1):
        plot(screen, color, x, y)
        if Z > 0:
            y += k
            Z -= 2 * B
        Z += 2 * A

def draw_liney(x0, y0, x1, y1, screen, color):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    B = y1 - y0
    A = abs(x1 - x0)
    a = x1 - x0
    k = 1 if A == a else -1
    Z = 2 * B - A
    x = x0
    for y in range(y0, y1):
        plot(screen, color, x, y)
        if Z > 0:
            x += k
            Z -= 2 * B
        Z += 2 * A

def draw_2D_edges(m, screen, color):
    for i in range(0, len(m[0]), 2):
        draw_line(m[0][i], m[1][i], m[0][i+1], m[1][i+1], screen, color)

def draw_3D_triangles(m, screen, color):
    for i in range(0, len(m[0]), 3):
        if dot_product(normal(m, i), [0, 0, 1]) > 0:
            draw_line(m[0][i], m[1][i], m[0][i+1], m[1][i+1], screen, color)
            draw_line(m[0][i+2], m[1][i+2], m[0][i+1], m[1][i+1], screen, color)
            draw_line(m[0][i], m[1][i], m[0][i+2], m[1][i+2], screen, color)
