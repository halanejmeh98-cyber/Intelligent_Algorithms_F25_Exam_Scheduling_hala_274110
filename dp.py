from main import (load_data, validate_data,build_relationships,check_enrollment_consistency,
                  validate_schedule,calculate_soft_penalties)
from itertools import combinations
from functools import lru_cache
import time
import csv
from pathlib import Path

data = load_data("small")
validate_data(data)
relationships = build_relationships(data)
check_enrollment_consistency(data, relationships)

def generate_daily_assignments(day, available_exams, relationships):
    timeslots = [
        slot for slot in relationships["ordered_timeslots"]
        if relationships["timeslot_info"][slot]["day"] == day
    ]

    exam_students = relationships["exam_students"]

    groups = [()]

    for exam in available_exams:
        groups.append((exam,))

   
    for exam1, exam2 in combinations(available_exams, 2):
        if not exam_students[exam1].intersection(exam_students[exam2]):
            groups.append((exam1, exam2))

    daily_assignments = []

    for first_group in groups:
        for second_group in groups:

            if set(first_group).intersection(second_group):
                continue

            assignment = {}

            for exam in first_group:
                assignment[exam] = timeslots[0]

            for exam in second_group:
                assignment[exam] = timeslots[1]

            daily_assignments.append(assignment)

    return daily_assignments


def calculate_daily_penalties(daily_assignment, previous_day_exams, relationships):
    exam_students = relationships["exam_students"]
    timeslot_info = relationships["timeslot_info"]

  
    student_periods = {}

    for exam, slot in daily_assignment.items():
        period = timeslot_info[slot]["period_index"]

        for student in exam_students[exam]:
            student_periods.setdefault(student, []).append(period)


    P1 = sum(
        1 for periods in student_periods.values()
        if len(periods) > 1
    )

    P2 = 0
    for periods in student_periods.values():
        for i in range(len(periods)):
            for j in range(i + 1, len(periods)):
                if abs(periods[i] - periods[j]) == 1:
                    P2 += 1

    P3 = (len(daily_assignment) - 2) ** 2
    P4 = 0
    for exam in daily_assignment:
        for previous_exam in previous_day_exams:
            P4 += len(
                exam_students[exam] & exam_students[previous_exam]
            )

    daily_cost = 3 * P1 + P2 + P3 + 4 * P4

    return {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P4": P4,
        "daily_cost": daily_cost
    }


def run_dp(data, relationships):
    exam_ids = [exam["exam_id"] for exam in data["exams"]]

    days = sorted({
        info["day"]
        for info in relationships["timeslot_info"].values()
    })

    exam_bits = {
        exam: 1 << i for i, exam in enumerate(exam_ids)
    }

    full_mask = (1 << len(exam_ids)) - 1
    best_choices = {}

    @lru_cache(maxsize=None)
    def dp(day_index, used_mask, previous_mask):

        if day_index == len(days):
            if used_mask == full_mask:
                return 0
            return float("inf")

        remaining = [
            exam for exam in exam_ids
            if not (used_mask & exam_bits[exam])
        ]

        previous = [
            exam for exam in exam_ids
            if previous_mask & exam_bits[exam]
        ]

        best_cost = float("inf")
        best_assignment = None

        daily_options = generate_daily_assignments(
            days[day_index], remaining, relationships
        )

        for assignment in daily_options:
            day_mask = 0

            for exam in assignment:
                day_mask |= exam_bits[exam]

            penalties = calculate_daily_penalties(
                assignment, previous, relationships
            )

            future_cost = dp(
                day_index + 1,
                used_mask | day_mask,
                day_mask
            )

            total_cost = penalties["daily_cost"] + future_cost

            if total_cost < best_cost:
                best_cost = total_cost
                best_assignment = assignment

        if best_assignment is not None:
            best_choices[
                (day_index, used_mask, previous_mask)
            ] = best_assignment

        return best_cost
    best_fitness = dp(0, 0, 0)

    cache_info = dp.cache_info()

    return best_fitness, best_choices, exam_ids, days, cache_info


def reconstruct_schedule(best_choices, exam_ids, days, relationships):
    exam_bits = {
        exam: 1 << i for i, exam in enumerate(exam_ids)
    }

    room_capacities = relationships["room_capacities"]
    exam_counts = relationships["exam_student_counts"]

    schedule = {}
    used_room_slots = set()

    used_mask = 0
    previous_mask = 0

    for day_index in range(len(days)):
        state = (day_index, used_mask, previous_mask)

        if state not in best_choices:
            raise ValueError("No valid DP assignment found.")

        daily_assignment = best_choices[state]
        day_mask = 0

        for exam, slot in daily_assignment.items():

            selected_room = None

            for room, capacity in room_capacities.items():
                if (
                    capacity >= exam_counts[exam]
                    and (slot, room) not in used_room_slots
                ):
                    selected_room = room
                    break

            if selected_room is None:
                raise ValueError(f"No available room for {exam}.")

            schedule[exam] = (slot, selected_room)
            used_room_slots.add((slot, selected_room))

            day_mask |= exam_bits[exam]

        used_mask |= day_mask
        previous_mask = day_mask

    return schedule

start_time = time.perf_counter()

best_fitness, best_choices, exam_ids, days, cache_info = run_dp(
    data, relationships
)

final_schedule = reconstruct_schedule(
    best_choices, exam_ids, days, relationships
)
execution_time = time.perf_counter() - start_time

errors = validate_schedule(final_schedule, data, relationships)

print("Scheduled Exams:", len(final_schedule))
print("Hard Violations:", len(errors))

if errors:
    print(errors)
else:
    penalties = calculate_soft_penalties(
        final_schedule, data, relationships
    )

    print("DP Best Fitness:", best_fitness)
    print("Final Fitness:", penalties["weighted_total"])
    print(
        "Fitness Match:",
        best_fitness == penalties["weighted_total"]
    )
    print("P1:", penalties["P1"])
    print("P2:", penalties["P2"])
    print("P3:", penalties["P3"])
    print("P4:", penalties["P4"])

    print("\nFinal Schedule:")

    for exam, (slot, room) in sorted(final_schedule.items()):
        info = relationships["timeslot_info"][slot]

        print(
            f"{exam}: Day {info['day']}, "
            f"Period {info['period_index']}, "
            f"Timeslot {slot}, Room {room}"
        )


print(f"Execution Time: {execution_time:.4f} seconds")
print("DP States:", cache_info.misses)
print("Cache Hits:", cache_info.hits)
print("Cached States:", cache_info.currsize)


if not errors and best_fitness == penalties["weighted_total"]:
    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(exist_ok=True)

    with (results_dir / "dp_small_experiments.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "best_fitness", "execution_time", "hard_violations",
            "P1", "P2", "P3", "P4",
            "dp_states", "cache_hits", "cached_states", "schedule"
        ])

        writer.writerow([
            best_fitness,
            execution_time,
            len(errors),
            penalties["P1"],
            penalties["P2"],
            penalties["P3"],
            penalties["P4"],
            cache_info.misses,
            cache_info.hits,
            cache_info.currsize,
            str(dict(sorted(final_schedule.items())))
        ])

    print("DP Small results saved successfully.")
else:
    print("Results not saved: validation failed.")