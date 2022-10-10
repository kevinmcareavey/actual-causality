from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause, is_sufficient_cause
from causal_explainer.halpern_pearl.explanations import EpistemicState, search_candidate_explanations, is_explanation, \
    is_trivial_explanation, is_nontrivial_explanation
from causal_explainer.utils import freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_L': {False, True},
        'U_MD': {False, True}
    }
    endogenous_domains = {
        'FF': {False, True},
        'L': exogenous_domains['U_L'],
        'MD': exogenous_domains['U_MD']
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('FF', ['L', 'MD'], lambda parent_values: parent_values['L'] and parent_values['MD'])
    causal_network.add_dependency('L', ['U_L'], lambda parent_values: parent_values['U_L'])
    causal_network.add_dependency('MD', ['U_MD'], lambda parent_values: parent_values['U_MD'])
    context = {'U_L': True, 'U_MD': True}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent('FF', True)

    causal_network.write("img/forest_fire_conjunctive.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'FF': True}, {'L': True}, {'MD': True}])
    assert actual_causes == expected_actual_causes

    sufficient_causes = freeze(search_candidate_causes(event, causal_setting, is_sufficient_cause))
    expected_sufficient_causes = freeze([{'FF': True}, {'L': True, 'MD': True}])
    assert sufficient_causes == expected_sufficient_causes

    u0 = {'U_L': False, 'U_MD': False}
    u1 = {'U_L': True, 'U_MD': False}
    u2 = {'U_L': False, 'U_MD': True}
    u3 = {'U_L': True, 'U_MD': True}
    k1 = EpistemicState(causal_network, [u0, u1, u2, u3], exogenous_domains, endogenous_domains)
    k2 = EpistemicState(causal_network, [u0, u1, u2], exogenous_domains, endogenous_domains)
    k3 = EpistemicState(causal_network, [u0, u1, u3], exogenous_domains, endogenous_domains)
    k4 = EpistemicState(causal_network, [u1, u3], exogenous_domains, endogenous_domains)
    epistemic_states = [k1, k2, k3, k4]

    explanations = [freeze(search_candidate_explanations(event, epistemic_state, is_explanation)) for epistemic_state in epistemic_states]
    expected_explanations = [
        freeze([{'FF': True}, {'L': True, 'MD': True}]),
        freeze([]),
        freeze([{'FF': True}, {'L': True, 'MD': True}]),
        freeze([{'FF': True}, {'MD': True}])
    ]
    assert explanations == expected_explanations

    trivial_explanations = [freeze(search_candidate_explanations(event, epistemic_state, is_trivial_explanation)) for epistemic_state in epistemic_states]
    expected_trivial_explanations = [
        freeze([{'FF': True}, {'L': True, 'MD': True}]),
        freeze([]),
        freeze([{'FF': True}, {'L': True, 'MD': True}]),
        freeze([{'FF': True}, {'MD': True}])
    ]
    assert trivial_explanations == expected_trivial_explanations

    nontrivial_explanations = [freeze(search_candidate_explanations(event, epistemic_state, is_nontrivial_explanation)) for epistemic_state in epistemic_states]
    expected_nontrivial_explanations = [freeze([]) for _ in epistemic_states]
    assert nontrivial_explanations == expected_nontrivial_explanations
