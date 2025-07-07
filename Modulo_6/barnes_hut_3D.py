import numpy as np
from numpy.linalg import norm

class Body:
    def __init__(self, m, x, y, z):
        self.m = m
        self.m_pos = m * np.array([x, y, z])
        self.momentum = np.array([0., 0., 0.])
        self.relpos = self.pos().copy()
        self.s = 1.0
        self.child = None

    def pos(self):
        return self.m_pos / self.m

    def reset_to_root(self):
        self.s = 1.0
        self.relpos = self.pos().copy()

    def into_next_octant(self):
        self.s *= 0.5
        idx = 0
        for i in range(3):
            self.relpos[i] *= 2.0
            if self.relpos[i] >= 1.0:
                idx += 2 ** i
                self.relpos[i] -= 1.0
        return idx

    def dist(self, other):
        return norm(other.pos() - self.pos())

    def force_on(self, other):
        cutoff = 0.002
        d = self.dist(other)
        if d < cutoff:
            return np.zeros(3)
        return (self.pos() - other.pos()) * (self.m * other.m / d**3)

def add(body, node):
    if node is None:
        return body
    smallest = 1e-4
    if node.s <= smallest:
        return node  # stop subdividing
    if node.child is None:
        new_node = Body(node.m, *node.pos())
        new_node.momentum = node.momentum.copy()
        new_node.child = [None] * 8
        idx_old = node.into_next_octant()
        new_node.child[idx_old] = node
    else:
        new_node = node
    new_node.m += body.m
    new_node.m_pos += body.m_pos
    idx_new = body.into_next_octant()
    new_node.child[idx_new] = add(body, new_node.child[idx_new])
    return new_node

def force_on(body, node, theta):
    if node.child is None:
        return node.force_on(body)
    d = node.dist(body)
    if node.s < d * theta:
        return node.force_on(body)
    total = np.zeros(3)
    for c in node.child:
        if c is not None:
            total += force_on(body, c, theta)
    return total

def verlet(bodies, root, theta, G, dt):
    for b in bodies:
        f = G * force_on(b, root, theta)
        b.momentum += dt * f
    for b in bodies:
        b.m_pos += dt * b.momentum

# ---------- SIMULACIÓN PRINCIPAL ----------

theta = 0.5
mass = 1.0
ini_radius = 0.1
inivel = 0.1
G = 4e-6
dt = 1e-3
numbodies = 1000
max_iter = 501

np.random.seed(1)

# Posiciones iniciales dentro del cubo
posx = np.random.rand(numbodies) * 2 * ini_radius + 0.5 - ini_radius
posy = np.random.rand(numbodies) * 2 * ini_radius + 0.5 - ini_radius
posz = np.random.rand(numbodies) * 2 * ini_radius + 0.5 - ini_radius

positions = np.stack((posx, posy, posz), axis=-1)
radii = norm(positions - np.array([0.5, 0.5, 0.5]), axis=1)
positions = positions[radii < ini_radius]

bodies = [Body(mass, *p) for p in positions]

# Momento angular en plano XY, componente z inicial = 0
for b in bodies:
    r = b.pos() - np.array([0.5, 0.5, b.pos()[2]])
    radius = norm(r)
    b.momentum = np.array([-r[1], r[0], 0.]) * mass * inivel * radius / ini_radius

# Bucle de simulación
for i in range(max_iter):
    root = None
    for b in bodies:
        b.reset_to_root()
        root = add(b, root)
    verlet(bodies, root, theta, G, dt)
    if i == 500:
        z = bodies[0].pos()[2]
        print(f"Componente z del primer cuerpo en i=500: {z:.6f} m")
