from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
U_V1, U_V2, U_V3 = Variable("U_V1"), Variable("U_V2"), Variable("U_V3")
V1, V2, V3, W = Variable("V1"), Variable("V2"), Variable("V3"), Variable("W")
exogenous_variables = {U_V1, U_V2, U_V3}
endogenous_domains = {
    V1: {False, True},
    V2: {False, True},
    V3: {False, True},
    W: {False, True}
}
causal_network = CausalNetwork()
causal_network.add_dependency(V1, [U_V1], lambda parent_values: parent_values[U_V1])
causal_network.add_dependency(V2, [U_V2], lambda parent_values: parent_values[U_V2])
causal_network.add_dependency(V3, [U_V3], lambda parent_values: parent_values[U_V3])
causal_network.add_dependency(W, [V1, V2, V3], lambda parent_values: ((parent_values[V1] and parent_values[V2]) or (parent_values[V1] and parent_values[V3])) or (parent_values[V2] and parent_values[V3]))
context = {U_V1: True, U_V2: True, U_V3: True}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(W, True)
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_network.write("voting.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{V1: True, V2: True}, {V1: True, V3: True}, {V2: True, V3: True}, {W: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {V1: {True: 0.5, False: 0}, V2: {True: 0.5, False: 0}, V3: {True: 0.5, False: 0}, W: {True: 1.0, False: 0}}
assert actual_degrees_of_responsibility == expected_degrees_of_responsibility
