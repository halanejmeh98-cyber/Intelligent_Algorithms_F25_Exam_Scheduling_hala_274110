import random

from main import (
    create_random_solution,calculate_soft_penalties,validate_schedule)

def initialize_swarm(data, relationships, num_particles, seed=42):
    swarm = []

    for i in range(num_particles):
        position = create_random_solution(
            data,
            relationships,
            seed=seed + i
        )
        velocity = []
        
        pbest = position.copy()

        penalties = calculate_soft_penalties(
            position,
            data,
            relationships
        )

        pbest_fitness = penalties["weighted_total"]

        particle = {
            "position": position,
            "velocity": velocity,
            "pbest": pbest,
            "pbest_fitness": pbest_fitness
        }

        swarm.append(particle)
    return swarm

def initialize_gbest(swarm):
    best_particle = min(
        swarm,
        key=lambda particle: particle["pbest_fitness"]
    )
    gbest = best_particle["pbest"].copy()
    gbest_fitness = best_particle["pbest_fitness"]

    return gbest, gbest_fitness


def update_velocity(particle, gbest, w, c1, c2, rng):
    position = particle["position"]
    new_velocity = []

    for move in particle["velocity"]:
        if rng.random() < w:
            new_velocity.append(move)

    pbest = particle["pbest"]
    for exam_id in position:
        if position[exam_id] != pbest[exam_id]:
            if rng.random() < c1 / (1 + c1):
                new_velocity.append((exam_id, pbest[exam_id]))

    for exam_id in position:
        if position[exam_id] != gbest[exam_id]:
            if rng.random() < c2 / (1 + c2):
                new_velocity.append((exam_id, gbest[exam_id]))

                 
    return new_velocity

def update_position(position, velocity, data, relationships):
    new_position = position.copy()

    for exam_id, assignment in velocity:
        old_assignment = new_position[exam_id]
        new_position[exam_id] = assignment

        if validate_schedule(new_position, data, relationships):
            new_position[exam_id] = old_assignment

            other_exam = None
            for candidate_id, candidate_assignment in new_position.items():
                if candidate_id != exam_id and candidate_assignment == assignment:
                    other_exam = candidate_id
                    break

            if other_exam is not None:
                new_position[exam_id] = assignment
                new_position[other_exam] = old_assignment


                if validate_schedule(new_position, data, relationships):
                    new_position[exam_id] = old_assignment
                    new_position[other_exam] = assignment

    return new_position

def update_pbest(particle, data, relationships):
    fitness = calculate_soft_penalties(
        particle["position"],
        data,
        relationships
    )["weighted_total"]

    if fitness < particle["pbest_fitness"]:
        particle["pbest"] = particle["position"].copy()
        particle["pbest_fitness"] = fitness


def run_pso(data, relationships, num_particles, num_iterations,
            w, c1, c2, seed=42):

    rng = random.Random(seed)

    swarm = initialize_swarm(
        data, relationships, num_particles, seed
    )

    gbest, gbest_fitness = initialize_gbest(swarm)
    history = [gbest_fitness]

    for iteration in range(num_iterations):

        for particle in swarm:
            new_velocity = update_velocity(
                particle, gbest, w, c1, c2, rng
            )

            particle["velocity"] = new_velocity

            particle["position"] = update_position(
                particle["position"],
                particle["velocity"],
                data,
                relationships
            )

            update_pbest(particle, data, relationships)
        gbest, gbest_fitness = initialize_gbest(swarm)
        history.append(gbest_fitness)

    return gbest, gbest_fitness, history