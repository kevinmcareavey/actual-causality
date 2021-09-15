from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, CausalFormula, PrimitiveEvent, \
    Negation, find_trivial_explanations, EpistemicState, find_nontrivial_explanations, find_explanations, \
    find_sufficient_causes

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
expected_actual_causes = [{FF: True}, {L: True, MD: True}]
assert actual_causes == {frozendict(expected_actual_cause) for expected_actual_cause in expected_actual_causes}

sufficient_causes = {frozendict(sufficient_cause) for sufficient_cause in find_sufficient_causes(event, causal_setting)}
expected_sufficient_causes = [{FF: True}, {L: True}, {FF: True, L: True}, {MD: True}, {FF: True, MD: True}, {L: True, MD: True}, {FF: True, L: True, MD: True}]
assert sufficient_causes == {frozendict(expected_sufficient_cause) for expected_sufficient_cause in expected_sufficient_causes}

assert CausalFormula({MD: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({L: False}, event).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
assert CausalFormula({L: False, MD: False}, Negation(event)).entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]

u0 = {U_L: False, U_MD: False}
u1 = {U_L: True, U_MD: False}
u2 = {U_L: False, U_MD: True}
u3 = {U_L: True, U_MD: True}
k1 = EpistemicState(causal_network, [u0, u1, u2, u3], exogenous_domains, endogenous_domains)
k2 = EpistemicState(causal_network, [u0, u1, u2], exogenous_domains, endogenous_domains)
k3 = EpistemicState(causal_network, [u0, u1, u3], exogenous_domains, endogenous_domains)
k4 = EpistemicState(causal_network, [u1, u3], exogenous_domains, endogenous_domains)
epistemic_states = [k1, k2, k3, k4]

explanations = [{frozendict(explanation) for explanation in find_explanations(event, epistemic_state)} for epistemic_state in epistemic_states]
expected_explanations = [
    [{FF: True}, {L: True}, {MD: True}],
    [{FF: True}, {L: True}, {MD: True}],
    [{FF: True}, {L: True}, {MD: True}],
    [{FF: True}, {L: True}, {MD: True}]
]
assert explanations == [{frozendict(expected_explanation) for expected_explanation in epistemic_state} for epistemic_state in expected_explanations]

trivial_explanations = [{frozendict(trivial_explanation) for trivial_explanation in find_trivial_explanations(event, epistemic_state)} for epistemic_state in epistemic_states]
expected_trivial_explanations = [
    [{FF: True}],
    [{FF: True}],
    [{FF: True}, {L: True}],
    [{FF: True}, {L: True}]
]
assert trivial_explanations == [{frozendict(expected_trivial_explanation) for expected_trivial_explanation in epistemic_state} for epistemic_state in expected_trivial_explanations]

nontrivial_explanations = [{frozendict(nontrivial_explanation) for nontrivial_explanation in find_nontrivial_explanations(event, epistemic_state)} for epistemic_state in epistemic_states]
expected_nontrivial_explanations = [
    [{L: True}, {MD: True}],
    [{L: True}, {MD: True}],
    [{MD: True}],
    [{MD: True}]
]
assert nontrivial_explanations == [{frozendict(expected_nontrivial_explanation) for expected_nontrivial_explanation in epistemic_state} for epistemic_state in expected_nontrivial_explanations]
