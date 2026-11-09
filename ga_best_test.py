from main import load_data, build_relationships
from ga import run_and_save_experiment
import csv
from pathlib import Path

best_settings = {
    "dataset": "small",
    "population_size": 40,
    "generations": 50,
    "k": 3,
    "crossover_rate": 0.6,
    "mutation_rate": 0.5
}

seeds = [42, 43, 44]

file_path = (
    Path(__file__).resolve().parent
    / "results"
    / "ga_small_experiments.csv"
)

with open(file_path, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([])


data = load_data(best_settings["dataset"])
relationships = build_relationships(data)

for seed in seeds:
    run_settings = best_settings.copy()
    run_settings["seed"] = seed

    print("Testing Best Settings - Seed:", seed)

    run_and_save_experiment(
        run_settings, data, relationships
    )