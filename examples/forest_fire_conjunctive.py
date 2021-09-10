from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, PrimitiveEvent, \
    find_trivial_explanations, find_nontrivial_explanations, EpistemicState

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

u0 = {U_L: False, U_MD: False}
u1 = {U_L: True, U_MD: False}
u2 = {U_L: False, U_MD: True}
u3 = {U_L: True, U_MD: True}
k1 = EpistemicState(causal_network, [u0, u1, u2, u3], exogenous_domains, endogenous_domains)
k2 = EpistemicState(causal_network, [u0, u1, u2], exogenous_domains, endogenous_domains)
k3 = EpistemicState(causal_network, [u0, u1, u3], exogenous_domains, endogenous_domains)
k4 = EpistemicState(causal_network, [u1, u3], exogenous_domains, endogenous_domains)
epistemic_states = [k1, k2, k3, k4]

trivial_explanations = [{frozendict(trivial_explanation) for trivial_explanation in find_trivial_explanations(event, epistemic_state)} for epistemic_state in epistemic_states]
expected_trivial_explanations = [
    [{FF: True}, {L: True, MD: True}],
    [],
    [{FF: True}, {L: True, MD: True}],
    [{FF: True}, {MD: True}]
]
assert trivial_explanations == [{frozendict(expected_trivial_explanation) for expected_trivial_explanation in epistemic_state} for epistemic_state in expected_trivial_explanations]

nontrivial_explanations = [{frozendict(nontrivial_explanation) for nontrivial_explanation in find_nontrivial_explanations(event, epistemic_state)} for epistemic_state in epistemic_states]
expected_nontrivial_explanations = [[] for _ in epistemic_states]
assert nontrivial_explanations == [{frozendict(expected_nontrivial_explanation) for expected_nontrivial_explanation in epistemic_state} for epistemic_state in expected_nontrivial_explanations]
