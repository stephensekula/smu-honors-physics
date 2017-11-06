import os 
import ctypes
import math



def simulate(time_duration, timestep_length, initial_conditions):
    number_steps = int(time_duration / timestep_length)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    simulation_engine_file = dir_path + '/simulation_engine.so'
    simulation_engine = ctypes.CDLL(simulation_engine_file)
    simulation_engine.get_error.restype = ctypes.c_double

    number_bodies = len(initial_conditions['position'])
    number_dimensions = len(initial_conditions['position'][0])

    mass_list = initial_conditions['mass']
    init_pos = initial_conditions['position']
    init_vel = initial_conditions['velocity']

    c_timestep_length = ctypes.c_double(timestep_length)
    masses = (ctypes.c_double * number_bodies)()
    c_init_pos  = (ctypes.c_double * number_dimensions * number_bodies)()
    c_init_vel = (ctypes.c_double * number_dimensions * number_bodies)()
    for body in range(0,number_bodies):
        masses[body] = mass_list[body]
        for comp in range(0,number_dimensions):
            c_init_pos[body][comp] = init_pos[body][comp]
            c_init_vel[body][comp] = init_vel[body][comp]

    body_array = ctypes.pointer(ctypes.pointer(ctypes.pointer(ctypes.c_double())))
    print("Running simulation engine...")
    simulation_engine.run(number_bodies,number_dimensions,number_steps,
                          c_timestep_length,masses, 
                          c_init_pos,c_init_vel,ctypes.byref(body_array))
    print("Engine finished, transferring data...")


    body_list = []
    for i in range(0,number_bodies):
        dimension_list = []
        for j in range(0,number_dimensions):
            step_list = []
            for k in range(0,number_steps):
                step_list.append(body_array[i][j][k])
            dimension_list.append(step_list)
        body_list.append(dimension_list)

    print("Data transfer complete, drawing image...")
    return body_list
