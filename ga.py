from main import create_random_solution, load_data, build_relationships
from main import calculate_soft_penalties
import random
from main import validate_schedule

import csv
import json
import time
from pathlib import Path

def create_population(data, relationships, population_size, base_seed=42):
    population = []

    for i in range(population_size):
        solution = create_random_solution(
            data, relationships, seed=base_seed + i
        )
        population.append(solution)

    return population

def tournament_selection(population, data, relationships, k):
    candidates = random.sample(population, k)

    best_parent = min(
        candidates,
        key=lambda schedule: calculate_soft_penalties(
            schedule, data, relationships
        )["weighted_total"]
    )

    return best_parent

def one_point_crossover(parent1, parent2):
    exam_ids = sorted(parent1.keys())
    point = random.randint(1, len(exam_ids) - 1)

    child = {}

    for i, exam_id in enumerate(exam_ids):
        if i < point:
            child[exam_id] = parent1[exam_id]
        else:
            child[exam_id] = parent2[exam_id]

    return child, point

def repair_child(child, parent1, data, relationships):
    repaired = parent1.copy()

    for exam_id in sorted(child.keys()):
        old_assignment = repaired[exam_id]

        repaired[exam_id] = child[exam_id]

        errors = validate_schedule(repaired, data, relationships)

        if errors:
            repaired[exam_id] = old_assignment

    return repaired


def swap_mutation(schedule, data, relationships):
    mutated = schedule.copy()
    exam_ids = list(mutated.keys())

    random.shuffle(exam_ids)

    for i in range(0, len(exam_ids) - 1, 2):
        exam1 = exam_ids[i]
        exam2 = exam_ids[i + 1]

        mutated[exam1], mutated[exam2] = (
            mutated[exam2], mutated[exam1]
        )

        errors = validate_schedule(mutated, data, relationships)

        if not errors:
            return mutated

        mutated[exam1], mutated[exam2] = (
            mutated[exam2], mutated[exam1]
        )

    return mutated

def run_ga(data, relationships, population_size, generations,
           k, crossover_rate, mutation_rate, seed):

    random.seed(seed)

    population = create_population(
        data, relationships, population_size, base_seed=seed
    )

    def fitness(schedule):
        return calculate_soft_penalties(
            schedule, data, relationships
        )["weighted_total"]

    best_schedule = min(population, key=fitness).copy()
    best_score = fitness(best_schedule)

    history = [best_score]

    for generation in range(generations):
        new_population = []

        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population, data, relationships, k
            )
            parent2 = tournament_selection(
                population, data, relationships, k
            )

            if random.random() < crossover_rate:
                child, point = one_point_crossover(parent1, parent2)
                child = repair_child(
                    child, parent1, data, relationships
                )
            else:
                child = parent1.copy()

            if random.random() < mutation_rate:
                child = swap_mutation(
                    child, data, relationships
                )

            errors = validate_schedule(
                child, data, relationships
            )

            if errors:
                raise ValueError(errors)

            new_population.append(child)

        population = new_population

        generation_best = min(population, key=fitness)
        generation_score = fitness(generation_best)

        if generation_score < best_score:
            best_score = generation_score
            best_schedule = generation_best.copy()

        history.append(best_score)

        print(f"Generation {generation + 1}: Best = {best_score}")

    return best_schedule, best_score, history

def save_experiment(result):
    file_path = (
        Path(__file__).resolve().parent
        / "results"
        / "ga_small_experiments.csv"
    )

    is_new_file = (
        not file_path.exists()
        or file_path.stat().st_size == 0
    )

    columns = [
        "dataset", "seed",
        "population_size", "generations", "k",
        "crossover_rate", "mutation_rate",
        "initial_best", "final_best",
        "runtime_seconds", "hard_violations",
        "P1", "P2", "P3", "P4",
        "selection_method", "crossover_method",
        "repair_method", "mutation_method",
        "elitism", "fitness_weights",
        "history", "best_schedule"
    ]

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        if is_new_file:
            writer.writeheader()

        writer.writerow(result)

    print("Experiment saved successfully.")

settings = {
    "dataset": "small",
    "population_size": 10,
    "generations": 3,
    "k": 2,
    "crossover_rate": 1.0,
    "mutation_rate": 1.0,
    "seed": 42
}

test_values = {
    "population_size": [10, 20, 40],
    "k": [2, 3],
    "generations": [10, 30, 50],
    "crossover_rate": [0.6, 0.8, 1.0],
    "mutation_rate": [0.1, 0.3, 0.5],
    "seeds": [42, 43, 44]
}

def prepare_experiments(settings, test_values, parameter):
    experiments = []

    for value in test_values[parameter]:
        experiment = settings.copy()
        experiment[parameter] = value
        experiments.append(experiment)

    return experiments


def add_seeds(experiments, seeds):
    runs = []

    for experiment in experiments:
        for seed in seeds:
            run = experiment.copy()
            run["seed"] = seed
            runs.append(run)

    return runs


def run_one_experiment(run_settings, data, relationships):

    start_time = time.perf_counter()

    best_schedule, best_score, history = run_ga(
        data,
        relationships,
        population_size=run_settings["population_size"],
        generations=run_settings["generations"],
        k=run_settings["k"],
        crossover_rate=run_settings["crossover_rate"],
        mutation_rate=run_settings["mutation_rate"],
        seed=run_settings["seed"]
    )

    execution_time = time.perf_counter() - start_time

    return best_schedule, best_score, history, execution_time


def run_and_save_experiment(run_settings, data, relationships):

    best_schedule, best_score, history, execution_time = (
        run_one_experiment(run_settings, data, relationships)
    )

    penalties = calculate_soft_penalties(
        best_schedule, data, relationships
    )

    errors = validate_schedule(
        best_schedule, data, relationships
    )

    if errors:
        raise ValueError(errors)

    result = {
        **run_settings,
        "selection_method": "Tournament",
        "crossover_method": "One-Point",
        "repair_method": "Parent-Based Repair",
        "mutation_method": "Swap",
        "elitism": False,
        "fitness_weights": "3,1,1,4",
        "initial_best": history[0],
        "final_best": best_score,
        "P1": penalties["P1"],
        "P2": penalties["P2"],
        "P3": penalties["P3"],
        "P4": penalties["P4"],
        "runtime_seconds": round(execution_time, 6),
        "hard_violations": len(errors),
        "history": json.dumps(history),
        "best_schedule": json.dumps(best_schedule)
    }

    save_experiment(result)


if __name__ == "__main__":

    data = load_data(settings["dataset"])
    relationships = build_relationships(data)

    parameters = [
        "population_size",
        "k",
        "generations",
        "crossover_rate",
        "mutation_rate"
    ]

    all_runs = []

    for parameter in parameters:
        experiments = prepare_experiments(
            settings, test_values, parameter
        )

        runs = add_seeds(
            experiments, test_values["seeds"]
        )

        all_runs.extend(runs)

    unique_runs = []
    seen = set()

    for run in all_runs:
        key = tuple(run.items())

        if key not in seen:
            seen.add(key)
            unique_runs.append(run)

    print("Total Experiments:", len(unique_runs))

    for run_settings in unique_runs:
        print(run_settings)

        run_and_save_experiment(
           run_settings, data, relationships
        )