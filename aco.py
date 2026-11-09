import random
from main import calculate_soft_penalties

def calculate_heuristic(
    exam_id,
    timeslot_id,
    partial_schedule,
    relationships
):

    exam_students = relationships["exam_students"]
    timeslot_info = relationships["timeslot_info"]

    target = timeslot_info[timeslot_id]
    target_day = target["day"]
    target_period = target["period_index"]

    students = exam_students[exam_id]

    same_day_students = set()
    p2 = 0
    p4 = 0
    daily_count = 0

    for other_exam, (other_slot, _) in partial_schedule.items():

        other = timeslot_info[other_slot]
        other_day = other["day"]
        other_period = other["period_index"]

        shared_students = students & exam_students[other_exam]

        if other_day == target_day:
            daily_count += 1
            same_day_students.update(shared_students)

            if abs(target_period - other_period) == 1:
                p2 += len(shared_students)

        if abs(target_day - other_day) == 1:
            p4 += len(shared_students)

    total_days = len({
        info["day"] for info in timeslot_info.values()
    })

    scheduled_exams = len(partial_schedule)

    p3_delta = (
        2 * daily_count + 1
        - (2 * scheduled_exams + 1) / total_days
    )

    min_p3_delta = (
        1 - (2 * scheduled_exams + 1) / total_days
    )

    p3_cost = p3_delta - min_p3_delta

    estimated_cost = (
        3 * len(same_day_students)
        + p2
        + p3_cost
        + 4 * p4
    )

    heuristic = 1 / (1 + estimated_cost)
    return heuristic

def get_feasible_assignments(
    exam_id,
    partial_schedule,
    relationships
):

    feasible = []
    
    
    exam_size = relationships["exam_student_counts"][exam_id]
    room_capacities = relationships["room_capacities"]
    
    suitable_rooms = []
    
    for room_id, capacity in room_capacities.items():
        if capacity >= exam_size:
            suitable_rooms.append(room_id)
    
    used_room_slots = set(partial_schedule.values())
    
    for timeslot_id in relationships["timeslot_info"]:
        for room_id in suitable_rooms:
    
            if (timeslot_id, room_id) in used_room_slots:
                continue
            student_conflict = False

            for other_exam, (other_slot, _) in partial_schedule.items():
    
                if other_slot == timeslot_id:
                    shared_students = (
                        relationships["exam_students"][exam_id]
                        & relationships["exam_students"][other_exam]
                    )
    
                    if shared_students:
                        student_conflict = True
                        break
    
            if student_conflict:
                continue   
            feasible.append((timeslot_id, room_id))
    
    return feasible

def initialize_pheromones(data, relationships, initial_value=1.0):

    pheromones = {}

    for exam in data["exams"]:
        exam_id = exam["exam_id"]

        choices = get_feasible_assignments(
            exam_id,
            {},
            relationships
        )

        for timeslot_id, room_id in choices:
            pheromones[(exam_id, timeslot_id, room_id)] = initial_value

    return pheromones

def select_next_assignment(
    exam_id,
    feasible,
    partial_schedule,
    relationships,
    pheromones,
    alpha,
    beta,
    rng
):
    weights = []

    for timeslot_id, room_id in feasible:
        pheromone = pheromones[(exam_id, timeslot_id, room_id)]

        heuristic = calculate_heuristic(
            exam_id,
            timeslot_id,
            partial_schedule,
            relationships
        )

        weight = (pheromone ** alpha) * (heuristic ** beta)
        weights.append(weight)


       
    if not feasible:
        return None

    
    selected = rng.choices(feasible, weights=weights, k=1)[0]

    return selected


# Construct a complete exam schedule for one ant.
def construct_ant_solution(
    data,
    relationships,
    pheromones,
    alpha,
    beta,
    rng
):
    solution = {}
    exam_ids = [exam["exam_id"] for exam in data["exams"]]
       
    rng.shuffle(exam_ids)

    exam_ids.sort(
        key=lambda exam_id: -relationships["exam_student_counts"][exam_id]
    )

    # Find valid choices for each exam.
    for exam_id in exam_ids:
        feasible = get_feasible_assignments(
            exam_id,
            solution,
            relationships
        )

        if not feasible:
            return None

        selected = select_next_assignment(
            exam_id,
            feasible,
            solution,
            relationships,
            pheromones,
            alpha,
            beta,
            rng
        )
               
        solution[exam_id] = selected
    return solution


def evaporate_pheromones(pheromones, evaporation_rate):

    for key in pheromones:
        pheromones[key] *= (1 - evaporation_rate)


def update_pheromones(pheromones, solution, fitness, q):

    deposit = q / (1 + fitness)

    for exam_id, (timeslot_id, room_id) in solution.items():
        key = (exam_id, timeslot_id, room_id)
        pheromones[key] += deposit

def run_aco(
    data,
    relationships,
    num_ants,
    num_iterations,
    alpha,
    beta,
    evaporation_rate,
    q,
    seed=42
    
):
    rng = random.Random(seed)
    pheromones = initialize_pheromones(data, relationships)
    best_solution = None
    best_fitness = float("inf")
    history = []


    for iteration in range(num_iterations):
        iteration_solutions = []

        for ant in range(num_ants):

            solution = construct_ant_solution(
                data,
                relationships,
                pheromones,
                alpha,
                beta,
                rng
            )

            if solution is None:
                continue

            penalties = calculate_soft_penalties(
                solution,
                data,
                relationships
            )

            fitness = penalties["weighted_total"]
            
         
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution.copy()

            iteration_solutions.append((solution, fitness))
        evaporate_pheromones(pheromones, evaporation_rate)

        for solution, fitness in iteration_solutions:
            update_pheromones(
                pheromones,
                solution,
                fitness,
                q
            )
                  
        history.append(best_fitness)

    if best_solution is None:
        return None, float("inf"), history

    return best_solution, best_fitness, history