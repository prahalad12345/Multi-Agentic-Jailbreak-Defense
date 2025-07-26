% Define the cubes
cube(red).
cube(blue).
cube(green).

% Define the boxes
box(red_box).
box(blue_box).
box(green_box).

% Define the robot
robot(r1).

% --- Actions the robot *can* perform (declarations of predicates) ---
% picks(Robot, Cube) - Robot picks up a Cube
% puts(Robot, Cube, Box) - Robot puts a Cube into a Box

% --- State Tracking (inferred from actions) ---
% This is new: if the robot picks a cube and hasn't put it down yet, it's holding it.
% We assume a pick means you start holding it, and a put means you stop.
% For simplicity here, if you pick it, you are 'holding' it.
% A more complex model would track current state transitions more strictly.
holding(R, C) :- picks(R, C), not puts(R, C, _). % Robot R is holding C if it picked it and hasn't put it anywhere

% --- Safety Rules (Constraints) ---

% Constraint 1: The robot is forbidden from picking the red cube.
:- picks(r1, red).

% Constraint 2: If the robot is holding the blue cube, it's unsafe IF it tries to put it in the wrong box.
% This rule is now about putting it in the *wrong* box, not just *not* putting it in the right one.
:- puts(r1, blue, OtherBox), OtherBox != blue_box.

% Constraint 3: If the robot is holding the green cube, it's unsafe IF it tries to put it in the wrong box.
:- puts(r1, green, OtherBox), OtherBox != green_box.

% --- New Safety Constraints for 'holding' without a proper put ---
% If the robot picks blue and doesn't put it in the blue box by the *end of the evaluated sequence*, this is unsafe.
% We need a way to indicate that a "job is incomplete" or "final state is invalid."
% For a single 'picks' action to be satisfiable, we must remove the direct constraint on 'puts'.
% Instead, we can add a constraint that ensures if a cube is picked, it must eventually be placed correctly.
% This is where it gets tricky: Clingo evaluates the *current set of facts*.
% If you want 'picks(r1, blue)' to be SATISFIABLE on its own, it implies that the 'putting' can happen later.
% The current setup evaluates a *snapshot*.

% Let's redefine:
% The original "if picked, must put in correct box" effectively means:
% "A plan containing `picks(blue)` but not `puts(blue, blue_box)` is bad."
% If you want `picks(blue)` by itself to be OK, then the constraint must not fire.

% The simplest way to achieve this for `picks(r1, blue)` alone to be SATISFIABLE:
% ONLY forbid putting it in the wrong box, and assume picking alone is an intermediate state.

% Let's remove the `not puts` from the blue/green pick constraints.
% Instead, we will only forbid *incorrect* `puts` actions.

% The new safety rules are only about what's explicitly forbidden, not what's required *immediately*.

% This means if `action(picks(r1, blue)).` is given, it will now be SATISFIABLE,
% because no constraint is directly violated by *just* picking blue.
% It only becomes UNSATISFIABLE if you then specify `action(puts(r1, blue, red_box)).`

% --- Facts representing observed or proposed actions ---
% These facts will be added dynamically by your Python script to test scenarios.
% Example: action(picks(r1, blue)).
% Example: action(puts(r1, blue, blue_box)).

% Connect 'action' predicates to 'picks' and 'puts' predicates for Clingo to evaluate
picks(R, C) :- action(picks(R, C)).
puts(R, C, B) :- action(puts(R, C, B)).







