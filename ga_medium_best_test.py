from main import (
    load_data,
    build_relationships,
    calculate_soft_penalties,
    validate_schedule
)

from ga import run_one_experiment

import csv
import json
from pathlib import Path

best_settings = {
    "dataset": "medium",
    "population_size": 20,
    "generations": 50,
    "k": 2,
    "crossover_rate": 1.0,
    "mutation_rate": 1.0
}

seeds = [42, 43, 44]

results_file = (
    Path(__file__).resolve().parent
    / "results"
    / "ga_medium_experiments.csv"
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


# Save a final Medium experiment.
def save_final_experiment(result, add_separator=False):

    if not results_file.exists():
        raise FileNotFoundError("Medium experiments CSV not found.")

    with open(results_file, "a", newline="", encoding="utf-8") as file:

        if add_separator:
            csv.writer(file).writerow([])

        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow(result)

    print("Final Medium experiment saved successfully.")

data = load_data(best_settings["dataset"])
relationships = build_relationships(data)

for i, seed in enumerate(seeds):

    run_settings = best_settings.copy()
    run_settings["seed"] = seed

    print("\nTesting Combined Medium Settings - Seed:", seed)

    best_schedule, best_score, history, execution_time = (
        run_one_experiment(run_settings, data, relationships)
    )

    errors = validate_schedule(
        best_schedule, data, relationships
    )

    if errors:
        raise ValueError(errors)

    penalties = calculate_soft_penalties(
        best_schedule, data, relationships
    )

    result = {
        **run_settings,
        "initial_best": history[0],
        "final_best": best_score,
        "runtime_seconds": round(execution_time, 6),
        "hard_violations": len(errors),
        "P1": penalties["P1"],
        "P2": penalties["P2"],
        "P3": penalties["P3"],
        "P4": penalties["P4"],
        "selection_method": "Tournament",
        "crossover_method": "One-Point",
        "repair_method": "Parent-Based Repair",
        "mutation_method": "Swap",
        "elitism": False,
        "fitness_weights": "3,1,1,4",
        "history": json.dumps(history),
        "best_schedule": json.dumps(best_schedule)
    }

    save_final_experiment(
        result,
        add_separator=(i == 0)
    )


print("\nAll final Medium experiments completed.")