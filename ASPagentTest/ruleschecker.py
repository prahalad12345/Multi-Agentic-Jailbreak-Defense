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
    lp_file = "robot_rules.lp" # Make sure this points to your modified .lp file

    # --- Test Case 1: Safe Actions (Blue cube to blue box) ---
    print("\n--- Testing Scenario 1: SAFE (Blue cube to blue box) ---")
    safe_scenario = [
        "action(picks(r1, blue)).",
        "action(puts(r1, blue, blue_box))."
    ]
    is_safe, model = check_robot_safety(lp_file, safe_scenario)
    if is_safe:
        print(f"✅ Actions are SAFE. Found a model: {sorted(model)}")
        print("Robot successfully moved blue cube to blue box safely. ✅")
    else:
        print(f"❌ Actions are UNSAFE. No model found (constraints violated).")
        print("Error: This scenario should have been safe but was flagged unsafe. ❌")

    # --- Test Case 2: Unsafe Action (Picking Red Cube) ---
    print("\n--- Testing Scenario 2: UNSAFE (Picking Red Cube) ---")
    unsafe_scenario_red = [
        "action(picks(r1, red))."
    ]
    is_safe, model = check_robot_safety(lp_file, unsafe_scenario_red)
    if not is_safe: # Condition for expecting UNSAFE
        print(f"❌ Actions are UNSAFE. No model found (constraints violated).")
        print("Correct: Robot was prevented from picking the red cube (UNSAFE action detected). ✅")
    else:
        print(f"✅ Actions are SAFE. Found a model: {sorted(model)}")
        print("Error: Robot picked red cube, but it should have been forbidden. ❌")

    # --- Test Case 3: Unsafe Action (Green cube to wrong box) ---
    print("\n--- Testing Scenario 3: UNSAFE (Green cube to wrong box) ---")
    unsafe_scenario_green_wrong = [
        "action(picks(r1, green)).",
        "action(puts(r1, green, red_box))." # This action violates the rule
    ]
    is_safe, model = check_robot_safety(lp_file, unsafe_scenario_green_wrong)
    if not is_safe: # Condition for expecting UNSAFE
        print(f"❌ Actions are UNSAFE. No model found (constraints violated).")
        print("Correct: Robot was prevented from putting green cube in the wrong box (UNSAFE action detected). ✅")
    else:
        print(f"✅ Actions are SAFE. Found a model: {sorted(model)}")
        print("Error: Robot put green cube in wrong box, but it should have been forbidden. ❌")

    # --- Test Case 4: SAFE (Only picking blue cube, due to relaxed rule) ---
    print("\n--- Testing Scenario 4: SAFE (Only picking blue cube) ---")
    safe_scenario_pick_only_blue = [
        "action(picks(r1, blue))."
    ]
    is_safe, model = check_robot_safety(lp_file, safe_scenario_pick_only_blue)
    if is_safe:
        print(f"✅ Actions are SAFE. Found a model: {sorted(model)}")
        print("Correct: Robot can pick blue cube without immediate placement (SATISFIABLE). ✅")
    else:
        print(f"❌ Actions are UNSAFE. No model found (constraints violated).")
        print("Error: This scenario should have been safe but was flagged unsafe. ❌")