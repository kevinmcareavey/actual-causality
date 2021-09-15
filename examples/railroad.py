from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, PrimitiveEvent
U_F, U_LB, U_RB = Variable("U_F"), Variable("U_LB"), Variable("U_RB")
F, LB, RB, A = Variable("F"), Variable("LB"), Variable("RB"), Variable("A")
exogenous_domains = {
    U_F: {False, True},
    U_LB: {False, True},
    U_RB: {False, True}
}
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
causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
event = PrimitiveEvent(A, True)
# list(find_actual_causes(event, causal_setting))

causal_network.write("railroad.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_actual_causes = [{LB: False}, {F: True, RB: False}, {A: True}]
assert actual_causes == {frozendict(expected_actual_cause) for expected_actual_cause in expected_actual_causes}
