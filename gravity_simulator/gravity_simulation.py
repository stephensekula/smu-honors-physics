import sys
from src import simulation_condition_reader
from src import simulation_interface
from src import simulation_artist

time_duration = 10 #seconds
timestep_length = .001 #reccomended = 0.001; 0.0001 is ideal but slow

render_parameters = {'x':[-10,10],         #x borders of the final image
                     'y':[-10,10],         #y borders of the final image
                     'z':[-10,10],         #z borders of the final image
                     'flat mode':True,    #generate the image/video looking straight down onto the xy plane
                     'animate mode':True,  #generate an mp4 video of the simulation, instead of only a picture
                     'render trails':True} #gives all moving objects a trail

initial_condition_file = sys.argv[1]
initial_conditions = simulation_condition_reader.read(initial_condition_file,render_parameters)
position_list = simulation_interface.simulate(time_duration,timestep_length,initial_conditions)
simulation_artist.visualize_simulation(time_duration,position_list,render_parameters)
