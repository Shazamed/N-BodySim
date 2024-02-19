import numpy as np

def system_param(height, width):
    collision = False
    dt = 0.4
    body_number = 3
    body_position = np.zeros([body_number, 2]).astype('float64')
    body_velocity = np.zeros([body_number, 2]).astype('float64')
    body_forces = np.zeros([body_number, 2]).astype('float64')
    body_mass = np.full([body_number, 1], 200).astype('float64')
    body_colour = np.full([body_number, 3], 0).astype('float64')
    body_radii = np.full([body_number, 1], 10).astype('float64')

    body_position[0] = np.array([(width/2 - 97 * 2, height/2 + 24 * 2)])
    body_position[1] = np.array([(width/2 + 97 * 2, height/2 - 24 * 2)])
    body_position[2] = np.array([(width/2, height/2)])

    body_velocity[0] = np.array([(0.466203685, 0.43236573)])
    body_velocity[1] = np.array([(0.466203685, 0.43236573)])
    body_velocity[2] = np.array([(-0.93240737, -0.86473146)])

    return body_position, body_velocity, body_forces, body_mass, body_colour, body_radii, collision, dt