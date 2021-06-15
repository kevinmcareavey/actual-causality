from actualcausality.boolean_combinations import Atom, Conjunction, Disjunction
from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
u_v1, u_v2, u_v3 = Variable("U_V1"), Variable("U_V2"), Variable("U_V3")
v1, v2, v3, w = Variable("V1"), Variable("V2"), Variable("V3"), Variable("W")
exogenous_variables = {u_v1, u_v2, u_v3}
structural_equations = {
    v1: Atom(u_v1),
    v2: Atom(u_v2),
    v3: Atom(u_v3),
    w: Disjunction(Disjunction(Conjunction(Atom(v1), Atom(v2)), Conjunction(Atom(v1), Atom(v3))), Conjunction(Atom(v2), Atom(v3)))
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_v1: True, u_v2: True, u_v3: True}
causal_setting = CausalSetting(causal_model, context)
event = Atom(w)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("voting.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{v1: True, v2: True}, {v1: True, v3: True}, {v2: True, v3: True}, {w: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {v1: {True: 0.5, False: 0}, v2: {True: 0.5, False: 0}, v3: {True: 0.5, False: 0}, w: {True: 1.0, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility
