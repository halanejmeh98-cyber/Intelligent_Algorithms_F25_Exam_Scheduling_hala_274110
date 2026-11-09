import csv
import time
from main import load_data, build_relationships, validate_schedule
from aco import run_aco


BASE_SETTINGS = {
    "num_ants": 5,
    "num_iterations": 10,
    "alpha": 1,
    "beta": 2,
    "evaporation_rate": 0.2,
    "q": 2
}

SEEDS = [42, 43, 44]

PARAMETER_TESTS = [
    ("num_ants", [5, 10, 20]),
    ("num_iterations", [10, 30, 50]),
    ("alpha", [0.5, 1, 2]),
    ("beta", [1, 2, 3]),
    ("evaporation_rate", [0.1, 0.2, 0.4]),
    ("q", [1, 2, 5])
]

def prepare_experiments():
    experiments = []

    for parameter, values in PARAMETER_TESTS:
        for value in values:
            settings = BASE_SETTINGS.copy()
            settings[parameter] = value

            if settings not in experiments:
                experiments.append(settings)

    return experiments


def run_one_experiment(data, relationships, settings, seed):

    start_time = time.perf_counter()

    best_solution, best_fitness, history = run_aco(
        data,
        relationships,
        num_ants=settings["num_ants"],
        num_iterations=settings["num_iterations"],
        alpha=settings["alpha"],
        beta=settings["beta"],
        evaporation_rate=settings["evaporation_rate"],
        q=settings["q"],
        seed=seed
    )

    execution_time = time.perf_counter() - start_time
    if best_solution is None:
        hard_violations = None
    else:
        hard_violations = len(
            validate_schedule(best_solution, data, relationships)
        )


    result = settings.copy()

    result["seed"] = seed
    result["best_fitness"] = best_fitness
    result["execution_time"] = execution_time
    result["hard_violations"] = hard_violations
    result["history"] = history

    return result

def save_results(results):

    with open("results/aco_medium_experiments.csv", "w", 
              newline="", encoding="utf-8-sig") as file:

        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results[:-3])
        writer.writerow({})
        writer.writerows(results[-3:])

if __name__ == "__main__": 

    data = load_data("medium")
    relationships = build_relationships(data)

    experiments = prepare_experiments()
    experiments.append({
        "num_ants": 20,
        "num_iterations": 10,
        "alpha": 1,
        "beta": 3,
        "evaporation_rate": 0.2,
        "q": 2
    })
    results = []

    for settings in experiments:
        for seed in SEEDS:
            result = run_one_experiment(
                data,
                relationships,
                settings,
                seed
            )

            results.append(result)

    save_results(results)

    print("Completed experiments:", len(results))
    print("ACO Medium experiments saved.")



