from main import load_data, build_relationships

import csv
import json
from pathlib import Path


from ga import (
    prepare_experiments,
    add_seeds,
    run_one_experiment,
    calculate_soft_penalties,
    validate_schedule,
    settings,
    test_values
)

data = load_data("medium")
relationships = build_relationships(data)

print("Dataset: Medium")
print("Exams:", len(data["exams"]))
print("Students:", len(data["students"]))
print("Rooms:", len(data["rooms"]))
print("Timeslots:", len(data["timeslots"]))


medium_settings = settings.copy()
medium_settings["dataset"] = "medium"

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
        medium_settings, test_values, parameter
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


print("Total Medium Experiments:", len(unique_runs))
results_file = (
    Path(__file__).resolve().parent
    / "results"
    / "ga_medium_experiments.csv"
)

def save_medium_experiment(result):

    is_new_file = (
        not results_file.exists()
        or results_file.stat().st_size == 0
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

    with open(results_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        if is_new_file:
            writer.writeheader()

        writer.writerow(result)

    print("Medium experiment saved successfully.")

def run_and_save_medium_experiment(run_settings):

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

    save_medium_experiment(result)

if __name__ == "__main__":
    for i, run_settings in enumerate(unique_runs, start=1):

        print(f"\nMedium Experiment {i}/{len(unique_runs)}")
        print("Settings:", run_settings)

        run_and_save_medium_experiment(run_settings)

    print("\nAll Medium experiments completed.")