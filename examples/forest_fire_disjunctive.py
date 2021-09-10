from frozendict import frozendict
from lib.chockler_halpern import degrees_of_responsibility
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, CausalFormula, PrimitiveEvent, Negation
U_L, U_MD = Variable("U_L"), Variable("U_MD")
FF, L, MD = Variable("FF"), Variable("L"), Variable("MD")
exogenous_domains = {
    U_L: {False, True},
    U_MD: {False, True}
}
endogenous_domains = {
    FF: {False, True},
    L: {False, True},
    MD: {False, True}
}
causal_network = CausalNetwork()
causal_network.add_dependency(FF, [L, MD], lambda parent_values: parent_values[L] or parent_values[MD])
causal_network.add_dependency(L, [U_L], lambda parent_values: parent_values[U_L])
causal_network.add_dependency(MD, [U_MD], lambda parent_values: parent_values[U_MD])
context = {U_L: True, U_MD: True}
causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
event = PrimitiveEvent(FF, True)
# list(find_actual_causes(event, causal_setting))

causal_network.write("forest_fire_disjunctive.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{FF: True}, {L: True, MD: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}

assert CausalFormula({MD: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({L: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({L: False, MD: False}, Negation(event)).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]
