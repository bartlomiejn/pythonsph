"""
Python 2D SPH by Alexandre Sajus

This script generates a 2D animation of a dam break using Smoothed Particle Hydrodynamics

More information at:
https://github.com/AlexandreSajus
https://web.archive.org/web/20090722233436/http://blog.brandonpelfrey.com/?p=303
"""

import sys
import random
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from math import sqrt

import pythonsph
from pythonsph.config import Config
from pythonsph.particle import Particle
import pythonsph.physics as physics 

(
    N,
    SIM_W,
    BOTTOM, 
    SIM_R,
    SIM_CEN_X,
    SIM_CEN_Y,
    SIM_FILL_TOP,
    SIM_FILL_SPACING,
    DAM,
    DAM_BREAK,
    G,
    SPACING,
    K,
    K_NEAR,
    REST_DENSITY,
    R,
    SIGMA,
    MAX_VEL,
    WALL_DAMP,
    VEL_DAMP,
) = Config().return_config()

def in_circle(x, y, circ_x, circ_y, circ_r):
    dx = x - circ_x
    dy = y - circ_y
    distance = sqrt(dx*dx + dy*dy)
    return distance < (circ_r * 1.01)

def init_circle(r, cen_x, cen_y, top, spacing) -> list[Particle]:
    result = []

    x_left = cen_x - r
    x_right = cen_x + r
    y_bottom = cen_y - r
    y_top = top
    stride = spacing

    y_pos = y_top
    while y_pos >= y_bottom:
        x_pos = x_left
        while x_pos <= x_right:
            if not in_circle(x_pos, y_pos, cen_x, cen_y, r):
                x_pos += stride
                continue
            result.append(Particle(x_pos, y_pos))
            x_pos += stride
        y_pos -= stride

    return result

def update(particles: list[Particle], dam: bool) -> list[Particle]:
    # Update the state of the particles (apply forces, reset values, etc.)
    for particle in particles:
        particle.update_state(dam)

    # Calculate density
    physics.calculate_density(particles)

    # Calculate pressure
    for particle in particles:
        particle.calculate_pressure()

    # Apply pressure force
    physics.create_pressure(particles)

    # Apply viscosity force
    physics.calculate_viscosity(particles)

    return particles

# Setup matplotlib
frame = 0
fig = plt.figure()
axes = fig.add_subplot(xlim=(-SIM_W, SIM_W), ylim=(-SIM_W, SIM_W))
(POINTS,) = axes.plot([], [], "bo", ms=20)
axes.set_aspect('equal')

simulation_state = init_circle(SIM_R, SIM_CEN_X, SIM_CEN_Y, SIM_FILL_TOP, SIM_FILL_SPACING)
particle_count = [len(simulation_state)]
particle_max = int(particle_count[0] / 0.4)

if not simulation_state:
    print("No particles generated, exiting")
    sys.exit(-1)

def animate(i: int):
    global simulation_state, frame

    simulation_state = update(simulation_state, False)
    # Create an array with the x and y coordinates of the particles
    visual = np.array(
        [
            [particle.visual_x_pos, particle.visual_y_pos]
            for particle in simulation_state
        ]
    )
    POINTS.set_data(visual[:, 0], visual[:, 1])  # Updates the position of the particles
    
    frame += 1

    return (POINTS,)

def append_rand_circle(sim_particles, count, r, cen_x, cen_y, top):
    x_left = cen_x - r
    x_right = cen_x + r
    y_bottom = cen_y - r
    y_top = top

    while count > 0:
        x_pos = random.uniform(x_left, x_right)
        y_pos = random.uniform(y_bottom, y_top)
        if in_circle(x_pos, y_pos, cen_x, cen_y, r):
            sim_particles.append(Particle(x_pos, y_pos))
            count -= 1

def spawn_particles(sim_particles, count, fill_top):
    append_rand_circle(sim_particles, count, SIM_R, SIM_CEN_X, SIM_CEN_Y, fill_top) 

def remove_particles(sim_particles, existing_count, count):
    while count > 0 and existing_count[0] > 1:
        del sim_particles[-1]
        existing_count[0] -= 1
        count -= 1

axcolor = 'lightgoldenrodyellow'
ax = plt.axes([0.175, 0.0, 0.65, 0.03], facecolor=axcolor) 
slider = Slider(ax, 'Fill', 0, 1.0, valinit=0.4)
def update_slider(val):
    global simulation_state, particle_count
    diff = int(val*particle_max - particle_count[0])
    print(diff)
    if diff > 0:
        print(f"update slider: {val}, current particle count: {particle_count[0]}, new count: {particle_count[0] + diff}")
        particle_count[0] += diff
        spawn_particles(simulation_state, diff, val)
    elif diff < 0 and particle_count[0] > 1:
        remove_particles(simulation_state, particle_count, abs(diff))
    
slider.on_changed(update_slider)

ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)
plt.show()
