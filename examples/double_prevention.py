from actualcausality.boolean_combinations import Atom, Negation, Conjunction
from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
u_bgu, u_esu = Variable("U_BGU"), Variable("U_ESU")
bgu, esu, bpt, ee, ess, sbt, td = Variable("BGU"), Variable("ESU"), Variable("BPT"), Variable("EE"), Variable("ESS"), Variable("SBT"), Variable("TD")
exogenous_variables = {u_bgu, u_esu}
structural_equations = {
    bgu: Atom(u_bgu),
    esu: Atom(u_esu),
    bpt: Conjunction(Atom(bgu), Atom(esu)),
    ee: Conjunction(Atom(esu), Negation(Atom(bpt))),
    ess: Atom(ee),
    sbt: Negation(Atom(ess)),
    td: Atom(sbt)
}
causal_model = CausalModel(exogenous_variables, structural_equations)
context = {u_bgu: True, u_esu: False}
causal_setting = CausalSetting(causal_model, context)
event = Atom(td)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_model.causal_network().draw("double_prevention.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

expected_causes = [{esu: False}, {ee: False}, {ess: False}, {sbt: True}, {td: True}]
assert {frozenset(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)} == {frozenset(expected_cause) for expected_cause in expected_causes}
expected_degrees_of_responsibility = {bgu: {True: 0, False: 0}, esu: {True: 0, False: 0.5}, bpt: {True: 0, False: 0}, ee: {True: 0, False: 1.0}, ess: {True: 0, False: 1.0}, sbt: {True: 1.0, False: 0}, td: {True: 1.0, False: 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility

