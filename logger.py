import json
import os
from datetime import datetime

DATA_FILE = "experiments.json"


def load_experiments():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_experiments(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_experiment():
    print("\n--- Add New Experiment ---")
    name = input("Experiment name: ")
    input_data = input("Input: ")
    observation = input("Observation: ")
    result = input("Result: ")

    experiment = {
        "name": name,
        "input": input_data,
        "observation": observation,
        "result": result,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data = load_experiments()
    data.append(experiment)
    save_experiments(data)

    print("\n✅ Experiment saved successfully!")


def view_experiments():
    print("\n--- Saved Experiments ---")
    data = load_experiments()

    if not data:
        print("No experiments found.")
        return

    for index, exp in enumerate(data, start=1):
        print(f"\nExperiment {index}")
        print(f"Name        : {exp['name']}")
        print(f"Input       : {exp['input']}")
        print(f"Observation : {exp['observation']}")
        print(f"Result      : {exp['result']}")
        print(f"Time        : {exp['time']}")


def main():
    while True:
        print("\n=== Digital Experiment Logger ===")
        print("1. Add Experiment")
        print("2. View Experiments")
        print("3. Exit")

        choice = input("Select option (1/2/3): ")

        if choice == "1":
            add_experiment()
        elif choice == "2":
            view_experiments()
        elif choice == "3":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    main()
