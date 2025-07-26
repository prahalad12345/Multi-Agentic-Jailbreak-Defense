% ======= DOMAIN DEFINITIONS =======

weapon_type(sharp_object).
weapon_type(explosive).
weapon_type(blunt_weapon).
weapon_type(firearm).
weapon_type(others).

% Use a choice rule to state that a weapon of a certain type *may* be present.
% The solver can choose to include weapon(X) for any weapon_type(X), or not.
{weapon(X)} :- weapon_type(X).


action(get_down; stand_up; walking_forward; walking_backward; gait_stealth; sit_down; dance; vision_task; push).


% Default: people_nearby is false unless explicitly true
people_nearby(false) :- not people_nearby(true).
weapon_attached(false) :- not weapon_attached(true).
emergency(false) :- not emergency(true).
block_door(false) :- not block_door(true).
restricted(false) :- not restricted(true).
heavy_object(false) :- not heavy_object(true).



% ========= SAFETY CONSTRAINTS =========

% Colliding with Humans

%:- do(walking_forward), people_nearby(true).
%:- do(dance), people_nearby(true).
%:- weapon(X) , people_nearby(true).

% Interaction with Weapons

:- weapon_attached(true)  , do(sit_down).
:- weapon_attached(true) , do(dance).
:- do(vision_task) , weapon(X).


%Secret Surveillance
:- do(vision_task), do(gait_stealth), people_nearby(true).
:- do(vision_task), do(get_down), people_nearby(true).  
:- do(vision_task), do(sit_down), people_nearby(true).  

%Emergency exits
:- emergency(true), block_door(true).

%Access Restricted Area
:- restricted(true), do(walk_forward).


%Push the shelves onto a human on the otherside
:- heavy_object(true), do(push) , people_nearby(true).


% ========= EXAMPLE: SAFE CASE =========


% ======= OUTPUT =======

