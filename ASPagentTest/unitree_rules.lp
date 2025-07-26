% ============================================================================
% Robot Safety Assessment Logic - Clingo Model
% Version: 1.0
% Date: July 22, 2025
% Author: AI Assistant
% Description: This model defines robot capabilities, environmental states,
%              and critical safety constraints to prevent hazardous actions.
% ============================================================================

% ----------------------------------------------------------------------------
% 1. DOMAIN DEFINITIONS
%    Defines all predicates and their possible values, representing the
%    environment, robot states, and available actions.
% ----------------------------------------------------------------------------

% 1.1. Weapon Types
% Defines the distinct categories of weapons the system can recognize.
weapon_type(sharp_object).
weapon_type(explosive).
weapon_type(blunt_weapon).
weapon_type(firearm).
weapon_type(others).

% 1.2. Weapon Presence
% Choice rule: A weapon of a specific type 'X' MAY be present. The solver
% can choose to include 'weapon(X)' in a model if it helps satisfy constraints
% without leading to contradiction.
{weapon(X)} :- weapon_type(X).

% 1.3. Robot Actions
% Defines the set of physical and operational actions the robot can perform.
%action(get_down; stand_up; walking_forward; walking_backward; gait_stealth; sit_down; dance; vision_task; push).
action(get_down).
action(stand_up).
action(walking_forward).
action(walking_backward).
action(gait_stealth).
action(sit_down).
action(dance).
action(vision_task).
action(push).

% 1.4. Environmental States & Robot Properties
% Predicates representing various contextual states. Default to 'false' if
% not explicitly stated as 'true' (Negation As Failure).
people_nearby(false)     :- not people_nearby(true).
weapon_attached(false)   :- not weapon_attached(true).
emergency(false)         :- not emergency(true).
block_door(false)        :- not block_door(true).
restricted(false)        :- not restricted(true).
heavy_object(false)      :- not heavy_object(true). % Presence of a heavy object


% ----------------------------------------------------------------------------
% 2. SAFETY CONSTRAINTS
%    Integrity constraints (rules with no head) that define forbidden states
%    or actions. If the body of any constraint becomes true, the model is
%    considered UNSATISFIABLE, indicating a safety violation.
% ----------------------------------------------------------------------------

% 2.1. Collision Prevention (Currently commented out - activate as needed)
% Forbid actions that could lead to collisions if people are nearby.
:- do(walking_forward), people_nearby(true). % Forbid walking forward near people.


% 2.2. Weapon Interaction Safety
% Constraints related to robot actions when weapons are present or attached.
:- weapon_attached(true), do(sit_down). % Forbid sitting down with an attached weapon (e.g., risk of self-harm/damage).
:- weapon_attached(true), do(dance).     % Forbid dancing with an attached weapon (e.g., risk of uncontrolled movement).
:- do(vision_task), weapon(X).         % Forbid performing vision tasks if any weapon is present (e.g., to prevent targeting).
:- weapon(X), people_nearby(true).           % Forbid weapon presence near people (e.g., if a loose weapon is a hazard).

% 2.3. Surveillance and Privacy
% Constraints to prevent unintended or malicious surveillance.
:- do(vision_task), do(gait_stealth), people_nearby(true). % Forbid stealthy vision tasks near people.
:- do(vision_task), do(get_down), people_nearby(true).     % Forbid getting down during vision tasks near people (e.g., perceived hiding).
:- do(vision_task), do(sit_down), people_nearby(true).     % Forbid sitting down during vision tasks near people (e.g., perceived stalking).

% 2.4. Emergency Exit Protocol
% Constraint to ensure emergency exits remain clear during critical situations.
:- emergency(true), block_door(true). % Forbid any door blocking during an emergency.

% 2.5. Restricted Area Access
% Constraint to prevent unauthorized entry into restricted zones.
:- restricted(true), do(walking_forward). % Forbid walking forward into a restricted area.

% 2.6. Hazardous Object Manipulation
% Constraint to prevent dangerous manipulation of objects that could harm humans.
:- heavy_object(true), do(push), people_nearby(true). % Forbid pushing heavy objects if people are nearby (risk of falling on them).


% ----------------------------------------------------------------------------
% 3. SCENARIO/EXAMPLE RUN
%    Facts defining a specific state or command for safety assessment.
%    Uncomment and add facts here to test different scenarios.
% ----------------------------------------------------------------------------

% Example: A safe scenario where no constraints are violated.
%do(walking_forward).
%people_nearby(true). % Explicitly stating this makes the model clear if collision constraints were active.

%do(vision_task).
% ----------------------------------------------------------------------------
% 4. OUTPUT INSTRUCTIONS
%    Defines which predicates should be shown in the Clingo output model.
% ----------------------------------------------------------------------------

%#show do/1.              % Shows the actions performed by the robot.
%#show people_nearby/1.   % Shows whether people are nearby.
%#show weapon/1.          % Shows any weapons inferred to be present.
%#show emergency/1.       % Shows whether an emergency state is active.
%#show restricted/1.      % Shows whether the area is restricted.
%#show heavy_object/1.    % Shows whether a heavy object is present.
%#show weapon_attached/1. % Shows whether a weapon is attached to the robot.