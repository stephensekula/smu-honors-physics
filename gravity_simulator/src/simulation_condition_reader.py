def read(conditions_file_name, render_parameters):

    conditions_file = open(conditions_file_name,'r')

    gravity_line = conditions_file.readline()
    distance_line = conditions_file.readline()
    period_line = conditions_file.readline()
    gravitational_constant = float( gravity_line.split('#')[0] )
    distance_scale_factor = float( distance_line.split('#')[0] )
    period_scale_factor = float( period_line.split('#')[0] )
    velocity_scale_factor = distance_scale_factor / period_scale_factor
    mass_scale_factor = gravitational_constant * ( distance_scale_factor**3 / period_scale_factor**2 )

    mass_list = [] 
    init_pos = []
    init_vel = []
    colors = []
    markers = []
    for line in conditions_file.readlines()[2:]:
        split_line = line.split(';')
        mass_string = split_line[0]
        position_strings = split_line[1].split()
        velocity_strings = split_line[2].split()
        color_string = split_line[3].strip()
        marker_string = split_line[4].strip()

        mass = float(mass_string) * mass_scale_factor
        mass_list.append(mass)
        colors.append(color_string)
        markers.append(marker_string)

        pos_x = float(position_strings[0]) * distance_scale_factor
        pos_y = float(position_strings[1]) * distance_scale_factor
        pos_z = float(position_strings[2]) * distance_scale_factor
                                                                   
        vel_x = float(velocity_strings[0]) * velocity_scale_factor
        vel_y = float(velocity_strings[1]) * velocity_scale_factor
        vel_z = float(velocity_strings[2]) * velocity_scale_factor

        init_pos.append([pos_x,pos_y,pos_z])
        init_vel.append([vel_x,vel_y,vel_z])

    initial_conditions = {'mass':mass_list,
                          'position':init_pos,
                          'velocity':init_vel}

    render_parameters['colors'] = colors
    render_parameters['markers'] = markers
    render_parameters['period_scale'] = period_scale_factor

    return initial_conditions
