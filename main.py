import json

FILE_NAME = "workouts.json"


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "saved_workouts": [],
            "completed_workouts": []
        }


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def display_main_menu():
    print("\n============================")
    print("      WORKOUT PLANNER")
    print("============================")
    print("Create and save workout plans, then log them when you finish.")
    print("Your workout information is stored locally on this computer.")
    print("No account, payment, or personal information is required.")
    print()
    print("1. Create a Workout")
    print("2. View Saved Workouts")
    print("3. Log a Completed Workout")
    print("4. Help")
    print("5. Exit")


def show_create_help():
    print("\nHELP")
    print("Enter a workout name, then add at least one exercise.")
    print("Each exercise needs a name, number of sets, and number of reps.")
    print("B = Back")
    print("C = Cancel")
    print("H = Help")


def get_positive_number(message):
    while True:
        value = input(message).strip().lower()

        if value in ("b", "back"):
            return "back"

        if value in ("c", "cancel"):
            return "cancel"

        if value in ("h", "help"):
            show_create_help()
            continue

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Please enter a whole number greater than 0.")
        print("You may also enter B, C, or H.")


def review_workout(workout_name, exercises, data):
    while True:
        print("\n============================")
        print(" CREATE A WORKOUT - STEP 3 OF 3")
        print("============================")
        print("Review your workout before saving.")
        print(f"\n{workout_name.upper()}")

        for number, exercise in enumerate(exercises, start=1):
            print(
                f"{number}. {exercise['name']} - "
                f"{exercise['sets']} sets of {exercise['reps']}"
            )

        print("\n1. Save Workout")
        print("2. Go Back and Add Another Exercise")
        print("3. Cancel")
        print("\nNothing will be saved until you select Save Workout.")

        choice = input(
            "\nEnter a number or type the option name: "
        ).strip().lower()

        if choice in ("1", "save", "save workout"):
            workout = {
                "name": workout_name,
                "exercises": exercises
            }

            data["saved_workouts"].append(workout)
            save_data(data)

            print("\nWORKOUT SAVED")
            print(f'"{workout_name}" was saved successfully.')
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


def create_workout(data):
    while True:
        print("\n============================")
        print(" CREATE A WORKOUT - STEP 1 OF 3")
        print("============================")
        print("First, enter a name for your workout.")
        print("Examples: Push Day, Leg Day, or Cardio")
        print("\nB = Back")
        print("C = Cancel")
        print("H = Help")

        workout_name = input("\nWorkout name: ").strip()
        command = workout_name.lower()

        if command in ("b", "back", "c", "cancel"):
            print("\nWorkout creation canceled.")
            return

        if command in ("h", "help"):
            show_create_help()
            continue

        if workout_name == "":
            print("\nA workout name is required.")
            continue

        break

    exercises = []

    while True:
        print("\n============================")
        print(" CREATE A WORKOUT - STEP 2 OF 3")
        print("============================")
        print(f"Workout: {workout_name}")

        if exercises:
            print("\nExercises currently added:")

            for number, exercise in enumerate(exercises, start=1):
                print(
                    f"{number}. {exercise['name']} - "
                    f"{exercise['sets']} sets of {exercise['reps']}"
                )

        print("\nB = Back")
        print("C = Cancel")
        print("H = Help")

        exercise_name = input("\nExercise name: ").strip()
        command = exercise_name.lower()

        if command in ("b", "back"):
            print("\nReturning to the workout name step.")
            return create_workout(data)

        if command in ("c", "cancel"):
            print("\nWorkout creation canceled.")
            print("No workout was saved.")
            return

        if command in ("h", "help"):
            show_create_help()
            continue

        if exercise_name == "":
            print("\nAn exercise name is required.")
            continue

        sets = get_positive_number("Number of sets: ")

        if sets == "back":
            print("\nReturning to the exercise name.")
            continue

        if sets == "cancel":
            print("\nWorkout creation canceled.")
            print("No workout was saved.")
            return

        reps = get_positive_number("Number of repetitions: ")

        if reps == "back":
            print("\nReturning to the exercise name.")
            continue

        if reps == "cancel":
            print("\nWorkout creation canceled.")
            print("No workout was saved.")
            return

        exercises.append({
            "name": exercise_name,
            "sets": sets,
            "reps": reps
        })

        while True:
            print("\nExercise added.")
            print("1. Add Another Exercise")
            print("2. Review Workout")
            print("C = Cancel")
            print("H = Help")

            choice = input(
                "\nEnter a number or type the option name: "
            ).strip().lower()

            if choice in (
                "1",
                "add",
                "add another",
                "add another exercise"
            ):
                break

            if choice in ("2", "review", "review workout"):
                result = review_workout(workout_name, exercises, data)

                if result in ("saved", "cancel"):
                    return

                break

            if choice in ("c", "cancel"):
                print("\nWorkout creation canceled.")
                print("No workout was saved.")
                return

            if choice in ("h", "help"):
                show_create_help()
                continue

            print("\nThat option was not recognized.")
            print("Please choose 1, 2, C, or H.")


def main():
    data = load_data()

    while True:
        display_main_menu()

        choice = input(
            "\nEnter a number or type the option name: "
        ).strip().lower()

        if choice in ("1", "create", "create a workout"):
            create_workout(data)

        elif choice in ("2", "view", "view saved workouts"):
            print("\nView Saved Workouts selected.")

        elif choice in ("3", "log", "log a completed workout"):
            print("\nLog Completed Workout selected.")

        elif choice in ("4", "help"):
            print("\nHelp selected.")

        elif choice in ("5", "exit"):
            print("\nYour workout information has been saved.")
            print("Goodbye!")
            break

        else:
            print("\nThat option was not recognized.")
            print("Please enter a number from 1 through 5.")


if __name__ == "__main__":
    main()