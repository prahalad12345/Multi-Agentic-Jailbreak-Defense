% Define the unsafe conditions
unsafe(weapons).
unsafe(restricted).
unsafe(people).
unsafe(exits).
unsafe(privacy).




% --- Safety Rules (Constraints) ---

% Robot Rules / Constraints
:- violation(R), unsafe(R).








