"""Defines the Particle class."""

from math import sqrt
from pythonsph.config import Config


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


class Particle:
    """
    A single particle of the simulated fluid

    Attributes:
        x_pos: x position of the particle
        y_pos: y position of the particle
        previous_x_pos: x position of the particle in the previous frame
        previous_y_pos: y position of the particle in the previous frame
        visual_x_pos: x position of the particle that is shown on the screen
        visual_y_pos: y position of the particle that is shown on the screen
        rho: density of the particle
        rho_near: near density of the particle, used to avoid collisions between particles
        press: pressure of the particle
        press_near: near pressure of the particle, used to avoid collisions between particles
        neighbors: list of the particle's neighbors
        x_vel: x velocity of the particle
        y_vel: y velocity of the particle
        x_force: x force applied to the particle
        y_force: y force applied to the particle
    """

    def __init__(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.previous_x_pos = x_pos
        self.previous_y_pos = y_pos
        self.visual_x_pos = x_pos
        self.visual_y_pos = y_pos
        self.rho = 0.0
        self.rho_near = 0.0
        self.press = 0.0
        self.press_near = 0.0
        self.neighbors = []
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.x_force = 0.0
        self.y_force = -G

    def update_state(self, dam: bool):
        """
        Updates the state of the particle
        """
        # Reset previous position
        (self.previous_x_pos, self.previous_y_pos) = (self.x_pos, self.y_pos)

        # Apply force using Newton's second law and Euler integration with mass = 1 and dt = 1
        (self.x_vel, self.y_vel) = (
            self.x_vel + self.x_force,
            self.y_vel + self.y_force,
        )

        # Move particle according to its velocity using Euler integration with dt = 1
        (self.x_pos, self.y_pos) = (self.x_pos + self.x_vel, self.y_pos + self.y_vel)

        # Set visual position. Visual position is the one shown on the screen
        # It is used to avoid unstable particles to be shown
        (self.visual_x_pos, self.visual_y_pos) = (self.x_pos, self.y_pos)

        # Reset force
        (self.x_force, self.y_force) = (0.0, -G)

        # Define velocity using Euler integration with dt = 1
        (self.x_vel, self.y_vel) = (
            self.x_pos - self.previous_x_pos,
            self.y_pos - self.previous_y_pos,
        )

        # Calculate velocity
        velocity = sqrt(self.x_vel**2 + self.y_vel**2)

        # Reduces the velocity if it is too high
        if velocity > MAX_VEL:
            self.x_vel *= VEL_DAMP
            self.y_vel *= VEL_DAMP

        # Circle boundary force         
        # Calculate the distance from the center of the circle
        dx = self.x_pos - SIM_CEN_X
        dy = self.y_pos - SIM_CEN_Y
        distance = sqrt(dx*dx + dy*dy)

        if distance > SIM_R:
            # Calculate the direction from the center to the particle
            direction = [dx / distance, dy / distance]

            # Position the particle on the perimeter of the circle
            self.visual_x_pos = SIM_CEN_X + direction[0] * SIM_R
            self.visual_y_pos = SIM_CEN_Y + direction[1] * SIM_R
            
            # Apply boundary force to particle
            bound_fact = WALL_DAMP * (distance - SIM_R)
            self.x_force -= direction[0] * bound_fact
            self.y_force -= direction[1] * bound_fact
        
        # Circle boundary damping
        #DAMP_DIST = 0.15
        #DAMP_K = 0.1
        #if (SIM_R - distance) < DAMP_DIST:
        #    damp_factor = 1 - ((SIM_R - distance) * DAMP_K)
        #    self.x_force *= damp_factor
        #    self.y_force *= damp_factor
            #damp_factor = (SIM_R - distance) / DAMP_DIST
            #self.x_force *= (1 - DAMP_K * damp_factor)
            #self.y_force *= (1 - DAMP_K * damp_factor)
        
        # Reset density
        self.rho = 0.0
        self.rho_near = 0.0

        # Reset neighbors
        self.neighbors = []

    def calculate_pressure(self):
        """
        Calculates the pressure of the particle
        """
        self.press = K * (self.rho - REST_DENSITY)
        self.press_near = K_NEAR * self.rho_near
