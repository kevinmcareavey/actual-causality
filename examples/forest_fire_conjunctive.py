from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, PrimitiveEvent
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
causal_network.add_dependency(FF, [L, MD], lambda parent_values: parent_values[L] and parent_values[MD])
causal_network.add_dependency(L, [U_L], lambda parent_values: parent_values[U_L])
causal_network.add_dependency(MD, [U_MD], lambda parent_values: parent_values[U_MD])
context = {U_L: True, U_MD: True}
causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
event = PrimitiveEvent(FF, True)
# list(find_actual_causes(event, causal_setting))

causal_network.write("forest_fire_conjunctive.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{FF: True}, {L: True}, {MD: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
