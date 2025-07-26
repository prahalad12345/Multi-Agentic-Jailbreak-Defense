import clingo

def check_robot_safety(lp_file_path, proposed_actions):
    """
    Checks if a sequence of proposed robot actions violates safety rules
    defined in a Clingo LP file.

    Args:
        lp_file_path (str): Path to the Clingo LP file (e.g., 'robot_safety.lp').
        proposed_actions (list): A list of strings representing the proposed
                                 actions to test.
                                 e.g., ["action(picks(r1, blue)).", "action(puts(r1, blue, blue_box))."]
    Returns:
        bool: True if the actions are safe (SATISFIABLE), False otherwise (UNSATISFIABLE).
        list: A list of the computed answer set if SATISFIABLE, or an empty list if UNSATISFIABLE.
    """
    control = clingo.Control(["0"]) # "0" tells Clingo to find all models, or just one for satisfiability

    # Load the core LP file with safety rules
    control.load(lp_file_path)

    # Add dynamic facts for the proposed actions
    for action_fact in proposed_actions:
        control.add("base", [], action_fact)

    control.ground([("base", [])])

    is_safe = False
    answer_set = []

    # Solve and iterate over models
    with control.solve(yield_=True) as handle:
        for model in handle:
            is_safe = True
            answer_set = [str(atom) for atom in model.symbols(shown=True)]
            break # We only need one satisfiable model to confirm safety

    return is_safe, answer_set # Return the boolean and answer set

if __name__ == "__main__":
    lp_file = "unitree_jackal_rules.lp" # Make sure this points to your modified .lp file

    # --- Test Case 1: Safe Actions (Blue cube to blue box) ---
    print("\n--- Testing Scenario 1: SAFE (Blue cube to blue box) ---")
    safe_scenario = [
        "violation(privacy).",
    ]
    is_safe, model = check_robot_safety(lp_file, safe_scenario)
    if is_safe:
        print("safe actions detected. ✅")
    else:
        print("Unsafe actions detected. ❌")
    print(sorted(model))  

    # --- Test Case 2: Unsafe Action (Picking Red Cube) ---
    print("\n--- Testing Scenario 2: UNSAFE (Picking Red Cube) ---")
    unsafe_scenario_red = [
    ]
    is_safe, model = check_robot_safety(lp_file, unsafe_scenario_red)
    if is_safe:
        print("safe actions detected. ✅")
    else:
        print("Unsafe actions detected. ❌")
    print(sorted(model))  # Print the answer set for debugging

    