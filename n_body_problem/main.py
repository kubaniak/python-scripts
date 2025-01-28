# n_body_simulation.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 6.67430e-11  # Gravitational constant

class Body:
    def __init__(self, position, velocity, mass, radius):
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.mass = mass
        self.radius = radius

    def update_position(self, dt):
        self.position += self.velocity * dt

    def update_velocity(self, force, dt):
        self.velocity += force / self.mass * dt
    
    def check_collision(self, other):
        distance = np.linalg.norm(self.position - other.position)
        return distance < self.radius + other.radius

    

def gravitational_force(body1, body2):
    distance = body2.position - body1.position
    r = np.linalg.norm(distance)
    if r == 0:
        return np.zeros(2)  # Avoid division by zero
    force_magnitude = G * body1.mass * body2.mass / r**2
    force_direction = distance / r
    return force_magnitude * force_direction

def update_bodies(bodies, dt):
    forces = [np.zeros(2) for _ in bodies]
    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if i != j:
                forces[i] += gravitational_force(body1, body2)
            # if body1.check_collision(body2):
            #     print(f'Collision between {i} and {j}')
    for i, body in enumerate(bodies):
        body.update_velocity(forces[i], dt)
        body.update_position(dt)

# Initialize bodies: position, velocity, mass
bodies = [
    Body([0, 0], [0, 0], 1.989e30, 696_340_000), # Sun
    Body([152e6, 0], [0, 29722], 5.972e24, 6_371_000), # Earth
    # Body([1.1e11, 0], [0, -2500], 1.898e27, 69_911_000), # Jupiter
]

time_factor = 50

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-2e7, 2e7)
ax.set_ylim(-2e7, 2e7)
lines = [ax.plot([], [], 'o')[0] for _ in range(len(bodies))]

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def animate(frame, time_factor=time_factor):
    update_bodies(bodies, dt=time_factor*3600)  # Update every hour
    for i, body in enumerate(bodies):
        lines[i].set_data([body.position[0]], [body.position[1]])
    return lines

# Create animation
ani = FuncAnimation(fig, animate, frames=1000, init_func=init, interval=20, blit=True)

plt.show()
