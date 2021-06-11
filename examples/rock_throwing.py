from actualcausality.boolean_combinations import Atom, Conjunction, Negation, Disjunction
from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
u_st, u_bt = Variable("U_ST"), Variable("U_BT")
st, bt, sh, bh, bs = Variable("ST"), Variable("BT"), Variable("SH"), Variable("BH"), Variable("BS")
exogenous_variables = {u_st, u_bt}
structural_equations = {
    st: Atom(u_st),
    bt: Atom(u_bt),
    sh: Atom(st),
    bh: Conjunction(Atom(bt), Negation(Atom(sh))),
    bs: Disjunction(Atom(sh), Atom(bh))
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_st: True, u_bt: True}
causal_setting = CausalSetting(causal_model, context)
event = Atom(bs)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("rock_throwing.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{st: True}, {bs: True}, {sh: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {st: {True: 0.5, False: 0}, bt: {True: 0, False: 0}, bs: {True: 1.0, False: 0}, sh: {True: 0.5, False: 0}, bh: {True: 0, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility

