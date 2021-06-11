from actualcausality.boolean_combinations import Atom, Conjunction
from actualcausality.hp_definition import CausalModel, CausalSetting, Variable, find_actual_causes, degrees_of_responsibility
u_l, u_md = Variable("U_L"), Variable("U_MD")
ff, l, md = Variable("FF"), Variable("L"), Variable("MD")
exogenous_variables = {u_l, u_md}
structural_equations = {
    ff: Conjunction(Atom(l), Atom(md)),
    l: Atom(u_l),
    md: Atom(u_md)
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_l: True, u_md: True}
causal_setting = CausalSetting(causal_model, context)
event = Atom(ff)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("forest_fire_conjunctive.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{ff: True}, {l: True}, {md: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {l: {True: 1.0, False: 0}, ff: {True: 1.0, False: 0}, md: {True: 1.0, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility
