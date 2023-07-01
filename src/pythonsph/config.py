"""Configuration file defining the simulation parameters."""

# Simulation parameters
N = 250  # Number of particles

# The simulation space rectangle boundary
SIM_W = 0.7  # Simulation space width
BOTTOM = -SIM_W  # Simulation space ground

# The simulation space circle boundary
SIM_R = 0.5 
SIM_CEN_X = 0.0
SIM_CEN_Y = 0.0

# Fill
SIM_FILL_TOP = 0.1
SIM_FILL_SPACING = 0.03

# Dam
DAM = -0.3  # Position of the dam, simulation space is between -0.5 and 0.5
DAM_BREAK = 200  # Number of frames before the dam breaks

# Physics parameters
G = 0.02 * 0.25  # Acceleration of gravity
SPACING = 0.10  # Spacing between particles, used to calculate pressure
K = SPACING / 1000.0  # Pressure factor
K_NEAR = K * 10  # Near pressure factor, pressure when particles are close to each other
# Default density, will be compared to local density to calculate pressure
REST_DENSITY = 2.0
# Neighbour radius, if the distance between two particles is less than R, they are neighbours
R = SPACING * 1.5
SIGMA = 0.2  # Viscosity factor
MAX_VEL = 1.5  # Maximum velocity of particles, used to avoid instability
# Wall constraints factor, how much the particle is pushed away from the simulation walls
WALL_DAMP = 0.05
VEL_DAMP = 0.5  # Velocity reduction factor when particles are going above MAX_VEL


class Config:
    """Contains the simulation parameters and the physics parameters."""

    def __init__(self):
        return None

    def return_config(self):
        """Returns the simulation parameters and the physics parameters."""
        return (
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
        )
