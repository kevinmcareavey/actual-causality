from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
from actualcausality.utils import issubdict
U_L, U_S, U_E, U_C, U_W = Variable("U_L"), Variable("U_S"), Variable("U_E"), Variable("U_C"), Variable("U_W")
L, S, E, C, W, O = Variable("L"), Variable("S"), Variable("E"), Variable("C"), Variable("W"), Variable("O")
exogenous_variables = {U_L, U_S, U_E, U_C, U_W}
endogenous_domains = {
    L: {6, 8},
    S: {False, True},
    E: {2, 5, 8},
    C: {False, True},
    W: {0, 2, 4},
    O: {"spider", "beetle", "bee", "fly", "unknown"}
}
causal_network = CausalNetwork()
causal_network.add_dependency(L, [U_L], lambda parent_values: parent_values[U_L])
causal_network.add_dependency(S, [U_S], lambda parent_values: parent_values[U_S])
causal_network.add_dependency(E, [U_E], lambda parent_values: parent_values[U_E])
causal_network.add_dependency(C, [U_C], lambda parent_values: parent_values[U_C])
causal_network.add_dependency(W, [U_W], lambda parent_values: parent_values[U_W])
causal_network.add_dependency(
    O,
    [L, S, E, C, W],
    lambda parent_values:
        "spider" if issubdict({L: 8, S: False, E: 8, C: False, W: 0}, parent_values)
        else "beetle" if issubdict({L: 6, S: False, E: 2, C: True, W: 2}, parent_values)
        else "bee" if issubdict({L: 6, S: True, E: 5, C: True, W: 4}, parent_values)
        else "fly" if issubdict({L: 6, S: False, E: 5, C: True, W: 2}, parent_values)
        else "unknown"
)
context = {U_L: 6, U_S: True, U_E: 5, U_C: True, U_W: 4}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(O, "bee")
# list(find_actual_causes(event, causal_setting))
# degrees_of_responsibility(event, causal_setting)

causal_network.write("arthropods.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{L: 6}, {S: True}, {C: True}, {O: 'bee'}, {W: 4}, {E: 5}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {L: {8: 0, 6: 1.0}, S: {False: 0, True: 1.0}, E: {8: 0, 2: 0, 5: 1.0}, C: {False: 0, True: 1.0}, W: {0: 0, 2: 0, 4: 1.0}, O: {'unknown': 0, 'bee': 1.0, 'beetle': 0, 'fly': 0, 'spider': 0}}
assert degrees_of_responsibility(event, causal_setting) == expected_degrees_of_responsibility

# contexts = {
#     "spider": {U_L: 8, U_S: False, U_E: 8, U_C: False, U_W: 0},
#     "beetle": {U_L: 6, U_S: False, U_E: 2, U_C: True, U_W: 2},
#     "bee": {U_L: 6, U_S: True, U_E: 5, U_C: True, U_W: 4},
#     "fly": {U_L: 6, U_S: False, U_E: 5, U_C: True, U_W: 2},
# }
#
# actual_causes = dict()
# actual_degrees_of_responsibility = dict()
# for arthropod, context in contexts.items():
#     causal_setting = CausalSetting(causal_network, context, endogenous_domains)
#     event = PrimitiveEvent(O, arthropod)
#     actual_causes[arthropod] = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
#     actual_degrees_of_responsibility[arthropod] = degrees_of_responsibility(event, causal_setting)
#
# causal_network.write("arthropods.png")
#
# expected_causes = {'spider': [{C: False}, {L: 8}, {O: 'spider'}, {E: 8}, {W: 0}, {S: False}], 'beetle': [{C: True}, {L: 6}, {O: 'beetle'}, {E: 2}, {W: 2}, {S: False}], 'bee': [{C: True}, {L: 6}, {O: 'bee'}, {E: 5}, {W: 4}, {S: True}], 'fly': [{C: True}, {L: 6}, {O: 'fly'}, {E: 5}, {W: 2}, {S: False}]}
# for arthropod in contexts.keys():
#     assert actual_causes[arthropod] == {frozendict(expected_cause) for expected_cause in expected_causes[arthropod]}
# expected_degrees_of_responsibility = {'spider': {L: {8: 1.0, 6: 0}, S: {False: 1.0, True: 0}, E: {8: 1.0, 2: 0, 5: 0}, C: {False: 1.0, True: 0}, W: {0: 1.0, 2: 0, 4: 0}, O: {'beetle': 0, 'spider': 1.0, 'unknown': 0, 'fly': 0, 'bee': 0}}, 'beetle': {L: {8: 0, 6: 1.0}, S: {False: 1.0, True: 0}, E: {8: 0, 2: 1.0, 5: 0}, C: {False: 0, True: 1.0}, W: {0: 0, 2: 1.0, 4: 0}, O: {'beetle': 1.0, 'spider': 0, 'unknown': 0, 'fly': 0, 'bee': 0}}, 'bee': {L: {8: 0, 6: 1.0}, S: {False: 0, True: 1.0}, E: {8: 0, 2: 0, 5: 1.0}, C: {False: 0, True: 1.0}, W: {0: 0, 2: 0, 4: 1.0}, O: {'beetle': 0, 'spider': 0, 'unknown': 0, 'fly': 0, 'bee': 1.0}}, 'fly': {L: {8: 0, 6: 1.0}, S: {False: 1.0, True: 0}, E: {8: 0, 2: 0, 5: 1.0}, C: {False: 0, True: 1.0}, W: {0: 0, 2: 1.0, 4: 0}, O: {'beetle': 0, 'spider': 0, 'unknown': 0, 'fly': 1.0, 'bee': 0}}}
# for arthropod in contexts.keys():
#     assert actual_degrees_of_responsibility[arthropod] == expected_degrees_of_responsibility[arthropod]
