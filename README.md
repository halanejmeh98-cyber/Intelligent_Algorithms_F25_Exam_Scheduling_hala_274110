# Exam Scheduling Optimization

## Project Overview

In this project, we worked on exam scheduling. The goal is to assign exams to rooms and time slots without conflicts and reduce soft constraint penalties.

We implemented three optimization algorithms: Genetic Algorithm (GA), Ant Colony Optimization (ACO), and Particle Swarm Optimization (PSO). We also implemented Dynamic Programming (DP) for the Small dataset.

We tested the algorithms and compared their results to see how they perform on different dataset sizes.

## Project Structure

The project contains the main functions, optimization algorithms, test files, and experiment results.

- **main.py:** Contains the shared functions for loading data, creating schedules, checking hard constraints, and calculating soft penalties.

- **ga.py:** Contains the Genetic Algorithm implementation.

- **aco.py:** Contains the Ant Colony Optimization implementation.

- **pso.py:** Contains the Particle Swarm Optimization implementation.

- **dp.py:** Contains the Dynamic Programming implementation for the Small dataset.

- **ga_tests.py and aco_tests.py:** Used to test the main operations of GA and ACO.

- **ga_best_test.py, ga_medium_best_test.py, and ga_large_best_test.py:** Test GA parameter combinations on the Small, Medium, and Large datasets.

- **ga_medium_experiments.py and ga_large_experiments.py:** Run GA experiments on Medium and Large datasets.

- **aco_small_experiments.py, aco_medium_experiments.py, and aco_large_experiments.py:** Run ACO parameter tuning experiments.

- **pso_small_experiments.py, pso_medium_experiments.py, and pso_large_experiments.py:** Run PSO parameter tuning experiments.

- **pso_small_combined_test.py, pso_medium_combined_test.py, and pso_large_combined_test.py:** Test selected PSO parameter combinations.

- **results/:** Contains CSV files with fitness values, execution times, hard constraint violations, and experiment results.

- **README.md:** Explains the project, the algorithms, and the experiments.

## How to Run

The project uses Python 3.

Open the project folder in VS Code and run the commands from its terminal.

The `data` folder contains three subfolders:

- `data/small/`
- `data/medium/`
- `data/large/`

Each subfolder must contain `exams.csv`, `students.csv`, `enrollments.csv`, `rooms.csv`, and `timeslots.csv`.

Keep the `results` folder in the project directory to store the experiment results.

### Shared Functions

To check the data and shared functions, run:

```bash
python main.py
```

### Genetic Algorithm (GA)

To run the GA experiments on Medium and Large, use:

```bash
python ga_medium_experiments.py
python ga_large_experiments.py
```

To run the additional GA tests, use:

```bash
python ga_best_test.py
python ga_medium_best_test.py
python ga_large_best_test.py
```

To test the main GA operations, use:

```bash
python ga_tests.py
```

### Ant Colony Optimization (ACO)

To run the ACO experiments, use:

```bash
python aco_small_experiments.py
python aco_medium_experiments.py
python aco_large_experiments.py
```

To test the main ACO operations, use:

```bash
python aco_tests.py
```

### Particle Swarm Optimization (PSO)

To run the PSO parameter tuning experiments, use:

```bash
python pso_small_experiments.py
python pso_medium_experiments.py
python pso_large_experiments.py
```

To run the additional PSO combined tests, use:

```bash
python pso_small_combined_test.py
python pso_medium_combined_test.py
python pso_large_combined_test.py
```

### Dynamic Programming (DP)

To run Dynamic Programming on the Small dataset, use:

```bash
python dp.py
```

### Experiment Results

The experiment results are saved as CSV files in the `results` folder.

These files contain fitness values, execution times, hard constraint violations, and other experiment information.

Some experiment scripts overwrite existing CSV files, while others append new results. Keep a backup of the saved results before running the experiments again.

## Shared Functions (main.py)

The `main.py` file contains the shared functions used in the exam scheduling project.

- **read_csv():** Reads data from CSV files.
- **load_data():** Loads the exam, student, enrollment, room, and timeslot data.
- **validate_data():** Checks if the input data is valid.
- **build_relationships():** Builds relationships between students, exams, rooms, and time slots.
- **check_enrollment_consistency():** Checks if the number of students in each exam matches the enrollment records.
- **create_empty_solution():** Creates an empty schedule.
- **validate_schedule():** Checks if a schedule satisfies all hard constraints.
- **create_random_solution():** Generates a random valid exam schedule using backtracking.
- **calculate_soft_penalties():** Calculates the four soft penalties and their weighted total.
- **main():** Loads and checks the data, builds relationships, and displays basic information.

### Schedule Representation

An exam schedule is represented as a Python dictionary.

Each exam ID is mapped to a tuple containing its assigned time slot and room:

`exam_id: (timeslot_id, room_id)`

Every exam must have exactly one valid assignment.


### Hard Constraints

The exam schedule must satisfy five hard constraints:

- **H1 – Student Conflict:** A student cannot have two exams in the same timeslot.
- **H2 – Room Conflict:** Two exams cannot use the same room in the same timeslot.
- **H3 – Room Capacity:** The number of students taking an exam must not exceed the assigned room capacity.
- **H4 – Exam Assignment:** Every exam must have exactly one valid assignment.
- **H5 – Resource Availability:** Each assigned room and timeslot must exist in the available dataset.

The `validate_schedule()` function checks these constraints and returns a list of violations.

A schedule is considered valid only when the list is empty.

### Data Validation

Before generating schedules, the shared functions can check the input data for:

- Missing required columns or empty CSV files.
- Empty or duplicate IDs.
- Invalid or duplicate enrollment records.
- Invalid room capacities, student counts, or time slot values.
- Differences between declared exam student counts and enrollment records.

The `main()` function performs data validation and enrollment consistency checks when `main.py` is executed directly.

### Random Valid Schedule Generation

The `create_random_solution()` function uses randomized backtracking to generate valid exam schedules.

It prepares possible room and time slot assignments, prioritizes constrained exams, and checks conflicts while building the schedule.

If an assignment causes a conflict, backtracking allows the function to try another assignment.

A random seed can be provided to make the generation reproducible.

Before returning the schedule, the function verifies that all hard constraints are satisfied.

If no valid schedule can be constructed, the function raises an error.

## Dataset
- **exams.csv:** Contains exam IDs, names, and the number of students in each exam.
- **enrollments.csv:** Shows which students are registered for each exam.
- **rooms.csv:** Contains room IDs, room names, and the capacity of each room.
- **students.csv:** Contains student IDs and student names.
- **timeslots.csv:** Contains time slot IDs, days, period numbers, and period names.



### Dataset Sizes

The project uses three dataset sizes: Small, Medium, and Large.

| Dataset | Small | Medium | Large |
|---|---:|---:|---:|
| Exams | 10 | 40 | 100 |
| Students | 30 | 100 | 300 |
| Rooms | 3 | 6 | 12 |
| Days | 5 | 10 | 20 |
| Periods per day | 2 | 3 | 4 |
| Total timeslots | 10 | 30 | 80 |


### Initial Baseline

Before applying the optimization algorithms, an initial baseline result was provided by a team member.

According to `initial_baseline.csv`, the baseline was generated using Randomized Backtracking with random seed 42 on the Small dataset.

The baseline produced a valid exam schedule with zero hard constraint violations.

**Baseline Results (Small Dataset):**

| Metric | Value |
|---|---:|
| Random Seed | 42 |
| P1 | 20 |
| P2 | 20 |
| P3 | 0 |
| P4 | 78 |
| Weighted Total | 392.0 |
| Runtime (seconds) | 0.001080 |
| Hard Constraint Violations | 0 |

The baseline serves as a reference for evaluating the improvement achieved by the optimization algorithms.

The results are stored in `results/initial_baseline.csv`.


## Genetic Algorithm (GA)
### Initial Population

We created a function called `create_population()` in `ga.py` to generate the initial population.

The function uses `create_random_solution()` from `main.py` to generate valid exam schedules and stores them in a list.

**Initial Test (Small Dataset):**

- Population Size: 10 (for testing only)
- Number of Exams: 10
- Generated Schedules: 10
- Exams in the First Schedule: 10

The initial test was successful. We confirmed that the function generates the requested number of schedules.

We later tested population sizes of 10, 20, and 40 during GA parameter tuning. The results are presented in the GA Parameter Tuning – Small Dataset section.

### Schedule Validation

We use `create_random_solution()` from `main.py` to generate valid exam schedules. This function checks all hard constraints using `validate_schedule()` before returning a schedule.

Also, `calculate_soft_penalties()` checks the hard constraints before calculating penalties.

Therefore, we do not need to repeat the validation separately for the initial population. We can directly calculate the soft penalties.

However, new schedules created by Crossover or Mutation will also need to satisfy all hard constraints.

### Fitness Evaluation

We use `calculate_soft_penalties()` from `main.py` to evaluate each exam schedule.

The function calculates four soft penalties (P1, P2, P3, and P4) and returns their weighted total.

A lower weighted total means a better schedule.

In our initial test on the Small dataset, we evaluated 10 schedules. The lowest penalty was **316.0**, found in Schedule 3.


### Soft Constraints and Penalties

After verifying that a schedule satisfies all hard constraints, the `calculate_soft_penalties()` function evaluates four soft constraints.

- **P1 – Multiple Exams per Day:** Counts each student-day combination where a student has more than one exam. Each affected student-day receives one penalty.

- **P2 – Consecutive Exam Periods:** Counts pairs of exams scheduled in consecutive periods on the same day for each student.

- **P3 – Uneven Exam Distribution:** Measures how unevenly exams are distributed across the available days. It calculates the sum of squared differences between the number of exams each day and the average number of exams per day.

- **P4 – Exams on Consecutive Days:** Counts pairs of exams scheduled on consecutive calendar days for each student.

The goal is to minimize these penalties while keeping all hard constraints satisfied.

The penalties are combined into a weighted total, which is used as the fitness value by the Genetic Algorithm.

### Fitness Weights and Rationale

The objective function uses a weighted sum of four soft penalties:

**Weighted Total = 3 × P1 + 1 × P2 + 1 × P3 + 4 × P4**

We assigned different weights based on the importance of each soft constraint.

- **P1 (Weight = 3):** Having multiple exams on the same day increases student workload and stress. Therefore, we assigned a relatively high weight to this penalty.
- **P2 (Weight = 1):** Consecutive exam periods on the same day can be tiring for students. We included this penalty with a lower weight because P1 already penalizes having multiple exams on the same day.
- **P3 (Weight = 1):** Distributing exams evenly across available days helps create a balanced timetable. However, we gave it a lower weight than constraints directly related to student workload.
- **P4 (Weight = 4):** Exams scheduled on consecutive calendar days leave less time for preparation and revision. We assigned the highest weight to this penalty to prioritize reducing such situations.

These weights represent our initial design priorities. They were not determined through a separate weight optimization experiment.

Also, the penalties use different calculation methods and scales, so their actual contributions to the weighted total may differ.

The same objective function should be used when comparing GA with the other optimization algorithms to ensure a fair comparison.

### Selection Method: Tournament Selection

We chose Tournament Selection because it is simple to implement and allows us to compare schedules directly using their penalty values.

The function randomly selects `k` schedules from the population, compares their weighted penalties, and returns the schedule with the lowest penalty.

**Initial Test (Small Dataset):**

- Population Size: 10
- Tournament Size (k): 3
- Random Seed for Selection: 42
- Candidate Penalties: 388.0, 392.0, 326.0
- Selected Parent Penalty: 326.0

The test was successful. The function selected the schedule with the lowest penalty among the three candidates.

The selected parent does not have to be the best schedule in the entire population.

We later compared tournament sizes k = 2 and k = 3 during the complete GA parameter tuning experiments.

**Second Test (k = 2):**

- Population Size: 10
- Tournament Size (k): 2
- Random Seed for Selection: 42
- Candidate Penalties: 388.0, 392.0
- Selected Parent Penalty: 388.0

The second test was also successful. The function selected the schedule with the lowest penalty among the two candidates.

Both initial tests confirmed that Tournament Selection worked correctly, but these tests alone were not enough to determine the better tournament size. We later compared k = 2 and k = 3 during GA parameter tuning and selected k = 3 based on the lower average final penalty.

### One-Point Crossover

We implemented `one_point_crossover()` to create a child schedule using assignments from two parent schedules.

The function selects a random crossover point and combines the assignments from both parents.

**Initial Test (Small Dataset):**
- Parent 1 Penalty: 388.0
- Parent 2 Penalty: 326.0
- Crossover Point: 4
- Child Exams: 10
- Child Schedule: Invalid
- Hard Constraint Violations: 7 (6 H1 violations and 1 H2 violation)

The test showed that combining two valid schedules can produce an invalid child. Therefore, the child must be validated before it can be accepted into the population.

To handle invalid children produced by crossover, we implemented the parent-based repair method described in the next section.

### Crossover Repair

We implemented `repair_child()` to handle invalid schedules produced by One-Point Crossover.

The repair function starts with a valid copy of Parent 1 and tries to apply assignments from the child. If an assignment causes a hard constraint violation, the function restores the original assignment from Parent 1.

**Initial Repair Test (Small Dataset):**
- Child Before Repair: Invalid
- Hard Constraint Violations Before Repair: 7
- Child After Repair: Valid
- Changes Compared to Parent 1: 2
- Repaired Child Penalty: 388.0
- Parent 1 Penalty: 388.0

The repair test was successful. The repaired child satisfies all hard constraints and differs from Parent 1 in two exam assignments.

However, the repaired child's penalty did not improve in this initial test. We later evaluated the complete GA, including crossover and repair, through parameter tuning experiments. These experiments did not measure the effect of repair separately.

### Swap Mutation

We implemented `swap_mutation()` to introduce changes into exam schedules.

The function attempts to swap the time slot and room assignments of two exams. Each swap is checked using `validate_schedule()`. Invalid swaps are rejected to maintain the hard constraints.

If no valid swap is found, the original schedule is returned.

**Initial Test (Small Dataset):**
- Schedule After Repair: Valid
- Penalty Before Mutation: 388.0
- Schedule After Mutation: Valid
- Changed Exam Assignments: 2
- Penalty After Mutation: 384.0
- Penalty Improvement: 4.0

The initial test was successful. Mutation produced a valid schedule with two changed assignments and a lower penalty.

However, one successful test does not guarantee that mutation will always improve the schedule. We later tested mutation rates of 0.1, 0.3, and 0.5 during GA parameter tuning and selected 0.5 based on the lowest average final penalty.

### Complete GA – Initial Test

We implemented `run_ga()` to combine selection, crossover, repair, and mutation over multiple generations.

The algorithm tracks the best valid schedule found during execution.

**Initial Test (Small Dataset):**
- Population Size: 10
- Generations: 3
- Tournament Size: 2
- Crossover Rate: 1.0
- Mutation Rate: 1.0
- Random Seed: 42
- Initial Best Penalty: 316.0
- Final Best Penalty: 312.0
- Improvement: 4.0 (approximately 1.27%)
- Convergence History: [316.0, 312.0, 312.0, 312.0]
- Final Schedule: Valid

The initial test was successful. GA improved the best penalty while satisfying all hard constraints.

These parameters were used for the initial test only. We later performed 36 parameter tuning experiments on the Small dataset and three additional experiments to evaluate the selected parameter combination. The results and final selected settings are documented in the following sections.

### GA Implementation and Experiment Workflow

After testing the GA operations separately, we connected them using the `run_ga()` function in `ga.py`.

The function starts by creating an initial population of valid exam schedules.

For each generation, the algorithm performs the following steps:

1. **Selection:** Selects two parents using Tournament Selection.
2. **Crossover:** Combines the parents using One-Point Crossover based on the crossover rate.
3. **Repair:** Checks the assignments from crossover and restores invalid changes using Parent 1.
4. **Mutation:** Attempts to swap exam assignments based on the mutation rate.
5. **Validation:** Checks that each new schedule satisfies all hard constraints.
6. **Population Update:** Creates a new population for the next generation.

The algorithm evaluates the schedules and tracks the best solution found during execution.

The `history` list stores the best penalty found so far, including the initial population and each generation.

The best solution is saved separately, but it is not automatically added to the next generation. Therefore, elitism is not currently used.

### GA Experiment Preparation

We added functions in `ga.py` to test different GA parameters and save their results.

- **prepare_experiments():** Prepares different values for one parameter while keeping the other parameters fixed.
- **add_seeds():** Repeats each experiment using different random seeds.
- **run_one_experiment():** Runs GA with the given settings and measures its execution time.
- **run_and_save_experiment():** Runs an experiment, evaluates the final solution, and saves its results.
- **save_experiment():** Appends the experiment results to a CSV file without deleting previous results.

The experiment results are stored in `results/ga_small_experiments.csv`.

For each experiment, we save the parameter values, initial and final penalties, execution time, hard constraint violations, individual soft penalties (P1–P4), convergence history, and best schedule.

This allows us to compare different configurations and select suitable GA parameters based on the experimental results.


### GA Parameter Tuning – Small Dataset

After implementing and testing the complete Genetic Algorithm, we performed parameter tuning on the Small dataset.

The goal was to find suitable GA settings that produce lower soft penalties while satisfying all hard constraints.

We tested five GA parameters: population size, tournament size, number of generations, crossover rate, and mutation rate.

We changed one parameter at a time while keeping the other parameters fixed. Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **36 experiments** using 12 unique parameter configurations.

**Initial reference settings:**

| Parameter | Value |
|---|---:|
| Population Size | 10 |
| Generations | 3 |
| Tournament Size (k) | 2 |
| Crossover Rate | 1.0 |
| Mutation Rate | 1.0 |

These values were used as a reference for the parameter tuning experiments, not as the final GA settings.

#### Parameter Tuning Results

We compared the average final penalty and average execution time for each tested value.

A lower average penalty indicates better solution quality.

| Parameter | Tested Value | Average Final Penalty | Average Runtime (s) |
|---|---:|---:|---:|
| Population Size | 10 | 309.33 | 0.0244 |
| | 20 | 296.00 | 0.0654 |
| | 40 | 282.00 | 0.1028 |
| Tournament Size (k) | 2 | 309.33 | 0.0244 |
| | 3 | 290.67 | 0.0299 |
| Generations | 10 | 292.67 | 0.0738 |
| | 30 | 282.00 | 0.2154 |
| | 50 | 280.67 | 0.3646 |
| Crossover Rate | 0.6 | 296.00 | 0.0222 |
| | 0.8 | 302.67 | 0.0227 |
| | 1.0 | 309.33 | 0.0244 |
| Mutation Rate | 0.1 | 315.33 | 0.0229 |
| | 0.3 | 308.67 | 0.0234 |
| | 0.5 | 295.33 | 0.0239 |

#### Parameter Selection

Based on the average final penalties, we selected the following parameter values for a combined test:

| Parameter | Selected Value |
|---|---:|
| Population Size | 40 |
| Tournament Size (k) | 3 |
| Generations | 50 |
| Crossover Rate | 0.6 |
| Mutation Rate | 0.5 |

**Reasons for selection:**

- **Population Size = 40:** Produced the lowest average penalty among the tested population sizes.
- **Tournament Size = 3:** Achieved a lower average penalty than k = 2.
- **Generations = 50:** Produced the lowest average penalty among the tested generation counts. However, 30 generations had a similar result with a shorter runtime.
- **Crossover Rate = 0.6:** Produced the lowest average penalty among the tested crossover rates.
- **Mutation Rate = 0.5:** Produced the lowest average penalty among the tested mutation rates.

These values were selected based mainly on solution quality. Execution time was also recorded to evaluate the performance trade-offs.

Because each parameter was tested separately, the selected values needed to be tested together before final evaluation.

All 36 parameter tuning experiments produced valid final schedules with zero hard constraint violations.


### Final Selected GA Settings – Small Dataset

After completing the 36 parameter tuning experiments, we selected the parameter values that produced the lowest average penalties in their individual tests.

We then tested the selected parameters together to evaluate their combined performance.

#### Selected Parameters

| Parameter | Selected Value |
|---|---:|
| Population Size | 40 |
| Generations | 50 |
| Tournament Size (k) | 3 |
| Crossover Rate | 0.6 |
| Mutation Rate | 0.5 |

We ran the GA three times using random seeds 42, 43, and 44.

#### Final Experiment Results

| Seed | Initial Best | Final Best | Runtime (s) | Hard Violations |
|---|---:|---:|---:|---:|
| 42 | 300.0 | 276.0 | 1.076945 | 0 |
| 43 | 300.0 | 270.0 | 1.085487 | 0 |
| 44 | 300.0 | 272.0 | 1.054583 | 0 |

#### Performance Summary

- **Average Initial Penalty:** 300.00
- **Average Final Penalty:** 272.67
- **Best Penalty:** 270.00
- **Worst Final Penalty:** 276.00
- **Average Execution Time:** 1.0723 seconds
- **Standard Deviation of Final Penalties (Sample):** 3.06
- **Average Penalty Improvement:** 27.33 points (9.11%)
- **Hard Constraint Violations:** 0 in all three runs

#### Convergence and Stability

The GA improved the initial best penalty in all three runs.

The convergence history shows that the best penalty decreased during the early generations and then remained stable.

The final penalties ranged from 270.0 to 276.0, showing relatively small variation across the three runs. However, three runs are not enough to make a strong general claim about stability, and the consecutive seeds produced overlapping initial populations.

#### Conclusion

The combined experiment was successful. All final schedules satisfied the hard constraints, and the GA reduced the soft penalty in every run.

Based on the parameter tuning experiments and the combined test, we selected the following GA configuration for the Small dataset:

**Population Size = 40, Generations = 50, Tournament Size = 3, Crossover Rate = 0.6, and Mutation Rate = 0.5.**

These parameters were selected based mainly on solution quality among the tested configurations. The selected settings do not guarantee a globally optimal exam schedule.

The final results and detailed convergence histories are stored in `results/ga_small_experiments.csv`.


### Additional GA Implementation Details

**Random Seeds and Reproducibility**

The `run_ga()` function uses a random seed to control the random operations during execution.

The initial population is generated using consecutive seeds, starting from the experiment seed (`seed + i`).

This allows us to reproduce experiments using the same settings and seed.

**Crossover and Mutation Conditions**

Crossover is applied according to the crossover rate. If crossover is not performed, the child is created as a copy of Parent 1.

Mutation is applied according to the mutation rate. The mutation function tries different pairs of exams and returns the first valid swap. If no valid swap is found, the original schedule is returned.

Therefore, applying mutation does not always mean that the schedule will change or improve.

**Best Solution Tracking**

After each generation, GA evaluates the new population and updates the best solution only when a lower penalty is found.

The algorithm keeps the best solution found during the entire run, even if that solution is no longer present in the current population.

However, the best solution is not automatically copied into the next generation. Therefore, the implementation does not use elitism.

**Experiment Results Storage**

Experiment results are appended to `results/ga_small_experiments.csv`, preserving previous experiments.

The saved information includes the GA settings, random seed, initial and final fitness values, execution time, hard constraint violations, individual soft penalties, convergence history, and best schedule.

Currently, the output filename is fixed for Small dataset experiments.

### GA Component Testing (ga_tests.py)

We created `ga_tests.py` to test the main Genetic Algorithm operations separately before evaluating the complete algorithm.

The tests use the Small dataset.

The file performs the following tests:

1. **Population Generation:** Generates 10 exam schedules and calculates their weighted penalties.
2. **Tournament Selection:** Selects two parents using tournament size k = 2 and evaluates their penalties.
3. **One-Point Crossover:** Creates a child from the selected parents and checks whether the child satisfies the hard constraints.
4. **Crossover Repair:** Repairs the child using Parent 1, validates the repaired schedule, and counts the changed exam assignments.
5. **Swap Mutation:** Attempts to modify the repaired schedule, checks its validity, and evaluates its penalty.

The tests print their results for manual inspection. They do not use automated assertions.

This file is used to test individual GA operations. The complete GA execution and parameter tuning experiments are handled separately in `ga.py`.


The final parameter combination was tested separately using `ga_best_test.py`.

This script loads the Small dataset and runs three experiments with the selected settings and different random seeds.

The results are appended to the same CSV file, with a blank row separating them from the previous parameter tuning experiments.


### GA Parameter Tuning – Medium Dataset

After completing the Small dataset experiments, we applied the same Genetic Algorithm to the Medium dataset without changing its core logic.

We created `ga_medium_experiments.py` to run the experiments and save the results separately.

The Medium dataset contains 40 exams, 100 students, 6 rooms, and 30 timeslots.

#### Experimental Setup

We used the same parameter tuning approach as the Small dataset.

We changed one parameter at a time while keeping the other parameters fixed.

**Reference settings:**

| Parameter | Value |
|---|---:|
| Population Size | 10 |
| Generations | 3 |
| Tournament Size (k) | 2 |
| Crossover Rate | 1.0 |
| Mutation Rate | 1.0 |

**Tested parameter values:**

| Parameter | Tested Values |
|---|---|
| Population Size | 10, 20, 40 |
| Generations | 10, 30, 50 |
| Tournament Size (k) | 2, 3 |
| Crossover Rate | 0.6, 0.8, 1.0 |
| Mutation Rate | 0.1, 0.3, 0.5 |

Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **36 experiments using 12 unique parameter configurations**.

For each experiment, we recorded the initial and final fitness values, execution time, hard constraint violations, individual soft penalties (P1–P4), convergence history, and best schedule.

All results were saved in `results/ga_medium_experiments.csv` without modifying the Small dataset results.

#### Medium Parameter Tuning Results

We compared the average final fitness and average execution time for each tested parameter value.

A lower fitness value indicates a better exam schedule.

| Parameter | Tested Value | Average Final Fitness | Average Runtime (s) |
|---|---:|---:|---:|
| Population Size | 10 | 510.67 | 0.1102 |
| | 20 | 484.67 | 0.2064 |
| | 40 | 493.33 | 0.3990 |
| Tournament Size (k) | 2 | 510.67 | 0.1102 |
| | 3 | 517.33 | 0.1092 |
| Generations | 10 | 477.33 | 0.2907 |
| | 30 | 447.00 | 0.9217 |
| | 50 | 395.33 | 1.5377 |
| Crossover Rate | 0.6 | 521.33 | 0.0902 |
| | 0.8 | 514.33 | 0.0920 |
| | 1.0 | 510.67 | 0.1102 |
| Mutation Rate | 0.1 | 523.00 | 0.1011 |
| | 0.3 | 529.67 | 0.1037 |
| | 0.5 | 520.33 | 0.1053 |
| | 1.0 (Reference) | 510.67 | 0.1102 |

#### Analysis of Parameter Tuning

Based on the average final fitness values:

- **Population Size = 20** achieved the lowest average fitness among the tested population sizes.
- **Tournament Size = 2** performed better than k = 3.
- **Generations = 50** produced the lowest average fitness, but required more execution time.
- **Crossover Rate = 1.0** achieved the lowest average fitness among the tested crossover rates.
- **Mutation Rate = 0.5** was the best among the three mutation rates tested during tuning. However, the reference value of 1.0 achieved an even lower average fitness.

All 36 experiments produced valid schedules with zero hard constraint violations.

These results evaluate one parameter at a time. Therefore, selecting the best value for each parameter does not guarantee that their combination will produce the best overall performance.

#### Final Parameter Comparison – Medium Dataset

After analyzing the 36 parameter tuning experiments, we selected the following combination for an additional test:

- Population Size = 20
- Generations = 50
- Tournament Size (k) = 2
- Crossover Rate = 1.0
- Mutation Rate = 1.0

We tested this combination using random seeds 42, 43, and 44.

**Combined Test Results:**

| Seed | Initial Fitness | Final Fitness | Runtime (s) | Hard Violations |
|---|---:|---:|---:|---:|
| 42 | 528 | 391 | 4.287 | 0 |
| 43 | 528 | 420 | 3.960 | 0 |
| 44 | 528 | 382 | 4.094 | 0 |

**Performance Summary:**

- Average Final Fitness: **397.67**
- Average Runtime: **4.113 seconds**
- Best Final Fitness: **382**
- Worst Final Fitness: **420**
- Sample Standard Deviation: **19.86**
- Hard Constraint Violations: **0 in all runs**

#### Comparison with a Previous Configuration

We compared the combined test results with a configuration already evaluated during the 36 parameter tuning experiments.

Both configurations used 50 generations, tournament size 2, crossover rate 1.0, and mutation rate 1.0. The only difference was the population size.

| Metric | Population = 10 | Population = 20 |
|---|---:|---:|
| Average Final Fitness | **395.33** | 397.67 |
| Average Runtime (s) | **1.5377** | 4.113 |
| Sample Standard Deviation | 28.92 | **19.86** |
| Hard Constraint Violations | 0 | 0 |

The configuration with population size 10 achieved a slightly lower average fitness and required less execution time.

The configuration with population size 20 showed lower variation between its final fitness values.

Because the configuration with population size 10 had already been tested using the same three seeds, we reused its recorded results without repeating the experiments.

#### Final Selected GA Settings – Medium Dataset

Based on the available experiments, we selected:

| Parameter | Final Value |
|---|---:|
| Population Size | 10 |
| Generations | 50 |
| Tournament Size (k) | 2 |
| Crossover Rate | 1.0 |
| Mutation Rate | 1.0 |

We selected this configuration because it achieved a slightly lower average final fitness with substantially shorter execution time than the combined configuration with population size 20.

However, the population size 20 configuration showed better stability across the three runs. Therefore, the selected settings represent our preferred trade-off between solution quality and runtime, rather than a proven global optimum.

All 39 Medium experiments produced valid final schedules with zero hard constraint violations.

The results are stored in `results/ga_medium_experiments.csv`.

### GA Parameter Tuning – Large Dataset

After completing the Medium dataset experiments, we applied the same Genetic Algorithm to the Large dataset without changing its core logic.

We created `ga_large_experiments.py` to run the experiments and save the results separately from Small and Medium.

The Large dataset contains 100 exams, 300 students, 12 rooms, and 80 timeslots.

#### Experimental Setup

We used the same parameter tuning approach as the Small and Medium datasets.

We changed one parameter at a time while keeping the other parameters fixed.

**Reference settings:**

| Parameter | Value |
|---|---:|
| Population Size | 10 |
| Generations | 3 |
| Tournament Size (k) | 2 |
| Crossover Rate | 1.0 |
| Mutation Rate | 1.0 |

**Tested parameter values:**

| Parameter | Tested Values |
|---|---|
| Population Size | 10, 20, 40 |
| Generations | 10, 30, 50 |
| Tournament Size (k) | 2, 3 |
| Crossover Rate | 0.6, 0.8, 1.0 |
| Mutation Rate | 0.1, 0.3, 0.5 |

Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **36 experiments using 12 unique parameter configurations**.

For each experiment, we recorded the initial and final fitness values, execution time, hard constraint violations, individual soft penalties (P1–P4), convergence history, and best schedule.

All results were saved in `results/ga_large_experiments.csv` without modifying the Small or Medium dataset results.

#### Large Parameter Tuning Results

We compared the average final fitness and average execution time for each tested parameter value.

A lower fitness value indicates a better exam schedule.

| Parameter | Tested Value | Average Final Fitness | Average Runtime (s) |
|---|---:|---:|---:|
| Population Size | 10 | 880.00 | 0.820 |
| | 20 | 860.00 | 1.660 |
| | 40 | 858.67 | 3.276 |
| Tournament Size (k) | 2 | 880.00 | 0.820 |
| | 3 | 867.67 | 0.876 |
| Generations | 10 | 853.67 | 2.146 |
| | 30 | 788.67 | 6.010 |
| | 50 | 710.33 | 9.846 |
| Crossover Rate | 0.6 | 880.33 | 0.656 |
| | 0.8 | 885.33 | 0.740 |
| | 1.0 | 880.00 | 0.820 |
| Mutation Rate | 0.1 | 890.33 | 0.802 |
| | 0.3 | 876.67 | 0.817 |
| | 0.5 | 888.33 | 0.807 |
| | 1.0 (Reference) | 880.00 | 0.820 |

#### Analysis of Parameter Tuning

Based on the average final fitness values:

- **Population Size = 40:** Produced the lowest average fitness among the tested population sizes. However, the improvement over population size 20 was small, while execution time was almost twice as long.
- **Tournament Size = 3:** Achieved a lower average fitness than k = 2.
- **Generations = 50:** Produced the lowest average fitness among the tested generation counts, but required more execution time.
- **Crossover Rate = 1.0:** Achieved the lowest average fitness among the tested crossover rates, with only a small improvement over 0.6.
- **Mutation Rate = 0.3:** Achieved the lowest average fitness among the tested mutation rates, including the reference value of 1.0.

All 36 experiments produced valid final schedules with zero hard constraint violations.

These results were obtained by changing one parameter at a time while keeping the others fixed. Therefore, the best individual parameter values needed to be tested together before selecting the final configuration.

#### Final Parameter Comparison – Large Dataset

After analyzing the 36 parameter tuning experiments, we selected the following parameter combination for an additional test:

| Parameter | Selected Value |
|---|---:|
| Population Size | 40 |
| Generations | 50 |
| Tournament Size (k) | 3 |
| Crossover Rate | 1.0 |
| Mutation Rate | 0.3 |

We tested this combination using random seeds 42, 43, and 44.

**Combined Test Results:**

| Seed | Initial Fitness | Final Fitness | Runtime (s) | Hard Violations |
|---|---:|---:|---:|---:|
| 42 | 901 | 599 | 31.331 | 0 |
| 43 | 901 | 576 | 31.039 | 0 |
| 44 | 901 | 586 | 30.912 | 0 |

**Performance Summary:**

- Average Initial Fitness: **901.00**
- Average Final Fitness: **587.00**
- Best Final Fitness: **576.00**
- Worst Final Fitness: **599.00**
- Average Runtime: **31.094 seconds**
- Sample Standard Deviation: **11.53**
- Average Fitness Improvement: **314 points (34.85%)**
- Hard Constraint Violations: **0 in all three runs**

The combined configuration improved the fitness in all three runs while satisfying all hard constraints.

#### Comparison with a Previous Configuration

We compared the new combination with the best-performing configuration from the previous 36 parameter tuning experiments.

The previous configuration had already been tested using the same three random seeds, so we reused its recorded results without repeating the experiments.

| Parameter | Previous Configuration | New Configuration |
|---|---:|---:|
| Population Size | 10 | 40 |
| Generations | 50 | 50 |
| Tournament Size (k) | 2 | 3 |
| Crossover Rate | 1.0 | 1.0 |
| Mutation Rate | 1.0 | 0.3 |

**Performance Comparison:**

| Metric | Previous | New |
|---|---:|---:|
| Average Final Fitness | 710.33 | **587.00** |
| Best Final Fitness | 705 | **576** |
| Average Runtime (s) | **9.846** | 31.094 |
| Sample Standard Deviation | **4.73** | 11.53 |
| Hard Constraint Violations | 0 | 0 |

The new configuration reduced the average final fitness by approximately **17.36%** compared with the previous configuration.

However, it required more execution time and showed greater variation between the three runs.

The previous configuration was faster and had lower variation, while the new configuration achieved substantially better solution quality.

#### Final Selected GA Settings – Large Dataset

Based on the experimental results, we selected the following configuration for the Large dataset:

| Parameter | Final Value |
|---|---:|
| Population Size | 40 |
| Generations | 50 |
| Tournament Size (k) | 3 |
| Crossover Rate | 1.0 |
| Mutation Rate | 0.3 |

We selected this configuration because our main objective was to minimize soft constraint penalties while satisfying all hard constraints.

The improvement in solution quality was considered more important than the additional execution time.

However, these settings represent the best-performing configuration among the tested alternatives in terms of average fitness, not a proven global optimum. The stability comparison is also limited to three runs per configuration.

All **39 Large experiments** produced valid final schedules with zero hard constraint violations.

The results and convergence histories are stored in `results/ga_large_experiments.csv`.


## Ant Colony Optimization (ACO)

### ACO Parameter Tuning – Small Dataset

We tested different ACO parameters on the Small dataset.
Each configuration was tested with three random seeds: 42, 43, and 44.

We compared the average fitness, execution time, and stability
to select suitable parameters.

### Selected ACO Parameters

| Parameter | Value |
|---|---:|
| Number of Ants | 5 |
| Number of Iterations | 10 |
| Alpha | 1 |
| Beta | 3 |
| Evaporation Rate | 0.2 |
| Q | 2 |

The selected settings achieved an average fitness of 274.67
and an average execution time of about 0.0208 seconds.

Using 20 ants with beta = 3 improved the average fitness
to 271.33, but increased the execution time to about
0.0842 seconds.

We selected 5 ants with beta = 3 because they provided
a good balance between solution quality and execution time.
All three runs satisfied the hard constraints.

### ACO Implementation

The Ant Colony Optimization (ACO) algorithm builds exam schedules
using a group of ants.

Each ant assigns exams to valid timeslots and rooms while
respecting the hard constraints.

The assignment choices depend on two values:
- Pheromone (tau): Information learned from previous iterations.
- Heuristic (eta): An estimate of how suitable an assignment is.

After constructing the schedules, the algorithm calculates
their fitness using the shared fitness function.

At the end of each iteration, pheromone values are reduced
through evaporation and increased based on successful schedules.

The algorithm keeps the best schedule and records its
fitness history to study convergence.

### Heuristic Information (Eta)

The heuristic helps each ant choose a suitable timeslot while
building a schedule.

We estimate the soft penalty cost using:
- P1: Students who have other exams on the same day.
- P2: Exams in consecutive periods.
- P3: Number of exams already assigned to the same day.
- P4: Exams on consecutive days.

Estimated Cost = 3 * same_day_students + P2 + 2 * daily_count + 4 * P4

Eta = 1 / (1 + Estimated Cost)

A lower estimated cost gives a higher heuristic value.

This is an estimate for a partial schedule, not the final fitness.
Hard constraints are checked separately when finding feasible assignments.

### Assignment Selection

Each ant selects an assignment using pheromone and heuristic values.

Weight = (Pheromone ^ Alpha) * (Heuristic ^ Beta)

Alpha controls the influence of pheromone, while Beta controls
the influence of heuristic information.

Assignments with higher weights have a greater chance of
being selected.

We use weighted random selection to allow different
solutions to be explored.



### ACO Parameter Tuning – Medium Dataset

We tested different ACO parameters on the Medium dataset.
Each configuration was tested using three random seeds: 42, 43, and 44.

We performed 39 parameter tuning experiments and 3 additional
experiments for the selected parameter combination.

### Selected ACO Parameters – Medium

| Parameter | Value |
|---|---:|
| Number of Ants | 20 |
| Number of Iterations | 10 |
| Alpha | 1 |
| Beta | 3 |
| Evaporation Rate | 0.2 |
| Q | 2 |

The selected settings achieved an average fitness of 345.33
and an average execution time of 4.081 seconds.

Using 5 ants with beta = 3 gave an average fitness of 353.67
and an average execution time of 1.025 seconds.

We selected 20 ants because they produced better average fitness
and more stable results across the three seeds, although
the execution time was higher.

All three runs of the selected settings satisfied the hard constraints.

### ACO Parameter Tuning – Large Dataset

We tested different ACO parameters on the Large dataset.
Each configuration was tested using three random seeds: 42, 43, and 44.

We performed 39 experiments using 13 different parameter settings.

We compared the average fitness, execution time, and stability
to select suitable parameters for the Large dataset.

### Selected ACO Parameters – Large

| Parameter | Value |
|---|---:|
| Number of Ants | 5 |
| Number of Iterations | 10 |
| Alpha | 1 |
| Beta | 3 |
| Evaporation Rate | 0.2 |
| Q | 2 |

The selected settings achieved an average fitness of 431.33
and an average execution time of 39.43 seconds.

Increasing the number of ants or iterations improved the fitness,
but also increased the execution time significantly.

Using beta = 3 provided a better average fitness without
a large increase in execution time.

We selected these settings because they provided a good balance
between solution quality and execution time.

All three runs satisfied the hard constraints.



## Particle Swarm Optimization (PSO)

### Swarm Initialization

We implemented Particle Swarm Optimization (PSO) in `pso.py` to improve exam schedules by minimizing soft constraint penalties while satisfying all hard constraints.

We created a function called `initialize_swarm()` to generate the initial swarm.

Each particle represents a complete exam schedule and stores:

- **position:** The current exam schedule.
- **velocity:** A list of assignment changes.
- **pbest:** The best schedule found by the particle.
- **pbest_fitness:** The weighted penalty of the particle's best schedule.

The function uses `create_random_solution()` from `main.py` to generate valid schedules.

Each particle starts with an empty velocity. Its initial personal best is a copy of its current position.

We use consecutive random seeds (`seed + i`) to generate the initial particles reproducibly.

### Global Best Initialization

We created a function called `initialize_gbest()` in `pso.py` to find the best initial solution in the swarm.

The function compares the `pbest_fitness` values of all particles and selects the particle with the lowest penalty.

It returns:

- **gbest:** A copy of the best schedule found in the swarm.
- **gbest_fitness:** The weighted penalty of that schedule.

This gives the swarm an initial global best solution before starting the optimization iterations.

### Velocity Update

We created a function called `update_velocity()` in `pso.py` to update the velocity of each particle.

Since exam scheduling is a discrete problem, velocity is represented as a list of assignment changes rather than numerical values.

Each change contains an exam ID and a target assignment (timeslot and room).

The function uses three parameters:

- **w (Inertia Weight):** Controls how many previous velocity changes are kept.
- **c1 (Cognitive Coefficient):** Controls the influence of the particle's personal best solution (pbest).
- **c2 (Social Coefficient):** Controls the influence of the global best solution (gbest).

The function first keeps previous changes with probability `w`.

It then compares the current schedule with pbest and gbest. When an exam assignment is different, the function may add a change toward the corresponding best solution.

The probabilities used for these changes are `c1 / (1 + c1)` and `c2 / (1 + c2)`.

Random values are used to decide which changes are added to the new velocity.

### Position Update

We created a function called `update_position()` in `pso.py` to apply the velocity changes to the current exam schedule.

The function starts with a copy of the current schedule and processes each proposed assignment change.

For each change:

1. It assigns the exam to the proposed timeslot and room.
2. It uses `validate_schedule()` to check the hard constraints.
3. If the new assignment is valid, the change is kept.
4. If the assignment is invalid, the function restores the original assignment and tries to swap assignments with another exam occupying the target timeslot and room.
5. If the swap is also invalid or no matching exam is found, the original assignment is kept.

This allows particles to explore different schedules while keeping all hard constraints satisfied.

A position update does not always improve the fitness. The updated schedule is evaluated separately during the optimization process.

### Personal Best Update

We created a function called `update_pbest()` in `pso.py` to update the personal best solution of each particle.

The function evaluates the particle's current schedule using `calculate_soft_penalties()` from `main.py`.

It compares the current weighted penalty with `pbest_fitness`.

If the current penalty is lower, the function:

- Saves a copy of the current schedule as the new `pbest`.
- Updates `pbest_fitness` with the new penalty value.

Otherwise, the previous personal best is kept.

This allows each particle to remember its best solution found during the optimization process.

### PSO Implementation and Optimization Loop

We created a function called `run_pso()` in `pso.py` to connect all PSO operations and run the optimization process.

The function starts by initializing the swarm and selecting the initial global best solution.

For each iteration, the algorithm performs the following steps:

1. **Velocity Update:** Updates each particle's velocity using its previous velocity, personal best, and global best.
2. **Position Update:** Applies the proposed assignment changes while maintaining the hard constraints.
3. **Personal Best Update:** Evaluates the updated schedule and updates pbest if a better solution is found.
4. **Global Best Update:** Selects the best personal best solution among all particles.
5. **History Tracking:** Records the global best fitness after each iteration.

The `history` list includes the initial global best fitness and the best fitness after each iteration.

At the end, the function returns the best schedule, its weighted fitness, and the convergence history.

### PSO Initial Test – Small Dataset

After implementing the complete PSO algorithm, we performed an initial test on the Small dataset to check that the algorithm works correctly.

**Initial Test Settings:**

- Number of Particles: 5
- Number of Iterations: 20
- Inertia Weight (w): 0.5
- Cognitive Coefficient (c1): 1
- Social Coefficient (c2): 2
- Random Seed: 42

**Initial Test Results:**

- Number of Exams: 10
- Initial Best Fitness: 316.0
- Final Best Fitness: 284.0
- Fitness Improvement: 32.0 (approximately 10.13%)
- Hard Constraint Violations: 0

The initial test was successful. PSO improved the best fitness while satisfying all hard constraints.

The convergence history showed that the best fitness did not increase during the optimization process.

These settings were used for the initial test only. We later performed parameter tuning experiments to select suitable PSO settings for each dataset size.

### PSO Experiment Preparation

After completing the initial PSO test, we created separate experiment files to evaluate different parameter settings on the Small, Medium, and Large datasets.

The experiment files are:

- `pso_small_experiments.py`
- `pso_medium_experiments.py`
- `pso_large_experiments.py`

We tested five PSO parameters: number of particles, number of iterations, inertia weight (w), cognitive coefficient (c1), and social coefficient (c2).

We changed one parameter at a time while keeping the other parameters fixed.

Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed 33 parameter tuning experiments for each dataset, using 11 unique configurations.

For each experiment, we recorded:

- Parameter values and random seed.
- Final best fitness.
- Execution time.
- Hard constraint violations.
- Convergence history.
- Best exam schedule.

The results were saved in separate CSV files for each dataset:

- `results/pso_small_experiments.csv`
- `results/pso_medium_experiments.csv`
- `results/pso_large_experiments.csv`

We also tested selected parameter combinations using additional experiments and compared their results with the previous configurations.

This allowed us to select suitable PSO settings based on solution quality, execution time, and stability.

### PSO Parameter Tuning – Small Dataset

After completing the initial PSO test, we performed parameter tuning on the Small dataset.

The goal was to find suitable PSO settings that minimize soft constraint penalties while satisfying all hard constraints.

We changed one parameter at a time while keeping the other parameters fixed. Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **33 experiments using 11 unique parameter configurations**.

#### Experimental Setup

**Reference settings:**

| Parameter | Value |
|---|---:|
| Number of Particles | 5 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.5 |
| Cognitive Coefficient (c1) | 1 |
| Social Coefficient (c2) | 2 |

**Tested parameter values:**

| Parameter | Tested Values |
|---|---|
| Number of Particles | 5, 10, 20 |
| Number of Iterations | 10, 20, 50 |
| Inertia Weight (w) | 0.2, 0.5, 0.8 |
| Cognitive Coefficient (c1) | 0.5, 1, 2 |
| Social Coefficient (c2) | 1, 2, 3 |

#### Parameter Tuning Results

We compared the average final fitness and average execution time for each tested value.

A lower fitness indicates a better exam schedule.

| Parameter | Tested Value | Average Final Fitness | Average Runtime (s) |
|---|---:|---:|---:|
| Number of Particles | 5 | 282.67 | 0.0173 |
| | 10 | 279.33 | 0.0325 |
| | 20 | 282.00 | 0.0764 |
| Number of Iterations | 10 | 293.33 | 0.0084 |
| | 20 | 282.67 | 0.0173 |
| | 50 | 282.67 | 0.0321 |
| Inertia Weight (w) | 0.2 | 288.67 | 0.0116 |
| | 0.5 | 282.67 | 0.0173 |
| | 0.8 | 278.67 | 0.0236 |
| Cognitive Coefficient (c1) | 0.5 | 292.00 | 0.0143 |
| | 1 | 282.67 | 0.0173 |
| | 2 | 294.00 | 0.0152 |
| Social Coefficient (c2) | 1 | 296.67 | 0.0128 |
| | 2 | 282.67 | 0.0173 |
| | 3 | 286.00 | 0.0158 |

#### Analysis of Parameter Tuning

Based on the experimental results:

- **Number of Particles = 10:** Produced the lowest average fitness among the tested particle counts.
- **Number of Iterations = 20:** Achieved the same average fitness as 50 iterations with a shorter execution time.
- **Inertia Weight = 0.8:** Produced a slightly lower average fitness than 0.5, but showed greater variation between runs.
- **Cognitive Coefficient (c1) = 1:** Produced the lowest average fitness among the tested c1 values.
- **Social Coefficient (c2) = 2:** Produced the lowest average fitness among the tested c2 values.

All 33 experiments recorded zero hard constraint violations.

Since each parameter was tested separately, the best individual values did not necessarily produce the best combined configuration.

#### Additional Combined Test

We tested the following combination using seeds 42, 43, and 44:

| Parameter | Value |
|---|---:|
| Number of Particles | 10 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.8 |
| Cognitive Coefficient (c1) | 1 |
| Social Coefficient (c2) | 2 |

**Combined Test Results:**

| Seed | Final Fitness | Runtime (s) | Hard Violations |
|---|---:|---:|---:|
| 42 | 290 | 0.0824 | 0 |
| 43 | 286 | 0.0692 | 0 |
| 44 | 286 | 0.1058 | 0 |

The combined configuration achieved an average final fitness of **287.33** and an average execution time of approximately **0.0858 seconds**.

#### Final Parameter Comparison

We compared the combined configuration with the previously tested configuration using 10 particles, 20 iterations, w = 0.5, c1 = 1, and c2 = 2.

| Metric | Previous Configuration | Combined Configuration |
|---|---:|---:|
| Average Final Fitness | **279.33** | 287.33 |
| Average Runtime (s) | **0.0325** | 0.0858 |
| Best Final Fitness | **274** | 286 |
| Fitness Range | 12 | **4** |
| Hard Violations | 0 | 0 |

The previous configuration achieved better average fitness and shorter execution time.

The combined configuration had a smaller fitness range, but its average solution quality was worse.

#### Final Selected PSO Settings – Small Dataset

Based on the available experiments, we selected:

| Parameter | Final Value |
|---|---:|
| Number of Particles | 10 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.5 |
| Cognitive Coefficient (c1) | 1 |
| Social Coefficient (c2) | 2 |

**Performance Summary:**

- Average Final Fitness: **279.33**
- Best Final Fitness: **274**
- Worst Final Fitness: **286**
- Average Runtime: **0.0325 seconds**
- Sample Standard Deviation: **6.11**
- Hard Constraint Violations: **0 in all three runs**

We selected this configuration because it provided better average solution quality and shorter execution time than the additional combined configuration.

These settings represent our preferred configuration among the tested alternatives, not a guaranteed global optimum.

The parameter tuning results are stored in `results/pso_small_experiments.csv`, and the additional combined test results are stored in `results/pso_small_combined_test.csv`.

### PSO Parameter Tuning – Medium Dataset

After completing the Small dataset experiments, we applied the same PSO algorithm to the Medium dataset without changing its core logic.

We created `pso_medium_experiments.py` to run the experiments and save the results separately.

The Medium dataset contains 40 exams, 100 students, 6 rooms, and 30 timeslots.

#### Experimental Setup

We used the same parameter tuning approach as the Small dataset.

We changed one parameter at a time while keeping the other parameters fixed.

**Reference settings:**

| Parameter | Value |
|---|---:|
| Number of Particles | 10 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.5 |
| Cognitive Coefficient (c1) | 1 |
| Social Coefficient (c2) | 2 |

**Tested parameter values:**

| Parameter | Tested Values |
|---|---|
| Number of Particles | 5, 10, 20 |
| Number of Iterations | 10, 20, 50 |
| Inertia Weight (w) | 0.2, 0.5, 0.8 |
| Cognitive Coefficient (c1) | 0.5, 1, 2 |
| Social Coefficient (c2) | 1, 2, 3 |

Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **33 experiments using 11 unique parameter configurations**.

#### Medium Parameter Tuning Results

We compared the average final fitness and average execution time for each tested parameter value.

A lower fitness value indicates a better exam schedule.

| Parameter | Tested Value | Average Final Fitness | Average Runtime (s) |
|---|---:|---:|---:|
| Number of Particles | 5 | 456.67 | 0.1569 |
| | 10 | 446.00 | 0.3066 |
| | 20 | 415.67 | 0.6129 |
| Number of Iterations | 10 | 464.33 | 0.2208 |
| | 20 | 446.00 | 0.3066 |
| | 50 | 440.33 | 0.4432 |
| Inertia Weight (w) | 0.2 | 464.00 | 0.2404 |
| | 0.5 | 446.00 | 0.3066 |
| | 0.8 | 436.67 | 0.6161 |
| Cognitive Coefficient (c1) | 0.5 | 454.67 | 0.2805 |
| | 1 | 446.00 | 0.3066 |
| | 2 | 434.00 | 0.3826 |
| Social Coefficient (c2) | 1 | 438.00 | 0.3276 |
| | 2 | 446.00 | 0.3066 |
| | 3 | 458.33 | 0.2868 |

#### Analysis of Parameter Tuning

Based on the average final fitness values:

- **Number of Particles = 20:** Produced the lowest average fitness among the tested particle counts, but required more execution time.
- **Number of Iterations = 50:** Achieved the lowest average fitness among the tested iteration counts. However, the improvement over 20 iterations was relatively small.
- **Inertia Weight = 0.8:** Produced the lowest average fitness among the tested w values.
- **Cognitive Coefficient (c1) = 2:** Achieved the lowest average fitness among the tested c1 values.
- **Social Coefficient (c2) = 1:** Produced the lowest average fitness among the tested c2 values.

All 33 parameter tuning experiments recorded zero hard constraint violations.

Since each parameter was tested separately, we needed to test the selected values together before making the final decision.

#### Additional Combined Test

We created `pso_medium_combined_test.py` to evaluate the selected parameter combination.

**Combined settings:**

| Parameter | Value |
|---|---:|
| Number of Particles | 20 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.8 |
| Cognitive Coefficient (c1) | 2 |
| Social Coefficient (c2) | 1 |

We used 20 iterations because increasing the count to 50 produced only a small improvement in the individual test while increasing execution time.

The combination was tested using random seeds 42, 43, and 44.

**Combined Test Results:**

| Seed | Final Fitness | Runtime (s) | Hard Violations |
|---|---:|---:|---:|
| 42 | 420 | 1.5210 | 0 |
| 43 | 404 | 1.2536 | 0 |
| 44 | 415 | 1.7010 | 0 |

**Performance Summary:**

- Average Final Fitness: **413.00**
- Best Final Fitness: **404**
- Worst Final Fitness: **420**
- Average Runtime: **1.4919 seconds**
- Sample Standard Deviation: **8.19**
- Hard Constraint Violations: **0 in all three runs**

#### Comparison with a Previous Configuration

We compared the combined configuration with the best configuration from the previous parameter tuning experiments.

The previous configuration used 20 particles, 20 iterations, w = 0.5, c1 = 1, and c2 = 2.

| Metric | Previous Configuration | Combined Configuration |
|---|---:|---:|
| Average Final Fitness | 415.67 | **413.00** |
| Best Final Fitness | **398** | 404 |
| Average Runtime (s) | **0.6129** | 1.4919 |
| Sample Standard Deviation | 18.01 | **8.19** |
| Fitness Range | 36 | **16** |
| Hard Violations | 0 | 0 |

The combined configuration achieved a slightly lower average fitness and showed less variation between the three runs.

However, it required more execution time. The previous configuration was faster and achieved a better individual fitness value.

The stability comparison is based on only three random seeds, so it does not guarantee the same behavior in other runs.

#### Final Selected PSO Settings – Medium Dataset

Based on the available results, we selected:

| Parameter | Final Value |
|---|---:|
| Number of Particles | 20 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.8 |
| Cognitive Coefficient (c1) | 2 |
| Social Coefficient (c2) | 1 |

We selected this configuration because it achieved a slightly better average fitness and lower variation across the three runs.

Although its execution time was higher, we prioritized solution quality and considered the improved consistency of the results.

These settings represent our preferred configuration among the tested alternatives, not a guaranteed global optimum.

All **36 Medium experiments** recorded zero hard constraint violations.

The parameter tuning results and the three additional combined experiments are stored in `results/pso_medium_experiments.csv`, with a blank row separating the two groups.

### PSO Parameter Tuning – Large Dataset

After completing the Medium dataset experiments, we applied the same PSO algorithm to the Large dataset without changing its core logic.

We created `pso_large_experiments.py` to run the experiments and save the results separately from Small and Medium.

The Large dataset contains 100 exams, 300 students, 12 rooms, and 80 timeslots.

#### Experimental Setup

We used the same parameter tuning approach as the Small and Medium datasets.

We changed one parameter at a time while keeping the other parameters fixed.

**Reference settings:**

| Parameter | Value |
|---|---:|
| Number of Particles | 10 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.5 |
| Cognitive Coefficient (c1) | 1 |
| Social Coefficient (c2) | 2 |

**Tested parameter values:**

| Parameter | Tested Values |
|---|---|
| Number of Particles | 5, 10, 20 |
| Number of Iterations | 10, 20, 50 |
| Inertia Weight (w) | 0.2, 0.5, 0.8 |
| Cognitive Coefficient (c1) | 0.5, 1, 2 |
| Social Coefficient (c2) | 1, 2, 3 |

Each configuration was tested using three random seeds: 42, 43, and 44.

After removing duplicate configurations, we performed **33 experiments using 11 unique parameter configurations**.

#### Large Parameter Tuning Results

We compared the average final fitness and average execution time for each tested parameter value.

A lower fitness value indicates a better exam schedule.

| Parameter | Tested Value | Average Final Fitness | Average Runtime (s) |
|---|---:|---:|---:|
| Number of Particles | 5 | 821.67 | 0.3858 |
| | 10 | 792.33 | 0.8189 |
| | 20 | 730.00 | 1.8583 |
| Number of Iterations | 10 | 803.00 | 0.7181 |
| | 20 | 792.33 | 0.8189 |
| | 50 | 792.33 | 1.0882 |
| Inertia Weight (w) | 0.2 | 775.67 | 0.6173 |
| | 0.5 | 792.33 | 0.8189 |
| | 0.8 | 741.00 | 1.7192 |
| Cognitive Coefficient (c1) | 0.5 | 809.67 | 0.7393 |
| | 1 | 792.33 | 0.8189 |
| | 2 | 760.67 | 0.8744 |
| Social Coefficient (c2) | 1 | 741.33 | 0.9072 |
| | 2 | 792.33 | 0.8189 |
| | 3 | 785.33 | 0.7975 |

#### Analysis of Parameter Tuning

Based on the average final fitness values:

- **Number of Particles = 20:** Produced the lowest average fitness among the tested particle counts, but required more execution time.
- **Number of Iterations = 20:** Achieved the same average fitness as 50 iterations with a shorter execution time under the reference settings.
- **Inertia Weight = 0.8:** Produced the lowest average fitness among the tested w values.
- **Cognitive Coefficient (c1) = 2:** Achieved the lowest average fitness among the tested c1 values.
- **Social Coefficient (c2) = 1:** Produced the lowest average fitness among the tested c2 values.

All 33 parameter tuning experiments recorded zero hard constraint violations.

Since each parameter was tested separately, we needed to test the selected values together before making the final decision.

#### Additional Combined Test

We created `pso_large_combined_test.py` to evaluate the selected parameter combination.

**Combined settings:**

| Parameter | Value |
|---|---:|
| Number of Particles | 20 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.8 |
| Cognitive Coefficient (c1) | 2 |
| Social Coefficient (c2) | 1 |

We selected 20 iterations because increasing the count to 50 did not improve the average fitness in the individual test under the reference settings, but increased execution time.

The combination was tested using random seeds 42, 43, and 44.

**Combined Test Results:**

| Seed | Final Fitness | Runtime (s) | Hard Violations |
|---|---:|---:|---:|
| 42 | 723 | 3.8958 | 0 |
| 43 | 686 | 4.2546 | 0 |
| 44 | 721 | 4.7748 | 0 |

**Performance Summary:**

- Average Final Fitness: **710.00**
- Best Final Fitness: **686**
- Worst Final Fitness: **723**
- Average Runtime: **4.3084 seconds**
- Sample Standard Deviation: **20.81**
- Hard Constraint Violations: **0 in all three runs**

#### Comparison with a Previous Configuration

We compared the combined configuration with the best configuration from the previous parameter tuning experiments based on average fitness.

The previous configuration used 20 particles, 20 iterations, w = 0.5, c1 = 1, and c2 = 2.

| Metric | Previous Configuration | Combined Configuration |
|---|---:|---:|
| Average Final Fitness | 730.00 | **710.00** |
| Best Final Fitness | 719 | **686** |
| Average Runtime (s) | **1.8583** | 4.3084 |
| Sample Standard Deviation | **16.52** | 20.81 |
| Fitness Range | **30** | 37 |
| Hard Violations | 0 | 0 |

The combined configuration reduced the average final fitness by approximately **2.74%** compared with the previous configuration.

However, it required more execution time and showed slightly greater variation between the three runs.

The previous configuration was faster and had lower variation, while the combined configuration achieved better average solution quality.

The stability comparison is limited to three random seeds.

#### Final Selected PSO Settings – Large Dataset

Based on the available results, we selected:

| Parameter | Final Value |
|---|---:|
| Number of Particles | 20 |
| Number of Iterations | 20 |
| Inertia Weight (w) | 0.8 |
| Cognitive Coefficient (c1) | 2 |
| Social Coefficient (c2) | 1 |

We selected this configuration because it achieved the lowest average final fitness among the tested configurations.

Although its execution time was higher and its results showed slightly more variation, we prioritized reducing soft constraint penalties while satisfying all hard constraints.

These settings represent our preferred configuration among the tested alternatives, not a guaranteed global optimum.

All **36 Large experiments** recorded zero hard constraint violations.

The parameter tuning results and the three additional combined experiments are stored in `results/pso_large_experiments.csv`, with a blank row separating the two groups.


## Dynamic Programming (DP)

### Overview

We implemented Dynamic Programming (DP) on the Small dataset to compare its results with the other algorithms.

The algorithm builds the exam schedule day by day. It explores valid daily assignments and uses memoization to avoid solving the same state more than once.

The goal is to find the schedule with the minimum weighted soft penalty while satisfying all hard constraints.

### State Representation

We represent each DP state using three values:

`(day_index, used_mask, previous_mask)`

- **day_index:** The current day being scheduled.
- **used_mask:** The exams already assigned to previous days.
- **previous_mask:** The exams scheduled on the previous day.

We use bitmasks to represent exam sets and reduce the size of the state representation.

The previous day's exams are needed to calculate the penalty for exams on consecutive days (P4).

### Daily Assignments and Hard Constraints

The `generate_daily_assignments()` function creates possible exam assignments for each day.

For the Small dataset, each day has two periods. The function allows empty periods, single exams, and pairs of exams without student conflicts.

After finding the best daily assignments, `reconstruct_schedule()` assigns available rooms with enough capacity.

The final schedule is checked using `validate_schedule()` from `main.py`.

### Fitness Calculation

The `calculate_daily_penalties()` function calculates the contribution of each day to the four soft penalties:

- **P1:** Students with multiple exams on the same day.
- **P2:** Pairs of exams in consecutive periods on the same day.
- **P3:** Uneven distribution of exams across days.
- **P4:** Pairs of student exams on consecutive days.

The same fitness function used by the other algorithms is applied:

**Fitness = 3 × P1 + P2 + P3 + 4 × P4**

For the Small dataset, the average number of exams per day is 2. Therefore, each day's contribution to P3 is calculated using `(daily_exam_count - 2) ** 2`.

### Recurrence and Memoization

The `run_dp()` function uses recursion with `lru_cache` for memoization.

For each state, it tries the valid daily assignments and calculates the current day's penalty plus the best cost for the remaining days.

The assignment with the minimum total cost is selected.

When all days have been processed, the function returns zero remaining cost if all exams are assigned. Otherwise, it returns infinity.

The algorithm stores the best assignments so the final schedule can be reconstructed.

### Experimental Results — Small Dataset

We tested DP on the Small dataset containing 10 exams, 30 students, 3 rooms, and 5 days.

| Metric | Result |
|---|---:|
| P1 | 20 |
| P2 | 20 |
| P3 | 2.0 |
| P4 | 44 |
| Best Fitness | 258.0 |
| Execution Time (s) | 8.0668 |
| DP States | 51,393 |
| Cache Hits | 976,330 |
| Cached States | 51,393 |
| Hard Constraint Violations | 0 |

The algorithm produced a valid schedule for all 10 exams. The final fitness calculated by `main.py` matched the DP result.

The memoization results also show that many previously calculated states were reused.

The results are saved in `results/dp_small_experiments.csv`, including the final exam schedule.

### Complexity and Limitations

The number of possible states depends on the number of exams and their assignments. In the worst case, the time and memory requirements can grow exponentially as the problem size increases.

Our implementation was designed specifically for the Small dataset, which has two exam periods per day.

We also examined the Medium dataset, which contains 40 exams and three periods per day. Supporting Medium would require generating more daily assignments and exploring a much larger number of states.

Therefore, we did not run this DP implementation on Medium or Large. This decision was based on the expected computational complexity, not on measured execution times for those datasets.

### How to Run

Run the following command from the project directory:

`python dp.py`

The program loads the Small dataset, runs DP, reconstructs the best schedule, validates it, and displays the fitness and performance results.

The results are saved in `results/dp_small_experiments.csv`.

DP does not use random seeds or parameter tuning in this implementation because the search is deterministic. The execution time may vary depending on the computer.


### Convergence and Visualization

Unlike GA, ACO, and PSO, our Dynamic Programming implementation does not use iterative generations or maintain a convergence history.

It uses memoization to solve states and find the minimum fitness for the Small dataset. Therefore, we did not generate an Iteration vs. Best Fitness curve for DP.

## Results Summary

We tested GA, ACO, and PSO on Small, Medium, and Large datasets.

The table shows the average final fitness using the selected settings for each algorithm.

| Algorithm | Small | Medium | Large |
|---|---:|---:|---:|
| GA | 272.67 | 395.33 | 587.00 |
| ACO | 274.67 | 345.33 | 431.33 |
| PSO | 279.33 | 413.00 | 710.00 |

We also tested DP on the Small dataset. It achieved a fitness of 258.00.

The results show that the algorithms performed differently depending on the dataset size.

We also compared execution time and the variation between runs when selecting the final settings.

All recorded final schedules satisfied the hard constraints.