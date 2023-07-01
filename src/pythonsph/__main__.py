"""
Python 2D SPH by Alexandre Sajus

This script generates a 2D animation of a dam break using Smoothed Particle Hydrodynamics

More information at:
https://github.com/AlexandreSajus
https://web.archive.org/web/20090722233436/http://blog.brandonpelfrey.com/?p=303
"""

import sys
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

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


def update(particles: list[Particle], dam: bool) -> list[Particle]:
    """
    Calculates a step of the simulation
    """
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
fig = plt.figure()
axes = fig.add_subplot(xlim=(-SIM_W, SIM_W), ylim=(-SIM_W, SIM_W))
(POINTS,) = axes.plot([], [], "bo", ms=20)
axes.set_aspect('equal')

simulation_state = physics.start_circle(SIM_R, SIM_CEN_X, SIM_CEN_Y, SIM_FILL_TOP, SIM_FILL_SPACING)

if not simulation_state:
    print("No particles generated, exiting")
    sys.exit(-1)

frame = 0

dam_built = False

# Animation function
def animate(i: int):
    """
    Animates the simulation in matplotlib

    Args:
        i: frame number

    Returns:
        points: the points to be plotted
    """
    global simulation_state, frame, dam_built
    if frame == 250:  # Break the dam at frame 250
        print("Breaking the dam")
        dam_built = False
    simulation_state = update(simulation_state, dam_built)
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


ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)
plt.show()
