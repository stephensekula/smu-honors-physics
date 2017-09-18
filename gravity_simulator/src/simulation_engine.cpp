#include <iostream>
#include <cmath>

#include <stdio.h>

using namespace std;

int _num_bodies;
int _num_dimensions;
int _num_steps;

double* _energy_errors = new double[_num_steps];


struct body {
    double mass;
    //The position and velocity are arrayed as:
    //p[0] = {x1,x2,x3,...,xn}
    //p[1] = {y1,y2,y3,...,yn}
    double** position; 
    double** velocity;

    body (double m, double** p, double** v):
            mass(m), position(p), velocity(v) {}
};

body** _final_bodies;


double calculate_velocity (double initial_velocity, double acceleration, double time) {
    double velocity = acceleration * time + initial_velocity;
    return velocity;
}


double calculate_position (double initial_position, double initial_velocity, double acceleration, double time) {
    double quadratic_component = acceleration * pow(time,2) / 2;
    double linear_component = initial_velocity * time;
    double position = initial_position + linear_component + quadratic_component;
    return position;
}


void calculate_acceleration(body** bodies, int body_index, int timestep, double acceleration[]) {
    for(int i = 0; i < _num_bodies; i++) {
        if (i == body_index) continue;

        double mass_i = bodies[i]->mass;

        double square_distance = 0.0;
        for (int j = 0; j < _num_dimensions; j++) {
            double position1 = bodies[body_index]->position[j][timestep-1];
            double position2 = bodies[i]->position[j][timestep-1];
            double square_distance_in_j = pow(position2-position1, 2.0);
            square_distance += square_distance_in_j;
        }
        double magnitude_of_distance_cubed = pow(square_distance,1.5); // |r1-r2|^3

        for(int j = 0; j < _num_dimensions; j++) {
            double position1 = bodies[body_index]->position[j][timestep-1];
            double position2 = bodies[i]->position[j][timestep-1];
            double vector_distance_from_i = position2 - position1; //the order of subtraction here is CRITICAL

            double acceleration_from_i_in_dimension_j = mass_i * vector_distance_from_i / magnitude_of_distance_cubed;
            acceleration[j] += acceleration_from_i_in_dimension_j;
        }
    }
}


void time_loop (body** bodies, double timestep_length, int _num_steps) {
    for(int timestep = 1; timestep < _num_steps; timestep++) {
        for(int i = 0; i < _num_bodies; i++) {
            double acceleration[_num_dimensions];
            for(int k = 0; k < _num_dimensions; k++) {acceleration[k] = 0.0;}
            calculate_acceleration(bodies,i,timestep,acceleration);
            for(int j = 0; j < _num_dimensions; j++) {
                double vel = calculate_velocity(
                    bodies[i]->velocity[j][timestep-1],
                    acceleration[j],
                    timestep_length);

                bodies[i]->velocity[j][timestep] = vel;

                bodies[i]->position[j][timestep] = calculate_position(
                    bodies[i]->position[j][timestep-1],
                    bodies[i]->velocity[j][timestep-1],
                    acceleration[j],
                    timestep_length);
            }
        }
    }
}


void calculate_paths(double timestep_length, double masses[], double init_pos[], double init_vel[], double***& body_array) {
    body** bodies = new body*[_num_bodies];
    for(int i = 0; i < _num_bodies; i++) {
        double** positions = new double*[_num_dimensions];
        double** velocities = new double*[_num_dimensions];
        for(int j = 0; j < _num_dimensions; j++) {
            positions[j] = new double[_num_steps];
            velocities[j] = new double[_num_steps];
            
            positions[j][0] = init_pos[i*_num_dimensions + j];
            velocities[j][0] = init_vel[i*_num_dimensions + j];
        }
        body* new_body = new body(masses[i],positions,velocities);
        bodies[i] = new_body;
    }

    time_loop(bodies,timestep_length,_num_steps);
    body_array = new double**[_num_bodies];
    for(int i = 0; i < _num_bodies; i++) {
        body_array[i] = bodies[i]->position;
    }

    _final_bodies = bodies;
}


double calculate_potential(int timestep) {
    double total_potential = 0.0;
    for(int body_i = 0; body_i < _num_bodies-1; body_i++) {
        double mass_of_i = _final_bodies[body_i]->mass;
        for(int body_j = body_i+1; body_j < _num_bodies; body_j++) {
            double mass_of_j = _final_bodies[body_j]->mass;
            double square_distance = 0.0;
            for (int component = 0; component < _num_dimensions; component++) {
                double position1 = _final_bodies[body_i]->position[component][timestep];
                double position2 = _final_bodies[body_j]->position[component][timestep];
                double square_distance_in_component = pow(position2-position1, 2.0);
                square_distance += square_distance_in_component;
            }
            double magnitude_of_distance = pow(square_distance,0.5); // |r1-r2|
            double mass_product = mass_of_i * mass_of_j;
            double potential_between_i_and_j = mass_product / magnitude_of_distance;
        }
        total_potential += total_potential;
    }
    return total_potential;
}


double calculate_kinetic(int timestep) {
    double kinetic_energy = 0.0;
    for(int body_i = 0; body_i < _num_bodies; body_i++) {
        double velocity_squared = 0.0;
        for(int component = 0; component < _num_dimensions; component++) {
            double velocity = _final_bodies[body_i]->velocity[component][timestep];
            velocity_squared += velocity*velocity;
        }
        double mass_of_i = _final_bodies[body_i]->mass;
        kinetic_energy += mass_of_i* velocity_squared;
    }
    return kinetic_energy;
}


double calculate_energy(int timestep) {
    double potential_energy = calculate_potential(timestep);
    double kinetic_energy = calculate_kinetic(timestep);
    return (potential_energy + kinetic_energy);
}


void calculate_energy_difference() {
    _energy_errors = new double[_num_steps];

    double initial_energy = calculate_energy(0);
    for(int t = 0; t < _num_steps; t++) {
        double energy = calculate_energy(t);
        double energy_difference = initial_energy - energy;
        double relative_error = energy_difference / initial_energy;
        _energy_errors[t] = relative_error;
    }
}


extern "C" {
    void run(int N_bodies, int N_dim, int N_steps, double timestep_length, double masses[], double init_pos[], double init_vel[], double***& body_array) {
        _num_bodies = N_bodies;
        _num_dimensions = N_dim;
        _num_steps = N_steps;

        calculate_paths(timestep_length, masses, init_pos, init_vel, body_array);
        calculate_energy_difference();
    }

    double get_error(int timestep) {
        double error = _energy_errors[timestep];
        return error;
    }
}
