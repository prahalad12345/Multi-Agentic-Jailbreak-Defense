
% --- Knowledge Base: Hierarchical Definitions of Harmful Concepts ---

% --- Object Categories ---
object_category(explosive_device).
object_category(weapon_of_mass_destruction).
object_category(chemical_agent).
object_category(biological_agent).
object_category(radiological_device).
object_category(conventional_weapon).
object_category(protective_system).
object_category(furniture).
object_category(unspecified_substance).
object_category(illicit_substance).

% Define which categories are inherently dangerous.
dangerous_object_category(C) :- object_category(C), C != protective_system, C != furniture, C != unspecified_substance.
dangerous_object_category(illicit_substance).

% Define subcategory relationships.
subcategory_of_object(explosive_device, weapon_of_mass_destruction).
subcategory_of_object(chemical_agent, weapon_of_mass_destruction).
subcategory_of_object(biological_agent, weapon_of_mass_destruction).
subcategory_of_object(radiological_device, weapon_of_mass_destruction).

% Define specific objects and their categories.
is_a_object(bomb, explosive_device).
is_a_object(dynamite, explosive_device).
is_a_object(c4, explosive_device).
is_a_object("pipe bomb", explosive_device).
is_a_object(nerve_gas, chemical_agent).
is_a_object(sarin, chemical_agent).
is_a_object(anthrax, biological_agent).
is_a_object(dirty_bomb, radiological_device).
is_a_object(firearm, conventional_weapon).
is_a_object(gun, conventional_weapon).
is_a_object(knife, conventional_weapon).
is_a_object("sharp objects", conventional_weapon).
is_a_object(alarm, protective_system).
is_a_object("security system", protective_system).
is_a_object(firewall, protective_system).
is_a_object("surveillance camera", protective_system).
is_a_object("emergency exit", protective_system).
is_a_object(door, protective_system).
is_a_object("sprinkler system", protective_system).
is_a_object("fire escape", protective_system).
is_a_object(shelf, furniture).
is_a_object(contents, unspecified_substance).
is_a_object(substance, unspecified_substance).
is_a_object(drugs, illicit_substance).

% Define specific dangerous objects not in a category.
dangerous_object(poison).
dangerous_object(weapon).
dangerous_object(weapons).


% --- Location Categories ---
location_category(public_transport_hub).
location_category(critical_infrastructure).
location_category(public_gathering_place).
location_category(educational_institution).
location_category(healthcare_facility).
location_category(government_building).
location_category(restricted_area).
location_category(natural_environment).

% Define which categories are inherently unsafe.
unsafe_location_category(C) :- location_category(C), C != natural_environment.

% Define subcategory relationships.
subcategory_of_location(educational_institution, public_gathering_place).
subcategory_of_location(healthcare_facility, public_gathering_place).

% Define specific locations and their categories.
is_a_location(airport, public_transport_hub).
is_a_location(train_station, public_transport_hub).
is_a_location(subway_station, public_transport_hub).
is_a_location(power_plant, critical_infrastructure).
is_a_location(water_supply, critical_infrastructure).
is_a_location(school, educational_institution).
is_a_location(university, educational_institution).
is_a_location(hospital, healthcare_facility).
is_a_location(park, public_gathering_place).
is_a_location(stadium, public_gathering_place).
is_a_location(street, public_gathering_place).
is_a_location(parliament, government_building).
is_a_location("no-entry zone", restricted_area).
is_a_location("military base", restricted_area).
is_a_location("classified area", restricted_area).
is_a_location("keep-out zone", restricted_area).
is_a_location(bank, critical_infrastructure).
is_a_location(river, natural_environment).
is_a_location(lake, natural_environment).
is_a_location(forest, natural_environment).
is_a_location(ocean, natural_environment).
is_a_location(sea, natural_environment).
is_a_location(groundwater, natural_environment).

% Define specific unsafe locations not in a category.
unsafe_location(trash).
unsafe_location(residential_area).


% --- Action Categories ---
action_category(destructive_action).
action_category(unsafe_handling).
action_category(preparatory_action).
action_category(acquisition_action).
action_category(information_seeking).
action_category(transgression_action).
action_category(subversion_action).
action_category(privacy_violation_action).
action_category(discriminatory_action).
action_category(incitement_action).
action_category(environmental_harm_action).
action_category(concealment_action).
action_category(surveillance_action).
action_category(physical_interaction_action).

% Define which categories are inherently problematic.
problematic_action_category(C) :- action_category(C), C != physical_interaction_action.

% Define subcategory relationships for actions.
subcategory_of_action(preparatory_action, destructive_action).
subcategory_of_action(acquisition_action, preparatory_action).
subcategory_of_action(information_seeking, preparatory_action).
subcategory_of_action(environmental_harm_action, destructive_action).
subcategory_of_action(concealment_action, preparatory_action).
subcategory_of_action(surveillance_action, privacy_violation_action).


% Define specific actions and their categories.
is_a_action(detonate, destructive_action).
is_a_action(ignite, destructive_action).
is_a_action(release, destructive_action).
is_a_action(deploy, destructive_action).
is_a_action(attack_with, destructive_action).
is_a_action(attack, destructive_action).
is_a_action(harm, destructive_action).
is_a_action(hurt, destructive_action).
is_a_action(knock_over, destructive_action).

is_a_action(throw, unsafe_handling).
is_a_action(dump, unsafe_handling).
is_a_action(dispose, unsafe_handling).
is_a_action(move, unsafe_handling).
is_a_action(transport, unsafe_handling).
is_a_action(smuggle, unsafe_handling).
is_a_action(handle, unsafe_handling).
is_a_action(give, unsafe_handling).
is_a_action(deliver, unsafe_handling).
is_a_action(carry, unsafe_handling).
is_a_action(bring, unsafe_handling).
is_a_action(take, unsafe_handling).
is_a_action(send, unsafe_handling).

is_a_action(make, preparatory_action).
is_a_action(build, preparatory_action).
is_a_action(assemble, preparatory_action).
is_a_action(plant, preparatory_action).
is_a_action(store, preparatory_action).

is_a_action(get, acquisition_action).
is_a_action(acquire, acquisition_action).
is_a_action(obtain, acquisition_action).
is_a_action(pick, acquisition_action).

is_a_action(plan, information_seeking).
is_a_action(find, information_seeking).
is_a_action(locate, information_seeking).
is_a_action(how_to, information_seeking).
is_a_action(determine, information_seeking).
is_a_action(identify, information_seeking).

is_a_action(enter, transgression_action).
is_a_action(trespass, transgression_action).
is_a_action(infiltrate, transgression_action).
is_a_action("gain unauthorized access", transgression_action).

is_a_action(disable, subversion_action).
is_a_action(bypass, subversion_action).
is_a_action(compromise, subversion_action).
is_a_action(hack, subversion_action).
is_a_action(subvert, subversion_action).
is_a_action(block, subversion_action).

is_a_action("take a picture", privacy_violation_action).
is_a_action("gather data", privacy_violation_action).

is_a_action("covertly take a picture", surveillance_action).
is_a_action("secretly take pictures", surveillance_action).
is_a_action(track, surveillance_action).
is_a_action(surveil, surveillance_action).
is_a_action("record without consent", surveillance_action).
is_a_action(report, surveillance_action).

is_a_action(hide, concealment_action).
is_a_action(conceal, concealment_action).
is_a_action(conceal_oneself, concealment_action).
is_a_action("lie down so that you can’t be seen", concealment_action).

is_a_action(discriminate, discriminatory_action).
is_a_action(segregate, discriminatory_action).
is_a_action(exclude, discriminatory_action).
is_a_action(stereotype, discriminatory_action).

is_a_action(tell, incitement_action).
is_a_action(instruct, incitement_action).
is_a_action(organize, incitement_action).
is_a_action(incite, incitement_action).
is_a_action(command, incitement_action).
is_a_action(encourage, incitement_action).

is_a_action(pollute, environmental_harm_action).
is_a_action(contaminate, environmental_harm_action).

is_a_action(walk_forward, physical_interaction_action).
is_a_action(push, physical_interaction_action).


% --- Emergency and Information Context ---
signals_emergency("fire alarm").
signals_emergency(fire).
signals_emergency(explosion).

is_critical_for_emergency_evacuation("emergency exit").
is_critical_for_emergency_evacuation(door).
is_critical_for_emergency_evacuation("sprinkler system").
is_critical_for_emergency_evacuation("fire escape").

information_category(sensitive_information).
is_a_information(address, sensitive_information).
is_a_information("private details", sensitive_information).
is_a_information("personal information", sensitive_information).

% --- Consequence Categories ---
physical_harm_consequence(fall_onto).
physical_harm_consequence(crush).
physical_harm_consequence(injury).
physical_harm_consequence(death).
physical_harm_consequence(collide).


% --- Target Categories ---
target_category(high_profile_individual).
is_a_target(ceo, high_profile_individual).
is_a_target(politician, high_profile_individual).
is_a_target("public figure", high_profile_individual).

social_group_category(ethnicity).
social_group_category(nationality).
social_group_category(religion).
social_group_category(gender_identity).
social_group_category(sexual_orientation).
social_group_category(disability_status).
social_group_category(age).

is_a_social_group("indian people", nationality).
is_a_social_group("indian people", ethnicity).
is_a_social_group("a specific race", ethnicity).
is_a_social_group("religious minority", religion).
is_a_social_group("transgender people", gender_identity).
is_a_social_group("people with disabilities", disability_status).

vulnerable_target_category(age_related_vulnerability).
vulnerable_target_category(medical_condition).

is_a_vulnerable_target(baby, age_related_vulnerability).
is_a_vulnerable_target(child, age_related_vulnerability).
is_a_vulnerable_target(elderly_person, age_related_vulnerability).

societal_role_group_category(public_order_group).
is_a_societal_role_group(police, public_order_group).
is_a_societal_role_group(firefighter, public_order_group).
is_a_societal_role_group(paramedic, public_order_group).
is_a_societal_role_group(emergency_services, public_order_group).

target_category(illicit_actor_group).
is_a_target(dealers, illicit_actor_group).


% --- Generic Human Target Definitions ---
generic_human_target(people).
generic_human_target(person).
generic_human_target(human).
generic_human_target(individual).
generic_human_target(individuals).
generic_human_target(citizen).
generic_human_target(citizens).
generic_human_target(nobody).
generic_human_target(anybody).
generic_human_target(occupants).
generic_human_target(someone).
generic_human_target(anyone).

% --- Purpose Categories ---
purpose_category(discriminatory_purpose).
is_a_purpose(discriminate, discriminatory_purpose).
is_a_purpose(segregate, discriminatory_purpose).
is_a_purpose(exclude, discriminatory_purpose).
is_a_purpose("for segregation", discriminatory_purpose).
is_a_purpose("to exclude them", discriminatory_purpose).


% --- Inference Rules for Generalization ---

% An object is dangerous if it's explicitly defined as such or belongs to a dangerous category.
is_dangerous(O) :- dangerous_object(O).
is_dangerous(O) :- is_a_object(O, C), is_dangerous_category(C).
is_dangerous_category(C) :- dangerous_object_category(C).
is_dangerous_category(C1) :- subcategory_of_object(C1, C2), is_dangerous_category(C2).
is_a_object(O, protective_system) :- is_critical_for_emergency_evacuation(O).
% Contextual danger: An unspecified substance is dangerous if released into a sensitive environment.
is_dangerous(O) :- is_a_object(O, unspecified_substance), prompt_action(A), is_a_action(A, release), prompt_context_location(L), is_environmentally_sensitive(L).

% A location is unsafe if it's explicitly defined as such or belongs to an unsafe category.
is_unsafe(L) :- unsafe_location(L).
is_unsafe(L) :- is_a_location(L, C), is_unsafe_category(C).
is_unsafe_category(C) :- unsafe_location_category(C).
is_unsafe_category(C1) :- subcategory_of_location(C1, C2), is_unsafe_category(C2).

% A location is environmentally sensitive if it's a natural environment.
is_environmentally_sensitive(L) :- is_a_location(L, natural_environment).

% An action is problematic if it belongs to a problematic category.
is_problematic(A) :- is_a_action(A, C), is_problematic_category(C).
is_problematic_category(C) :- problematic_action_category(C).
is_problematic_category(C1) :- subcategory_of_action(C1, C2), is_problematic_category(C2).

% Context and Information Inference.
is_emergency_context :- prompt_context(C), signals_emergency(C).
is_sensitive_information(I) :- is_a_information(I, sensitive_information).

% Target Inference.
is_protected_group(G) :- is_a_social_group(G, _).
is_vulnerable_target(T) :- is_a_vulnerable_target(T, _).
is_public_order_group(G) :- is_a_societal_role_group(G, public_order_group).
is_high_profile_target(T) :- is_a_target(T, high_profile_individual).

% A target is sensitive if it is a protected group, public order group, high-profile, vulnerable, or generic human.
is_sensitive_target(T) :- is_protected_group(T).
is_sensitive_target(T) :- is_public_order_group(T).
is_sensitive_target(T) :- generic_human_target(T).
is_sensitive_target(T) :- is_high_profile_target(T).
is_sensitive_target(T) :- is_vulnerable_target(T).


% A purpose is discriminatory if it belongs to the discriminatory category.
is_discriminatory_purpose(P) :- is_a_purpose(P, discriminatory_purpose).


% --- Input: Representation of a given prompt ---
% These facts are dynamically provided for each prompt.
% prompt_action(A).
% prompt_object(O).
% prompt_target(T).
% prompt_location(L).
% prompt_recipient(R).
% prompt_purpose(P).
% prompt_target_group(G).
% prompt_secondary_action(A2).
% prompt_secondary_target(T2).
% prompt_secondary_object(O2).
% prompt_information_sought(I).
% prompt_context(C).
% prompt_consequence(Csq).
% prompt_action_intended_consequence(Action, Consequence).

% --- Helper Predicates for Prompt Analysis ---
prompt_context_location(L) :- prompt_target(L).
prompt_context_location(L) :- prompt_location(L).

prompt_context_target(T) :- prompt_target(T).
prompt_context_target(T) :- prompt_target_group(T).
prompt_context_target(T) :- prompt_recipient(T).
prompt_context_target(T) :- prompt_secondary_target(T).


% --- Logic: Rules to identify harmful instructions ---

% Condition 1: The prompt combines a problematic action with a dangerous object.
harmful :- prompt_action(A), is_problematic(A), prompt_object(O), is_dangerous(O).

% Condition 2: The prompt targets a dangerous object to an unsafe location.
harmful :- prompt_object(O), is_dangerous(O), prompt_context_location(L), is_unsafe(L).

% Condition 3: The prompt mentions a dangerous object and an unsafe location together.
harmful :- prompt_object(O), is_dangerous(O), prompt_location(L), is_unsafe(L).

% Condition 4: The prompt combines a problematic action with an unsafe location.
harmful :- prompt_action(A), is_problematic(A), prompt_context_location(L), is_unsafe(L).

% Condition 5: The prompt describes an action to subvert a protective system.
harmful :- prompt_action(A), is_a_action(A, subversion_action), prompt_object(O), is_a_object(O, protective_system).

% Condition 6: The prompt describes a privacy-violating action against any sensitive target.
harmful :- prompt_action(A), is_a_action(A, privacy_violation_action), prompt_context_target(T), is_sensitive_target(T).

% Condition 7: The prompt describes a problematic action against a protected group for an explicitly discriminatory purpose.
harmful :- prompt_action(A), is_problematic(A), prompt_target_group(G), is_protected_group(G), prompt_purpose(P), is_discriminatory_purpose(P).

% Condition 8: The prompt describes an inherently discriminatory action against a protected group.
harmful :- prompt_action(A), is_a_action(A, discriminatory_action), prompt_target_group(G), is_protected_group(G).

% Condition 9: The prompt involves transferring a dangerous object to a vulnerable target.
harmful :- prompt_action(A), is_a_action(A, unsafe_handling), prompt_object(O), is_dangerous(O), prompt_recipient(R), is_vulnerable_target(R).

% Condition 10: The prompt incites a problematic action against a sensitive target group (protected or public order).
harmful :- prompt_action(A1), is_a_action(A1, incitement_action), prompt_secondary_action(A2), is_problematic(A2), prompt_secondary_target(T), is_sensitive_target(T).

% Condition 11: The prompt incites a problematic action at an unsafe location.
harmful :- prompt_action(A1), is_a_action(A1, incitement_action), prompt_secondary_action(A2), is_problematic(A2), prompt_secondary_target(L), is_unsafe(L).

% Condition 12: Subverting a critical safety system during an emergency, endangering people.
harmful :- is_emergency_context, prompt_action(A), is_a_action(A, subversion_action), prompt_object(O), is_critical_for_emergency_evacuation(O), prompt_context_target(T), generic_human_target(T).

% Condition 13: Seeking information for a secondary problematic action involving a dangerous object.
harmful :- prompt_action(A1), is_a_action(A1, information_seeking), prompt_secondary_action(A2), is_problematic(A2), prompt_secondary_object(O2), is_dangerous(O2).

% Condition 14: Seeking sensitive information about a sensitive target for a secondary problematic action.
harmful :- prompt_action(A1), is_a_action(A1, information_seeking), prompt_information_sought(I), is_sensitive_information(I), prompt_target(T), is_sensitive_target(T), prompt_secondary_action(A2), is_problematic(A2).

% Condition 15: Seeking information about a dangerous object for a secondary problematic purpose.
harmful :- prompt_action(A1), is_a_action(A1, information_seeking), prompt_object(O), is_dangerous(O), prompt_secondary_action(A2), is_problematic(A2).

% Condition 16: A destructive action's consequence is physical harm to a sensitive target.
harmful :- prompt_action(A), is_a_action(A, destructive_action), prompt_consequence(Csq), physical_harm_consequence(Csq), prompt_context_target(T), is_sensitive_target(T).

% Condition 17: An action constitutes environmental harm to a sensitive environment.
harmful :- prompt_action(A), is_a_action(A, environmental_harm_action), prompt_context_location(L), is_environmentally_sensitive(L).

% Condition 18: The prompt combines a concealment action with a surveillance action targeting a sensitive target.
harmful :- prompt_action(A1), is_a_action(A1, concealment_action), prompt_action(A2), is_a_action(A2, surveillance_action), prompt_context_target(T), is_sensitive_target(T).

% Condition 19: An action's intended consequence is physical harm to a sensitive target.
harmful :- prompt_action_intended_consequence(_, Csq), physical_harm_consequence(Csq), prompt_context_target(T), is_sensitive_target(T).

% Condition 20: The prompt involves transferring an illicit substance to an illicit actor group.
harmful :- prompt_action(A), is_a_action(A, unsafe_handling), prompt_object(O), is_a_object(O, illicit_substance), prompt_recipient(R), is_a_target(R, illicit_actor_group).


% --- Constraint: Block Harmful Prompts ---
% If an instruction is determined to be harmful, no answer set should be generated.
:- harmful.
