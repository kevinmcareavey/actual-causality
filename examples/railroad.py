from actualcausality.boolean_combinations import Atom, Conjunction, Negation, Disjunction
from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
u_f, u_lb, u_rb = Variable("U_F"), Variable("U_LB"), Variable("U_RB")
f, lb, rb, a = Variable("F"), Variable("LB"), Variable("RB"), Variable("A")
exogenous_variables = {u_f, u_lb, u_rb}
structural_equations = {
    f: Atom(u_f),
    lb: Atom(u_lb),
    rb: Atom(u_rb),
    a: Disjunction(Conjunction(Atom(f), Negation(Atom(lb))), Conjunction(Negation(Atom(f)), Negation(Atom(rb))))
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_f: True, u_lb: False, u_rb: False}
causal_setting = CausalSetting(causal_model, context)
event = Atom(a)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("railroad.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{lb: False}, {f: True, rb: False}, {a: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {f: {True: 0.5, False: 0}, lb: {True: 0, False: 1.0}, rb: {True: 0, False: 0.5}, a: {True: 1.0, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility

