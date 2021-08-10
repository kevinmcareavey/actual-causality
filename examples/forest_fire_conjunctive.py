from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
U_L, U_MD = Variable("U_L"), Variable("U_MD")
FF, L, MD = Variable("FF"), Variable("L"), Variable("MD")
exogenous_variables = {U_L, U_MD}
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
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(FF, True)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_network.write("forest_fire_conjunctive.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{FF: True}, {L: True}, {MD: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {L: {True: 1.0, False: 0}, FF: {True: 1.0, False: 0}, MD: {True: 1.0, False: 0}}
assert actual_degrees_of_responsibility == expected_degrees_of_responsibility
