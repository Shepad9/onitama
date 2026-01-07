#---------particle_swarm.py--------

import numpy as np
import math

import game_file
import player_file
import gui_file

MAX_MOVES_FOR_RANDOM = 21 # maximmum some games will be shorter
MIN_MOVES_FOR_RANDOM = 17
TEST_ACCURACY = 400 #not guaranteed as some positions die in generation
MAD_WEIGHT = 0.1 # should be noticeable


def get_dynamic(state):
    com_b = player_file.computer(True, depth = 5, weights = {"total pieces": (0.580, 0.550), "piece progression": (0.520, 0.500), "master to temple": (0.300, 0.400), "defended pieces": (0.480, 0.450), "piece spread": (-0.180, -0.150)})
    com_r = player_file.computer(False, depth = 5, weights = {"total pieces": (0.580, 0.550), "piece progression": (0.520, 0.500), "master to temple": (0.300, 0.400), "defended pieces": (0.480, 0.450), "piece spread": (-0.180, -0.150)})
    if state.is_b_turn:
        dyna = com_b.maximiser(state)["score"]
    else:
        dyna = com_r.minimiser(state)["score"]
    return dyna


def get_states(): # add the optimal dynamic search value
    game_states = []
    dynas = []

    for attempt in range(TEST_ACCURACY):
        g = game_file.game.create_random_game(player_file.full_random(True), player_file.full_random(False))
        for i in range (np.random.binomial(MAX_MOVES_FOR_RANDOM-MIN_MOVES_FOR_RANDOM, 0.5)+MIN_MOVES_FOR_RANDOM):

            move = g._game__get_active_player().get_move(g.current_game_state)
            g.move_stack.append(move)   
            g.current_game_state.progress_game_state(move) # get move
        if g.current_game_state.is_game_live:
            dyna = get_dynamic(g.current_game_state)
            if (dyna > -700 and
                dyna < 700 and 
                len(g.current_game_state.player_b_pieces) + 
                len(g.current_game_state.player_r_pieces) <= 7): #ensure first/second weightings
                dynas.append(dyna)
                game_states.append(g.current_game_state)
                gui_file.game_display(g.current_game_state)
            
    return game_states, dynas
    # take 15 positions from a file


STATES, DYNAS = get_states()
print(len(DYNAS))
print(np.mean(DYNAS))
print(np.mean([abs(dyna) for dyna in DYNAS]))


def particle_to_weights(p): # remember total pieces has been doubled for the weighting also I have reduced the computation to 5 dimensions vy ignoring weighting after endgame
    return {"total pieces": (p[0], p[0]), "piece progression": (p[1], p[1]), "master to temple": (p[2], p[2]), "defended pieces": (p[3], p[3]), "piece spread": (p[4],p[4])}


def src_benchmark(particle):
    
    weights = particle_to_weights(particle)
    com_b = player_file.computer(True, weights = weights)
    com_r = player_file.computer(False, weights = weights)
    
    vectorized_src = np.vectorize(get_src, otypes=[float])

    scores = vectorized_src(STATES, DYNAS, com_b, com_r)

    mean = np.mean(scores)
    mad = np.mean(np.abs(scores - mean))
    return mean + mad * MAD_WEIGHT


def get_src(g1, dyna, com_b, com_r):
    
    if g1.is_b_turn:
        stat = com_b.quiescence_max(g1)
    else:
        stat = com_r.quiescence_min(g1)
    return  abs (dyna - stat)


def show_diversity(positions):
    centroid = np.mean(positions, axis=0) # how alligned are the particles to the mean
    centroid /= np.linalg.norm(centroid) + SMALL_NUM

    diversity = np.mean([
        1 - np.dot(x, centroid) for x in positions
    ])
    print("diversity is")
    print(diversity)


DIMENSIONS = 5 # because 10 different weights
NUM_PARTICLES = 35 # may be too high
ITERATIONS = 200 # very high for now
SMALL_NUM = 1e-9 # to prevent divide by zero error

V_max = 0.2
W_max = 0.95
W_min = 0.8     # inertia decreases linearly
C1 = 0.9   # personal
C2 = 0.9    # social both kept low because function is probably noisy

W_over_time = np.linspace(W_max, W_min, ITERATIONS)

print("begining initialisation")
positions = np.random.randn(NUM_PARTICLES, DIMENSIONS)# everything stored by 1 row per particle
positions[0] = [0.580, 0.520, 0.300, 0.480, -0.180]
# known solution
velocities = np.random.randn(NUM_PARTICLES, DIMENSIONS)*0.1 #keep velocities smaller to prevent them from jumping across hypershere
positions /= np.linalg.norm(positions, axis=1, keepdims=True) + SMALL_NUM

personal_best_positions = positions.copy()
personal_best_scores = np.array([src_benchmark(p) for p in positions])

global_best_index = np.argmin(personal_best_scores)
global_best_position = personal_best_positions[global_best_index].copy()
global_best_score = personal_best_scores[global_best_index] 

# optimize
for iteration, W in enumerate(W_over_time):
    for i in range(NUM_PARTICLES):
        r1 = np.random.rand(DIMENSIONS) #and randomness
        r2 = np.random.rand(DIMENSIONS)

        velocities[i] = (
            W * velocities[i]
            + C1 * r1 * (personal_best_positions[i] - positions[i])
            + C2 * r2 * (global_best_position - positions[i]) # update velocities
        )

        v = velocities[i]
        x = positions[i]
        velocities[i] = v - np.dot(v, x) * x # make velocities tangental

        v_norm = np.linalg.norm(velocities[i])
        if v_norm > V_max:
            velocities[i] *= V_max / v_norm # keeps velocities under V max


        positions[i] += velocities[i]
        
        norm = np.linalg.norm(positions[i])
        if norm > SMALL_NUM: #should be impossible but a crash would be very annoying
            positions[i] /= norm

        score = src_benchmark(positions[i])

        if score < personal_best_scores[i]: #if PB update
            personal_best_scores[i] = score
            personal_best_positions[i] = positions[i].copy()

            if score < global_best_score: #if WR update
                global_best_score = score
                global_best_position = positions[i].copy()

    if iteration % 10 == 0: #give scenario every 10 incase crash
        print(f"iteration: {iteration}   best score: {global_best_score}")
        print(global_best_position)
        show_diversity(positions)

# show solution
print("Best solution found:")
print(global_best_position)
print("Best score:", global_best_score)
show_diversity(positions)




