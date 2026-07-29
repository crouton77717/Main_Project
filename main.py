import json

FILE_NAME = "workouts.json"


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if "saved_workouts" not in data:
            data["saved_workouts"] = []

        if "completed_workouts" not in data:
            data["completed_workouts"] = []

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "saved_workouts": [],
            "completed_workouts": []
        }


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def format_exercise(exercise):
    if exercise["weight"] == 0:
        weight_text = "Bodyweight"
    else:
        weight_text = f'{exercise["weight"]} lbs'

    return (
        f'{exercise["name"]} - '
        f'{exercise["sets"]} sets of '
        f'{exercise["reps"]} reps at {weight_text}'
    )


def main_menu(data):
    while True:
        print("\n============================")
        print("      WORKOUT PLANNER")
        print("============================")
        print("Create, save, and track your workouts.")
        print("Your workout information is stored locally.")
        print("No account, payment, or personal information is required.")
        print()
        print("1. Create a Workout")
        print("2. View Saved Workouts")
        print("3. Log a Completed Workout")
        print("4. Search Exercises")
        print("5. Help")
        print("6. Exit")

        choice = input(
            "\nEnter a number or option name: "
        ).strip().lower()

        if choice in ("1", "create", "create a workout"):
            create_workout(data)

        elif choice in ("2", "view", "view saved workouts"):
            saved_workouts_page(data)

        elif choice in ("3", "log", "log a completed workout"):
            log_completed_page(data)

        elif choice in ("4", "search", "search exercises"):
            search_exercises(data)

        elif choice in ("5", "help"):
            help_page()

        elif choice in ("6", "exit"):
            print("\nYour workout information has been saved.")
            print("Goodbye!")
            break

        else:
            print("\nThat option was not recognized.")
            print("Please enter a number from 1 through 6.")


def get_number(message, minimum):
    while True:
        value = input(message).strip().lower()

        if value in ("b", "back"):
            return "back"

        if value in ("c", "cancel"):
            return "cancel"

        if value in ("h", "help"):
            print("\nEnter a whole number.")
            print("Sets and reps must be greater than 0.")
            print("Weight may be 0 for a bodyweight exercise.")
            continue

        if value.isdigit() and int(value) >= minimum:
            return int(value)

        if minimum == 0:
            print("\nPlease enter a whole number that is 0 or greater.")
        else:
            print("\nPlease enter a whole number greater than 0.")

        print("You may also enter B, C, or H.")


def create_workout(data):
    while True:
        print("\n============================")
        print(" CREATE WORKOUT - STEP 1 OF 3")
        print("============================")
        print("Enter a name for your workout.")
        print("Examples: Push Day, Leg Day, or Cardio")
        print()
        print("B. Back")
        print("C. Cancel")
        print("H. Help")

        workout_name = input("\nWorkout name: ").strip()
        command = workout_name.lower()

        if command in ("b", "back", "c", "cancel"):
            return

        if command in ("h", "help"):
            print("\nChoose a name that describes the workout.")
            continue

        if workout_name == "":
            print("\nA workout name is required.")
            continue

        exercises = []
        go_back_to_name = False

        while True:
            print("\n============================")
            print(" CREATE WORKOUT - STEP 2 OF 3")
            print("============================")
            print(f"Workout: {workout_name}")

            if exercises:
                print("\nExercises currently added:")

                for number, exercise in enumerate(exercises, start=1):
                    print(f"{number}. {format_exercise(exercise)}")

            print()
            print("B. Back")
            print("C. Cancel")
            print("H. Help")

            exercise_name = input("\nExercise name: ").strip()
            command = exercise_name.lower()

            if command in ("b", "back"):
                go_back_to_name = True
                break

            if command in ("c", "cancel"):
                print("\nWorkout creation canceled.")
                print("No workout was saved.")
                return

            if command in ("h", "help"):
                print("\nEnter the name of one exercise.")
                print("Example: Bench Press")
                continue

            if exercise_name == "":
                print("\nAn exercise name is required.")
                continue

            sets = get_number("Number of sets: ", 1)

            if sets == "back":
                print("\nReturning to the exercise-name prompt.")
                continue

            if sets == "cancel":
                print("\nWorkout creation canceled.")
                return

            reps = get_number("Number of repetitions: ", 1)

            if reps == "back":
                print("\nReturning to the exercise-name prompt.")
                continue

            if reps == "cancel":
                print("\nWorkout creation canceled.")
                return

            weight = get_number(
                "Weight in pounds (enter 0 for bodyweight): ",
                0
            )

            if weight == "back":
                print("\nReturning to the exercise-name prompt.")
                continue

            if weight == "cancel":
                print("\nWorkout creation canceled.")
                return

            exercise = {
                "name": exercise_name,
                "sets": sets,
                "reps": reps,
                "weight": weight
            }

            exercises.append(exercise)

            while True:
                print("\nExercise added.")
                print("1. Add Another Exercise")
                print("2. Review Workout")
                print("3. Cancel")

                choice = input(
                    "\nEnter a number or option name: "
                ).strip().lower()

                if choice in (
                    "1",
                    "add",
                    "add another",
                    "add another exercise"
                ):
                    break

                if choice in ("2", "review", "review workout"):
                    result = review_workout(
                        workout_name,
                        exercises,
                        data
                    )

                    if result == "back":
                        break

                    return

                if choice in ("3", "c", "cancel"):
                    print("\nWorkout creation canceled.")
                    print("No workout was saved.")
                    return

                print("\nThat option was not recognized.")
                print("Please choose 1, 2, or 3.")

        if go_back_to_name:
            print("\nReturning to the workout-name step.")
            continue


def review_workout(workout_name, exercises, data):
    while True:
        print("\n============================")
        print(" CREATE WORKOUT - STEP 3 OF 3")
        print("============================")
        print("Review your workout before saving.")
        print()
        print(f"Workout: {workout_name}")

        for number, exercise in enumerate(exercises, start=1):
            print(f"{number}. {format_exercise(exercise)}")

        print()
        print("1. Save Workout")
        print("2. Go Back and Add Another Exercise")
        print("3. Cancel")
        print()
        print("Nothing will be saved until you select Save Workout.")

        choice = input(
            "\nEnter a number or option name: "
        ).strip().lower()

        if choice in ("1", "save", "save workout"):
            workout = {
                "name": workout_name,
                "exercises": exercises
            }

            data["saved_workouts"].append(workout)
            save_data(data)

            workout_saved_page(workout_name)
            return "saved"

        if choice in (
            "2",
            "back",
            "go back",
            "add another exercise"
        ):
            return "back"

        if choice in ("3", "c", "cancel"):
            print("\nWorkout creation canceled.")
            print("No workout was saved.")
            return "cancel"

        print("\nThat option was not recognized.")
        print("Please choose 1, 2, or 3.")


def workout_saved_page(workout_name):
    print("\n============================")
    print("       WORKOUT SAVED")
    print("============================")
    print(f'"{workout_name}" was saved successfully.')

    input("\nPress Enter to return to the Main Menu.")


def find_workout(choice, workouts):
    if choice.isdigit():
        workout_number = int(choice)

        if 1 <= workout_number <= len(workouts):
            return workouts[workout_number - 1]

    for workout in workouts:
        if workout["name"].lower() == choice.lower():
            return workout

    return None


def saved_workouts_page(data):
    while True:
        print("\n============================")
        print("       SAVED WORKOUTS")
        print("============================")

        workouts = data["saved_workouts"]

        if not workouts:
            print("You do not have any saved workouts.")
            input("\nPress Enter to return to the Main Menu.")
            return

        for number, workout in enumerate(workouts, start=1):
            print(f"{number}. {workout['name']}")

        print()
        print("B. Back")
        print("H. Help")

        choice = input(
            "\nChoose a workout or option: "
        ).strip()

        if choice.lower() in ("b", "back"):
            return

        if choice.lower() in ("h", "help"):
            print("\nEnter a workout number or its name.")
            continue

        workout = find_workout(choice, workouts)

        if workout is None:
            print("\nThat workout was not found.")
            continue

        workout_details_page(workout)


def workout_details_page(workout):
    while True:
        print("\n============================")
        print("       WORKOUT DETAILS")
        print("============================")
        print(f"Workout: {workout['name']}")
        print()

        for number, exercise in enumerate(
            workout["exercises"],
            start=1
        ):
            print(f"{number}. {format_exercise(exercise)}")

        print()
        print("B. Back")
        print("H. Help")

        choice = input("\nChoose an option: ").strip().lower()

        if choice in ("b", "back"):
            return

        if choice in ("h", "help"):
            print("\nThis page displays every exercise in the workout.")
            continue

        print("\nPlease enter B or H.")


def log_completed_page(data):
    while True:
        print("\n============================")
        print("   LOG COMPLETED WORKOUT")
        print("============================")

        workouts = data["saved_workouts"]

        if not workouts:
            print("You do not have any saved workouts to log.")
            input("\nPress Enter to return to the Main Menu.")
            return

        print("Select the workout you completed.")
        print()

        for number, workout in enumerate(workouts, start=1):
            print(f"{number}. {workout['name']}")

        print()
        print("B. Back")
        print("H. Help")

        choice = input(
            "\nChoose a workout or option: "
        ).strip()

        if choice.lower() in ("b", "back"):
            return

        if choice.lower() in ("h", "help"):
            print("\nEnter a workout number or its name.")
            continue

        workout = find_workout(choice, workouts)

        if workout is None:
            print("\nThat workout was not found.")
            continue

        result = confirm_log_page(workout, data)

        if result == "logged" or result == "cancel":
            return


def confirm_log_page(workout, data):
    while True:
        print("\n============================")
        print("    CONFIRM COMPLETION")
        print("============================")
        print(f'You selected "{workout["name"]}".')
        print("Logging it will record the workout as completed.")
        print()
        print("1. Confirm and Log")
        print("2. Go Back")
        print("3. Cancel")

        choice = input(
            "\nEnter a number or option name: "
        ).strip().lower()

        if choice in (
            "1",
            "confirm",
            "log",
            "confirm and log"
        ):
            completed_workout = {
                "name": workout["name"],
                "exercises": workout["exercises"]
            }

            data["completed_workouts"].append(completed_workout)
            save_data(data)

            print("\n============================")
            print("       WORKOUT LOGGED")
            print("============================")
            print(
                f'"{workout["name"]}" was logged as completed.'
            )

            input("\nPress Enter to return to the Main Menu.")
            return "logged"

        if choice in ("2", "b", "back", "go back"):
            return "back"

        if choice in ("3", "c", "cancel"):
            print("\nNo workout was logged.")
            return "cancel"

        print("\nThat option was not recognized.")
        print("Please choose 1, 2, or 3.")


def help_page():
    print("\n============================")
    print("            HELP")
    print("============================")
    print("Create a Workout:")
    print("Enter a workout name, then add exercises.")
    print("Each exercise has sets, repetitions, and weight.")
    print()
    print("View Saved Workouts:")
    print("Choose a workout to view all its exercises.")
    print()
    print("Log a Completed Workout:")
    print("Choose a saved workout and confirm that you completed it.")
    print()
    print("Options may be selected by number or name.")
    print("Back returns to the previous page.")
    print("Cancel returns to the Main Menu without saving.")

    input("\nPress Enter to return to the Main Menu.")

def search_exercises(data):
    print("\n============================")
    print("      SEARCH EXERCISES")
    print("============================")

    search_term = input(
        "Enter an exercise name or part of a name: "
    ).strip().lower()

    if search_term == "":
        print("\nPlease enter something to search for.")
        return

    matches = []

    for workout in data["saved_workouts"]:
        for exercise in workout["exercises"]:
            if search_term in exercise["name"].lower():
                matches.append((workout["name"], exercise))

    if not matches:
        print("\nNo matching exercises were found.")
        return

    print("\nMatching exercises:")

    for workout_name, exercise in matches:
        print(
            f"{exercise['name']} in {workout_name}: "
            f"{exercise['sets']} sets of {exercise['reps']} reps "
            f"at {exercise['weight']} lbs"
        )

    input("\nPress Enter to return to the Main Menu.")


def main():
    data = load_data()
    main_menu(data)


if __name__ == "__main__":
    main()