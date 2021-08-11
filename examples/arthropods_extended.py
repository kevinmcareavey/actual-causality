from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes
from actualcausality.utils import issubdict
U_L, U_S, U_E, U_C, U_W, U_A = Variable("U_L"), Variable("U_S"), Variable("U_E"), Variable("U_C"), Variable("U_W"), Variable("U_A")
L, S, E, C, W, O, A, V = Variable("L"), Variable("S"), Variable("E"), Variable("C"), Variable("W"), Variable("O"), Variable("A"), Variable("V")
exogenous_variables = {U_L, U_S, U_E, U_C, U_W}
endogenous_domains = {
    L: {6, 7, 8},
    S: {False, True},
    E: {2, 5, 8},
    C: {False, True},
    W: {0, 2, 4},
    O: {"spider", "beetle", "bee", "fly", "unknown"},
    A: {"spider", "beetle", "bee", "fly", "unknown"},
    V: {"pass", "fail"}
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
causal_network.add_dependency(A, [U_A], lambda parent_values: parent_values[U_A])
causal_network.add_dependency(V, [O, A], lambda parent_values: "pass" if parent_values[O] == parent_values[A] or parent_values[O] == "unknown" or parent_values[A] == "unknown" else "fail")
context = {U_L: 7, U_S: False, U_E: 8, U_C: False, U_W: 0, U_A: "unknown"}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(V, "pass")
# list(find_actual_causes(event, causal_setting))

causal_network.write("arthropods_extended.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{V: 'pass'}, {O: 'unknown', A: 'unknown'}, {L: 7, A: 'unknown'}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
