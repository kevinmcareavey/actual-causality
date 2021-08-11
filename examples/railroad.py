from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
U_F, U_LB, U_RB = Variable("U_F"), Variable("U_LB"), Variable("U_RB")
F, LB, RB, A = Variable("F"), Variable("LB"), Variable("RB"), Variable("A")
exogenous_variables = {U_F, U_LB, U_RB}
endogenous_domains = {
    F: {False, True},
    LB: {False, True},
    RB: {False, True},
    A: {False, True}
}
causal_network = CausalNetwork()
causal_network.add_dependency(F, [U_F], lambda parent_values: parent_values[U_F])
causal_network.add_dependency(LB, [U_LB], lambda parent_values: parent_values[U_LB])
causal_network.add_dependency(RB, [U_RB], lambda parent_values: parent_values[U_RB])
causal_network.add_dependency(A, [F, LB, RB], lambda parent_values: (parent_values[F] and not parent_values[LB]) or (not parent_values[F] and not parent_values[RB]))
context = {U_F: True, U_LB: False, U_RB: False}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(A, True)
# list(find_actual_causes(event, causal_setting))
# degrees_of_responsibility(event, causal_setting)

causal_network.write("railroad.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{LB: False}, {F: True, RB: False}, {A: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {F: {True: 0.5, False: 0}, LB: {True: 0, False: 1.0}, RB: {True: 0, False: 0.5}, A: {True: 1.0, False: 0}}
assert actual_degrees_of_responsibility == expected_degrees_of_responsibility

