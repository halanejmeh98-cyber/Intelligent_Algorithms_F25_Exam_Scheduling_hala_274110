import random

from main import (
    load_data,
    build_relationships,
    calculate_soft_penalties,
    validate_schedule
)

from ga import (
    create_population,
    tournament_selection,
    one_point_crossover,
    repair_child,
    swap_mutation
)

data = load_data("small")
relationships = build_relationships(data)

population = create_population(data, relationships, 10)

print("Population Size:", len(population))
print("Exams in first schedule:", len(population[0]))


for i, solution in enumerate(population, start=1):
    penalties = calculate_soft_penalties(solution, data, relationships)
    print(f"Schedule {i}: {penalties['weighted_total']}")


random.seed(42)
parent1 = tournament_selection(population, data, relationships, 2)
parent2 = tournament_selection(population, data, relationships, 2)
parent_penalties = calculate_soft_penalties(parent1, data, relationships)

print("Parent 1 Penalty:", parent_penalties["weighted_total"])
parent2_penalties = calculate_soft_penalties(parent2, data, relationships)
print("Parent 2 Penalty:", parent2_penalties["weighted_total"])


child, point = one_point_crossover(parent1, parent2)
print("Crossover Point:", point)
print("Child Exams:", len(child))

errors = validate_schedule(child, data, relationships)

if not errors:
    print("Child Schedule: Valid")
else:
    print("Child Schedule: Invalid")
    print("Hard Constraint Violations:", errors)


repaired_child = repair_child(child, parent1, data, relationships)

errors = validate_schedule(repaired_child, data, relationships)

print("After Repair:", "Valid" if not errors else "Invalid")

changes = sum(
    repaired_child[e] != parent1[e]
    for e in repaired_child
)

print("Changes Compared to Parent 1:", changes)

if not errors:
    penalty = calculate_soft_penalties(
        repaired_child, data, relationships
    )["weighted_total"]

    print("Repaired Child Penalty:", penalty)


mutated_child = swap_mutation(
    repaired_child, data, relationships
)

mutation_errors = validate_schedule(
    mutated_child, data, relationships
)

print("After Mutation:",
      "Valid" if not mutation_errors else "Invalid")

mutation_changes = sum(
    mutated_child[e] != repaired_child[e]
    for e in mutated_child
)

print("Mutation Changes:", mutation_changes)

if not mutation_errors:
    mutation_penalty = calculate_soft_penalties(
        mutated_child, data, relationships
    )["weighted_total"]

    print("Mutated Child Penalty:", mutation_penalty)