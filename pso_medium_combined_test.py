import csv
import json
import time
from pathlib import Path

from main import load_data, build_relationships, validate_schedule
from pso import run_pso

SETTINGS = {
    "num_particles": 20,
    "num_iterations": 20,
    "w": 0.8,
    "c1": 2,
    "c2": 1
}

SEEDS = [42, 43, 44]

def run_combined_test():
    data = load_data("medium")
    relationships = build_relationships(data)

    results = []

    for seed in SEEDS:
        start_time = time.perf_counter()

        best_solution, best_fitness, history = run_pso(
            data,
            relationships,
            **SETTINGS,
            seed=seed
        )

        runtime = time.perf_counter() - start_time

        hard_violations = len(
            validate_schedule(best_solution, data, relationships)
        )

        result = SETTINGS.copy()
        result["seed"] = seed
        result["best_fitness"] = best_fitness
        result["runtime"] = runtime
        result["hard_violations"] = hard_violations

        result["history"] = json.dumps(history)
        result["best_schedule"] = json.dumps(best_solution)

        results.append(result)

    output_path = Path("results/pso_medium_experiments.csv")

    with output_path.open("a", newline="", encoding="utf-8") as file:
        file.write("\n")
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writerows(results)

    print("Combined PSO Medium test completed.")
    print("Results saved to:", output_path)


if __name__ == "__main__":
    run_combined_test()