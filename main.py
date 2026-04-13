import random

# -------- Algorithms --------
def fcfs(processes, arrival):
    return [p for p, _ in sorted(zip(processes, arrival), key=lambda x: x[1])]

def sjf(processes, arrival, burst):
    n = len(processes)
    completed = [False] * n
    time_now = 0
    order = []

    while len(order) < n:
        idx = -1
        min_bt = float('inf')
        for i in range(n):
            if arrival[i] <= time_now and not completed[i]:
                if burst[i] < min_bt:
                    min_bt = burst[i]
                    idx = i

        if idx == -1:
            time_now += 1
        else:
            order.append(processes[idx])
            time_now += burst[idx]
            completed[idx] = True

    return order

def priority_sched(processes, arrival, burst, priority):
    combined = list(zip(processes, arrival, burst, priority))
    combined.sort(key=lambda x: (x[1], x[3]))
    return [p for p, _, _, _ in combined]

def round_robin(processes, burst, tq):
    rem = burst[:]
    queue = list(range(len(processes)))
    order = []

    while queue:
        i = queue.pop(0)
        if rem[i] > 0:
            order.append(processes[i])
            if rem[i] > tq:
                rem[i] -= tq
                queue.append(i)
            else:
                rem[i] = 0
    return order


# -------- Gantt Chart --------
def print_gantt(order, processes, arrival, burst):
    time_now = 0

    # Fix start time
    if order:
        first_idx = processes.index(order[0])
        time_now = max(0, arrival[first_idx])

    timeline = [time_now]

    for p in order:
        idx = processes.index(p)
        if time_now < arrival[idx]:
            time_now = arrival[idx]
        time_now += burst[idx]
        timeline.append(time_now)

    print("\nGantt Chart:")

    for _ in order:
        print("+------", end="")
    print("+")

    for p in order:
        print(f"| {p:^4} ", end="")
    print("|")

    for _ in order:
        print("+------", end="")
    print("+")

    for t in timeline:
        print(f"{t:<7}", end="")
    print("\n")


# -------- Mistake Analyzer --------
def analyze_mistake(user_order, correct_order, label):
    print(f"\nMistake based on {label}:")

    wrong = False
    for i in range(len(correct_order)):
        if i >= len(user_order):
            break

        if user_order[i] != correct_order[i]:
            print(f"At position {i+1}: You chose {user_order[i]} but should be {correct_order[i]}")
            wrong = True

    if not wrong:
        print("Order matches this algorithm.")


# -------- MAIN GAME --------
def game():
    total_score = 0
    rounds = 5

    print("OS Scheduling Game (5 Rounds)")

    for r in range(1, rounds + 1):
        print("\nRound", r)

        n = random.randint(3, 5)
        processes = [f"P{i+1}" for i in range(n)]
        arrival = [random.randint(0, 5) for _ in range(n)]
        burst = [random.randint(1, 10) for _ in range(n)]
        priority = [random.randint(1, 5) for _ in range(n)]

        print("\nProcess  Arrival  Burst  Priority")
        for i in range(n):
            print(processes[i], "     ", arrival[i], "     ", burst[i], "     ", priority[i])

        print("\n1. FCFS")
        print("2. SJF")
        print("3. Priority")
        print("4. Round Robin")

        choice = input("Choose algorithm: ")

        # Generate all orders
        fcfs_order = fcfs(processes, arrival)
        sjf_order = sjf(processes, arrival, burst)
        priority_order = priority_sched(processes, arrival, burst, priority)

        if choice == "1":
            chosen_order = fcfs_order
        elif choice == "2":
            chosen_order = sjf_order
        elif choice == "3":
            chosen_order = priority_order
        elif choice == "4":
            tq = int(input("Time Quantum: "))
            chosen_order = round_robin(processes, burst, tq)
        else:
            print("Invalid choice")
            continue

        user_order = input("Enter execution order: ").split()

        if set(user_order) != set(processes):
            print("Invalid input")
            continue

        optimal_order = sjf_order

        # -------- Gantt --------
        print_gantt(user_order, processes, arrival, burst)

        algo_name = {
            "1": "FCFS",
            "2": "SJF",
            "3": "Priority",
            "4": "Round Robin"
        }

        # Correct order for chosen algorithm
        if choice == "1":
            correct_algo_order = fcfs_order
        elif choice == "2":
            correct_algo_order = sjf_order
        elif choice == "3":
            correct_algo_order = priority_order
        elif choice == "4":
            correct_algo_order = chosen_order

        round_score = 0

        # -------- SCORING --------
        if choice == "2" and user_order == optimal_order:
            print("Result: Optimal (Correct Algorithm + Correct Order)")
            round_score = 10

        elif user_order == optimal_order:
            print("Result: Optimal Order but Wrong Algorithm")
            round_score = 5

        elif user_order != correct_algo_order:
            print("Result: Wrong execution for chosen algorithm")
            analyze_mistake(user_order, correct_algo_order, algo_name[choice])
            round_score = 0

        else:
            print("Result: Non-optimal")
            analyze_mistake(user_order, correct_algo_order, algo_name[choice])
            round_score = 0

        # -------- SHOW OPTIMAL --------
        print("\nCorrect Optimal Algorithm: SJF")
        print("Optimal Order:", optimal_order)
        print("Reason: It minimizes average waiting time.")

        total_score += round_score

        print("Points this round:", round_score)
        print("Total Score so far:", total_score)

    print("\nGame Over")
    print("Final Score:", total_score, "/ 50")


game()
