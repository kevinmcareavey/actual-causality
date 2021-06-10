from actualcausality.boolean_combinations import Atom, Conjunction
from actualcausality.hp_definition import CausalModel, CausalSetting, Variable, find_actual_causes
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
find_actual_causes(event, causal_setting, expected_causes=[{ff: True}, {l: True}, {md: True}])

causal_model.causal_network().draw("forest_fire_conjunctive.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop
