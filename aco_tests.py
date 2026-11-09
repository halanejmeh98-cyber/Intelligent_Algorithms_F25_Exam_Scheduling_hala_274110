from aco import calculate_heuristic, get_feasible_assignments,initialize_pheromones,select_next_assignment
from aco import construct_ant_solution,evaporate_pheromones, update_pheromones,run_aco
from main import load_data, build_relationships, validate_schedule,calculate_soft_penalties
import random

if __name__ == "__main__":
    
    relationships = {
        "exam_students": {
            "E1": {"S1", "S2"},
            "E2": {"S1"}
        },
        "timeslot_info": {
            "T1": {"day": 1, "period_index": 1},
            "T2": {"day": 1, "period_index": 2},
            "T3": {"day": 2, "period_index": 1}
        }
    }

    partial_schedule = {
        "E1": ("T1", "R1")
    }

    result = calculate_heuristic(
        "E2",
        "T2",
        partial_schedule,
        relationships
    )

    print("Heuristic:", result)

    assert abs(result - 1/7) < 1e-9

    print("Heuristic test passed.")


    result2 = calculate_heuristic(
        "E2",
        "T3",
        partial_schedule,
        relationships
    )

    print("Second heuristic:", result2)

    assert abs(result2 - 0.2) < 1e-9

    print("Second heuristic test passed.")


    result3 = calculate_heuristic(
        "E2",
        "T1",
        partial_schedule,
        relationships
    )

    print("Conflicting timeslot heuristic:", result3)

    assert abs(result3 - 1/6) < 1e-9

    print("Third heuristic test passed.")

    relationships["exam_student_counts"] = {
        "E1": 2,
        "E2": 1
    }

    relationships["room_capacities"] = {
        "R1": 2,
        "R2": 1
    }



    feasible = get_feasible_assignments(
        "E2",
        partial_schedule,
        relationships
    )

    print("Feasible assignments:", feasible)

       
    expected = {
        ("T2", "R1"),
        ("T2", "R2"),
        ("T3", "R1"),
        ("T3", "R2")
    }

    assert set(feasible) == expected

    print("Feasible assignments test passed.")



    capacity_test = get_feasible_assignments(
        "E1",
        {},
        relationships
    )

    expected_capacity = {
        ("T1", "R1"),
        ("T2", "R1"),
        ("T3", "R1")
    }

    assert set(capacity_test) == expected_capacity

    print("Room capacity test passed.")


    relationships["exam_students"]["E3"] = {"S3"}
    relationships["exam_student_counts"]["E3"] = 1

    room_conflict_test = get_feasible_assignments(
        "E3",
        partial_schedule,
        relationships
    )

    assert ("T1", "R1") not in room_conflict_test
    assert ("T1", "R2") in room_conflict_test

    print("Room conflict test passed.")

    relationships["exam_students"]["E4"] = {"S1"}
    relationships["exam_students"]["E5"] = {"S1"}
    relationships["exam_student_counts"]["E4"] = 1
    relationships["exam_student_counts"]["E5"] = 1

    full_schedule = {
        "E1": ("T1", "R1"),
        "E2": ("T2", "R1"),
        "E4": ("T3", "R1")
    }

    no_options = get_feasible_assignments(
        "E5",
        full_schedule,
        relationships
    )
    assert no_options == []
    print("No feasible assignments test passed.")

    test_data = {
        "exams": [
            {"exam_id": "E1"},
            {"exam_id": "E2"}
        ]
    }

    pheromones = initialize_pheromones(
        test_data,
        relationships
    )

    print("Pheromone entries:", len(pheromones))
    assert len(pheromones) == 9
    assert all(value == 1.0 for value in pheromones.values())
    print("Pheromone initialization test passed.")

    rng = random.Random(42)

    selected = select_next_assignment(
        "E2",
        feasible,
        partial_schedule,
        relationships,
        pheromones,
        alpha=1,
        beta=2,
        rng=rng
    )

    print("Selected assignment:", selected)
    assert selected in feasible
    print("Assignment selection test passed.")

    selected_empty = select_next_assignment(
        "E5",
        no_options,
        full_schedule,
        relationships,
        pheromones,
        alpha=1,
        beta=2,
        rng=rng
    )

    assert selected_empty is None

    print("Empty selection test passed.")

    small_data = load_data("small")
    small_relationships = build_relationships(small_data)

    small_pheromones = initialize_pheromones(
        small_data,
        small_relationships
    )

    print("Small exams:", len(small_data["exams"]))

    ant_solution = construct_ant_solution(
        small_data,
        small_relationships,
        small_pheromones,
        alpha=1,
        beta=2,
        rng=random.Random(42)
    )

    print("Ant solution:", ant_solution)

    assert ant_solution is not None
    assert len(ant_solution) == len(small_data["exams"])

    violations = validate_schedule(
        ant_solution,
        small_data,
        small_relationships
    )

    print("Hard constraint violations:", violations)

    assert not violations
    print("Ant construction test passed.")

    test_pheromones = {
        ("E1", "T1", "R1"): 1.0,
        ("E2", "T2", "R1"): 0.5
    }

    evaporate_pheromones(test_pheromones, 0.2)

    print("Pheromones after evaporation:", test_pheromones)

    assert abs(test_pheromones[("E1", "T1", "R1")] - 0.8) < 1e-9
    assert abs(test_pheromones[("E2", "T2", "R1")] - 0.4) < 1e-9

    print("Pheromone evaporation test passed.")


    # Test pheromone update.
    test_pheromones = {
        ("E1", "T1", "R1"): 0.8,
        ("E2", "T2", "R1"): 0.5
    }

    test_solution = {
        "E1": ("T1", "R1")
    }

    update_pheromones(
        test_pheromones,
        test_solution,
        fitness=9,
        q=2
    )

    print("Pheromones after update:", test_pheromones)

    assert abs(test_pheromones[("E1", "T1", "R1")] - 1.0) < 1e-9
    assert abs(test_pheromones[("E2", "T2", "R1")] - 0.5) < 1e-9

    print("Pheromone update test passed.")

    best_solution, best_fitness, history = run_aco(
        small_data,
        small_relationships,
        num_ants=5,
        num_iterations=10,
        alpha=1,
        beta=2,
        evaporation_rate=0.2,
        q=2,
        seed=42
    )

    print("Best ACO fitness:", best_fitness)
    print("Best ACO solution:", best_solution)
    print("ACO history:", history)

    assert best_solution is not None
    assert len(best_solution) == len(small_data["exams"])

    aco_violations = validate_schedule(
        best_solution,
        small_data,
        small_relationships
    )

    print("ACO hard constraint violations:", aco_violations)

    assert not aco_violations
    print("ACO best schedule test passed.")

    checked_penalties = calculate_soft_penalties(
        best_solution,
        small_data,
        small_relationships
    )

    assert abs(checked_penalties["weighted_total"] - best_fitness) < 1e-9

    print("ACO fitness test passed.")
    