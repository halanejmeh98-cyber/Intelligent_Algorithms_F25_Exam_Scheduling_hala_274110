
import csv
from pathlib import Path
import random


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def read_csv(filename, size):
    with (DATA_DIR / size / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def load_data(size="small"):
    files = {
        "exams": "exams.csv",
        "students": "students.csv",
        "enrollments": "enrollments.csv",
        "rooms": "rooms.csv",
        "timeslots": "timeslots.csv",
    }
    return {name: read_csv(filename, size) for name, filename in files.items()}


def validate_data(data):
    required = {
        "exams": {"exam_id", "exam_name", "num_students"},
        "students": {"student_id", "student_name"},
        "enrollments": {"student_id", "exam_id"},
        "rooms": {"room_id", "room_name", "capacity"},
        "timeslots": {"timeslot_id", "day", "period_index", "period_name"},
    }

    id_columns = {
        "exams": "exam_id",
        "students": "student_id",
        "rooms": "room_id",
        "timeslots": "timeslot_id",
    }

    for table, columns in required.items():
        if not data[table]:
            raise ValueError(f"{table}.csv is empty.")

        missing = columns - set(data[table][0])
        if missing:
            raise ValueError(f"{table}.csv is missing columns: {missing}")

    for table, column in id_columns.items():
        ids = [row[column] for row in data[table]]
        if any(not value for value in ids) or len(ids) != len(set(ids)):
            raise ValueError(f"Empty or duplicate IDs in {table}.csv")

    exam_ids = {row["exam_id"] for row in data["exams"]}
    student_ids = {row["student_id"] for row in data["students"]}
    seen = set()

    for row in data["enrollments"]:
        student_id, exam_id = row["student_id"], row["exam_id"]
        pair = (student_id, exam_id)

        if student_id not in student_ids or exam_id not in exam_ids:
            raise ValueError(f"Invalid enrollment: {pair}")
        if pair in seen:
            raise ValueError(f"Duplicate enrollment: {pair}")
        seen.add(pair)

    for room in data["rooms"]:
        if not room["capacity"].isdigit() or int(room["capacity"]) <= 0:
            raise ValueError(f"Invalid capacity for room {room['room_id']}")

    for exam in data["exams"]:
        if not exam["num_students"].isdigit():
            raise ValueError(f"Invalid student count for {exam['exam_id']}")

    for slot in data["timeslots"]:
        if not slot["day"].isdigit() or not slot["period_index"].isdigit():
            raise ValueError(f"Invalid timeslot: {slot['timeslot_id']}")

    print("Data validation passed.")


def build_relationships(data):
    exam_students = {row["exam_id"]: set() for row in data["exams"]}
    student_exams = {row["student_id"]: set() for row in data["students"]}

    for row in data["enrollments"]:
        exam_students[row["exam_id"]].add(row["student_id"])
        student_exams[row["student_id"]].add(row["exam_id"])

    room_capacities = {
        row["room_id"]: int(row["capacity"]) for row in data["rooms"]
    }

    timeslot_info = {
        row["timeslot_id"]: {
            "day": int(row["day"]),
            "period_index": int(row["period_index"]),
            "period_name": row["period_name"],
        }
        for row in data["timeslots"]
    }

    ordered_timeslots = sorted(
        timeslot_info,
        key=lambda slot: (
            timeslot_info[slot]["day"],
            timeslot_info[slot]["period_index"],
        ),
    )

    return {
        "exam_students": exam_students,
        "student_exams": student_exams,
        "room_capacities": room_capacities,
        "timeslot_info": timeslot_info,
        "ordered_timeslots": ordered_timeslots,
        "exam_student_counts": {
            exam_id: len(students)
            for exam_id, students in exam_students.items()
        },
    }


def check_enrollment_consistency(data, relationships):
    for exam in data["exams"]:
        exam_id = exam["exam_id"]
        declared = int(exam["num_students"])
        actual = relationships["exam_student_counts"][exam_id]

        if declared != actual:
            raise ValueError(
                f"{exam_id}: declared {declared} students, "
                f"but found {actual} enrollments."
            )

    print("Enrollment consistency check passed.")


def create_empty_solution():
    return {}


def validate_schedule(solution, data, relationships):
    errors = []
    exam_ids = {row["exam_id"] for row in data["exams"]}
    room_capacities = relationships["room_capacities"]
    timeslot_info = relationships["timeslot_info"]
    exam_students = relationships["exam_students"]
    student_counts = relationships["exam_student_counts"]

    # H4: Missing or unknown exams
    for exam_id in exam_ids - set(solution):
        errors.append(f"H4: Exam {exam_id} has no assignment.")

    for exam_id in set(solution) - exam_ids:
        errors.append(f"H4: Unknown exam {exam_id}.")

    valid = {}

    for exam_id, assignment in solution.items():
        if exam_id not in exam_ids:
            continue

        if (
            not isinstance(assignment, (tuple, list))
            or len(assignment) != 2
        ):
            errors.append(f"H4: Invalid assignment for {exam_id}.")
            continue

        slot, room = assignment

        if not isinstance(slot, str) or not slot or not isinstance(room, str) or not room:
            errors.append(f"H4: Invalid assignment for {exam_id}.")
            continue

        if slot not in timeslot_info:
            errors.append(f"H5: Unavailable timeslot {slot} for {exam_id}.")
        if room not in room_capacities:
            errors.append(f"H5: Unavailable room {room} for {exam_id}.")

        if slot in timeslot_info and room in room_capacities:
            valid[exam_id] = (slot, room)

    room_usage = {}

    for exam_id, (slot, room) in valid.items():
        key = (slot, room)

        if key in room_usage:
            errors.append(
                f"H2: Exams {room_usage[key]} and {exam_id} "
                f"share room {room} in {slot}."
            )
        else:
            room_usage[key] = exam_id

        if student_counts[exam_id] > room_capacities[room]:
            errors.append(f"H3: Insufficient capacity for {exam_id} in {room}.")


    student_usage = {}

    for exam_id, (slot, _) in valid.items():
        for student_id in exam_students[exam_id]:
            key = (student_id, slot)

            if key in student_usage:
                errors.append(
                    f"H1: Student {student_id} has exams "
                    f"{student_usage[key]} and {exam_id} in {slot}."
                )
            else:
                student_usage[key] = exam_id

    return errors


def create_random_solution(data, relationships, seed=None):
    """
    Generate a random schedule satisfying all hard constraints.

    Returns:
        A dictionary mapping each exam ID to (timeslot_id, room_id).

    Raises:
        ValueError if no valid schedule can be constructed.
    """
    rng = random.Random(seed)

    exam_students = relationships["exam_students"]
    exam_counts = relationships["exam_student_counts"]
    room_capacities = relationships["room_capacities"]
    timeslot_info = relationships["timeslot_info"]

    exam_ids = [exam["exam_id"] for exam in data["exams"]]
    timeslot_ids = list(timeslot_info)

    candidates = {}

    for exam_id in exam_ids:
        suitable_rooms = [
            room_id
            for room_id, capacity in room_capacities.items()
            if capacity >= exam_counts[exam_id]
        ]

        choices = [
            (timeslot_id, room_id)
            for timeslot_id in timeslot_ids
            for room_id in suitable_rooms
        ]

        if not choices:
            raise ValueError(
                f"No suitable room is available for {exam_id}."
            )

        rng.shuffle(choices)
        candidates[exam_id] = choices

    rng.shuffle(exam_ids)
    exam_ids.sort(
        key=lambda exam_id: (
            len(candidates[exam_id]),
            -exam_counts[exam_id],
        )
    )

    solution = {}
    used_room_slots = set()

    students_in_slot = {
        timeslot_id: set()
        for timeslot_id in timeslot_ids
    }

    def backtrack(index):

        if index == len(exam_ids):
            return True

        exam_id = exam_ids[index]
        enrolled_students = exam_students[exam_id]

        for timeslot_id, room_id in candidates[exam_id]:
            room_slot = (timeslot_id, room_id)

            if room_slot in used_room_slots:
                continue

            if enrolled_students.intersection(
                students_in_slot[timeslot_id]
            ):
                continue

            solution[exam_id] = (timeslot_id, room_id)
            used_room_slots.add(room_slot)
            students_in_slot[timeslot_id].update(enrolled_students)

            if backtrack(index + 1):
                return True

            del solution[exam_id]
            used_room_slots.remove(room_slot)
            students_in_slot[timeslot_id].difference_update(
                enrolled_students
            )

        return False

    if not backtrack(0):
        raise ValueError(
            "Could not construct a valid schedule. "
            "Check room capacities, available timeslots, "
            "and student enrollment conflicts."
        )
    
    errors = validate_schedule(solution, data, relationships)

    if errors:
        raise RuntimeError(
            "The generated schedule failed validation:\n"
            + "\n".join(errors)
        )

    return solution


def calculate_soft_penalties(solution, data, relationships):
    """
    Calculate the four soft-constraint penalties and
    their weighted total.

    The schedule must satisfy all hard constraints.
    """

    errors = validate_schedule(solution, data, relationships)

    if errors:
        raise ValueError(
            "Cannot calculate soft penalties for an invalid schedule:\n"
            + "\n".join(errors)
        )

    exam_students = relationships["exam_students"]
    timeslot_info = relationships["timeslot_info"]

    # Count exams per day and collect each student's exam times.
    days = sorted({
        info["day"] for info in timeslot_info.values()
    })

    daily_exam_counts = {day: 0 for day in days}
    student_day_counts = {}
    student_exam_schedule = {
        student_id: []
        for student_id in relationships["student_exams"]
    }

    for exam_id, (timeslot_id, room_id) in solution.items():
        slot = timeslot_info[timeslot_id]
        day = slot["day"]
        period = slot["period_index"]

        daily_exam_counts[day] += 1

        for student_id in exam_students[exam_id]:

            key = (student_id, day)
            student_day_counts[key] = (
                student_day_counts.get(key, 0) + 1
            )

            student_exam_schedule[student_id].append(
                (day, period, exam_id)
            )

    P1 = sum(
        1
        for count in student_day_counts.values()
        if count > 1
    )


    P2 = 0

    for exams in student_exam_schedule.values():
        for i in range(len(exams)):
            day1, period1, _ = exams[i]

            for j in range(i + 1, len(exams)):
                day2, period2, _ = exams[j]

                if (
                    day1 == day2
                    and abs(period1 - period2) == 1
                ):
                    P2 += 1

    average_exams = (
        sum(daily_exam_counts.values()) / len(days)
    )

    P3 = sum(
        (count - average_exams) ** 2
        for count in daily_exam_counts.values()
    )

    P4 = 0

    for exams in student_exam_schedule.values():
        for i in range(len(exams)):
            day1, _, _ = exams[i]

            for j in range(i + 1, len(exams)):
                day2, _, _ = exams[j]

                if abs(day1 - day2) == 1:
                    P4 += 1

    total = 3 * P1 + P2 + P3 + 4 * P4

    return {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "P4": P4,
        "weighted_total": total,
    }


def main():
    data = load_data()
    validate_data(data)

    relationships = build_relationships(data)
    check_enrollment_consistency(data, relationships)
    
    print(f"Loaded {len(data['exams'])} exams.")
    print(f"Available rooms: {len(data['rooms'])}")
    print(f"Available timeslots: {len(data['timeslots'])}")


if __name__ == "__main__":
    main()
