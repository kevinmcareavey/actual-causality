from actualcausality.boolean_combinations import Atom, Disjunction, Negation
from actualcausality.hp_definition import CausalModel, CausalSetting, Variable, find_actual_causes, CausalFormula, degrees_of_responsibility
u_l, u_md = Variable("U_L"), Variable("U_MD")
ff, l, md = Variable("FF"), Variable("L"), Variable("MD")
exogenous_variables = {u_l, u_md}
structural_equations = {
    ff: Disjunction(Atom(l), Atom(md)),
    l: Atom(u_l),
    md: Atom(u_md)
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_l: True, u_md: True}
causal_setting = CausalSetting(causal_model, context)
event = Atom(ff)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("forest_fire_disjunctive.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{ff: True}, {l: True, md: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {l: {True: 0.5, False: 0}, ff: {True: 1.0, False: 0}, md: {True: 0.5, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility

assert CausalFormula({md: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({l: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({l: False, md: False}, Negation(event)).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]
