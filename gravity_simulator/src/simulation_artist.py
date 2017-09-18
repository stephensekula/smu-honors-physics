import colorsys
import matplotlib
import matplotlib.pyplot as Plotter
import matplotlib.animation as Animator
from mpl_toolkits.mplot3d import Axes3D


_trail_length_divisor = 50 #make this smaller to make the trail longer



def initialize_render(render_parameters, number_bodies, flat_mode):
    figure = Plotter.figure()
    axes = figure.add_subplot(1,1,1,projection='3d')
    figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

    if flat_mode:
        axes.view_init(90,0)
        zmin=-1
        zmax=1

    render_parameters['axes'] = axes
    render_parameters['figure'] = figure



def set_axes_parameters(render_parameters):
    axes = render_parameters['axes']
    axes.w_xaxis.set_pane_color((0,0,0,0))
    axes.w_yaxis.set_pane_color((0,0,0,0))
    axes.w_zaxis.set_pane_color((0,0,0,0))
    axes.patch.set_facecolor('black')
    axes.set_xlim3d(render_parameters['x'][0],render_parameters['x'][1])
    axes.set_ylim3d(render_parameters['y'][0],render_parameters['y'][1])
    axes.set_zlim3d(render_parameters['z'][0],render_parameters['z'][1])



def render_image(render_parameters, position_list):
    set_axes_parameters(render_parameters)
    for i,body in enumerate(position_list):
        x = body[0]
        y = body[1]
        z = body[2]
        color = render_parameters['colors'][i]
        marker = render_parameters['markers'][i]
        Plotter.plot(x,y,z,color=color,marker=marker)
    Plotter.savefig('image.png', bbox_inches='tight')



def initialize_animation(position_list, render_parameters):
    Plotter.cla()
    color = render_parameters['colors']
    marker = render_parameters['markers']
    axes = render_parameters['axes']
    set_axes_parameters(render_parameters)
    lines = []
    for i,body in enumerate(position_list):
        line = axes.plot(body[0][0:1], 
                         body[1][0:1],
                         body[2][0:1],
                         color=color[i],
                         marker=marker[i])[0]
        lines.append(line)
    return lines



def animate(visible_step, position_list, time_duration, number_visible_steps, render_parameters, lines):
    number_steps = len(position_list[0][0])
    animation_trail_length = int(number_steps / _trail_length_divisor)

    end = int(visible_step * number_steps / number_visible_steps)
    start = end - 1
    if render_parameters['render trails']:
        start = end - animation_trail_length
    if start < 0:
        start = 0

    for i,body in enumerate(position_list):
        x = body[0][start:end]
        y = body[1][start:end]
        z = body[2][start:end]
        lines[i].set_data(x,y)
        lines[i].set_3d_properties(z)



def render_animation(time_duration,position_list,render_parameters):
    number_visible_steps = int(time_duration*10) #ten frames per second
    figure = render_parameters['figure']
    lines = initialize_animation(position_list,render_parameters)
    animation = Animator.FuncAnimation(figure,animate,
                    number_visible_steps,interval=100,blit=False,
                    fargs=(position_list,
                           time_duration,
                           number_visible_steps,
                           render_parameters,
                           lines)
                    )
    animation.save('animation.mp4')



def visualize_simulation(time_duration, position_list, render_parameters):
    animate_mode = render_parameters['animate mode']
    flat_mode = render_parameters['flat mode']
    number_bodies = len(position_list)
    initialize_render(render_parameters,number_bodies,flat_mode)
    render_image(render_parameters,position_list)
    if animate_mode:
        print('Image drawn, rendering animation...')
        render_animation(time_duration,position_list,render_parameters)
        print('Animation rendered, program complete.')
    else:
        print('Image drawn, program complete.')
