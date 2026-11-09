import csv
import json
import time
from pathlib import Path

from main import load_data, build_relationships, validate_schedule
from pso import run_pso

BASE_SETTINGS = {
    "num_particles": 10,
    "num_iterations": 20,
    "w": 0.5,
    "c1": 1,
    "c2": 2
}

SEEDS = [42, 43, 44]

PARAMETER_TESTS = {
    "num_particles": [5, 10, 20],
    "num_iterations": [10, 20, 50],
    "w": [0.2, 0.5, 0.8],
    "c1": [0.5, 1, 2],
    "c2": [1, 2, 3]
}

def run_experiments():
    data = load_data("large")
    relationships = build_relationships(data)

    results = []
    tested_settings = set()

    for parameter, values in PARAMETER_TESTS.items():
        for value in values:
            settings = BASE_SETTINGS.copy()
            settings[parameter] = value

            setting_key = tuple(sorted(settings.items()))

            if setting_key in tested_settings:
                continue

            tested_settings.add(setting_key)

            for seed in SEEDS:
                start_time = time.perf_counter()

                # Run PSO with the current settings.
                best_solution, best_fitness, history = run_pso(
                    data,
                    relationships,
                    **settings,
                    seed=seed
                )

                runtime = time.perf_counter() - start_time

                hard_violations = len(
                    validate_schedule(best_solution, data, relationships)
                )

                result = settings.copy()
                result["seed"] = seed
                result["best_fitness"] = best_fitness
                result["runtime"] = runtime
                result["hard_violations"] = hard_violations

                result["history"] = json.dumps(history)
                result["best_schedule"] = json.dumps(best_solution)

                results.append(result)

    output_path = Path("results/pso_large_experiments.csv")

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    run_experiments()
