from causal_explainer.halpern_pearl.causes import CausalNetwork, Disjunction, PrimitiveEvent
from causal_explainer.halpern_pearl.explanations import EpistemicState, search_candidate_explanations, is_explanation, \
    is_trivial_explanation, is_nontrivial_explanation
from causal_explainer.utils import freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_AS': {False, True},
        'U_ES_M': {False, True},
        'U_ES_J': {False, True}
    }
    endogenous_domains = {
        'AS': exogenous_domains['U_AS'],
        'ES_M': exogenous_domains['U_ES_M'],
        'ES_J': exogenous_domains['U_ES_J'],
        'FF_M': {False, True},
        'FF_J': {False, True}
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('AS', ['U_AS'], lambda parent_values: parent_values['U_AS'])
    causal_network.add_dependency('ES_M', ['U_ES_M'], lambda parent_values: parent_values['U_ES_M'])
    causal_network.add_dependency('ES_J', ['U_ES_J'], lambda parent_values: parent_values['U_ES_J'])
    causal_network.add_dependency('FF_M', ['AS', 'ES_M'], lambda parent_values: parent_values['ES_M'] and not parent_values['AS'])
    causal_network.add_dependency('FF_J', ['AS', 'ES_M', 'ES_J'], lambda parent_values: parent_values['ES_J'] and (parent_values['AS'] or not parent_values['ES_M']))
    # explanandum = PrimitiveEvent('FF_M', True)
    # explanandum = PrimitiveEvent('FF_J', True)
    explanandum = Disjunction(PrimitiveEvent('FF_M', True), PrimitiveEvent('FF_J', True))

    causal_network.write("img/weather.png")

    u0 = {'U_AS': False, 'U_ES_M': False, 'U_ES_J': False}
    u1 = {'U_AS': True, 'U_ES_M': False, 'U_ES_J': False}
    u2 = {'U_AS': False, 'U_ES_M': True, 'U_ES_J': False}
    u3 = {'U_AS': True, 'U_ES_M': True, 'U_ES_J': False}
    u4 = {'U_AS': False, 'U_ES_M': False, 'U_ES_J': True}
    u5 = {'U_AS': True, 'U_ES_M': False, 'U_ES_J': True}
    u6 = {'U_AS': False, 'U_ES_M': True, 'U_ES_J': True}
    u7 = {'U_AS': True, 'U_ES_M': True, 'U_ES_J': True}
    k0 = EpistemicState(causal_network, [u0, u1, u2, u3, u4, u5, u6, u7], exogenous_domains, endogenous_domains)
    k1 = EpistemicState(causal_network, [u2, u4, u6, u5, u7], exogenous_domains, endogenous_domains)
    epistemic_states = [k0, k1]

    explanations = [freeze(search_candidate_explanations(explanandum, epistemic_state, is_explanation)) for epistemic_state in epistemic_states]
    expected_explanations = [
        freeze([{'AS': False, 'ES_M': True}, {'AS': False, 'ES_J': True}, {'AS': True, 'ES_J': True}, {'ES_J': True, 'ES_M': False}, {'ES_J': True, 'ES_M': True}, {'FF_M': True}, {'FF_J': True}]),
        freeze([{'AS': False, 'ES_M': True}, {'AS': False, 'ES_J': True}, {'AS': True, 'ES_J': True}, {'ES_J': True, 'ES_M': False}, {'ES_J': True, 'ES_M': True}, {'FF_M': True}, {'FF_J': True}])
    ]
    assert explanations == expected_explanations

    explanations = [freeze(search_candidate_explanations(explanandum, epistemic_state, is_trivial_explanation)) for epistemic_state in epistemic_states]
    expected_explanations = [
        freeze([]),
        freeze([])
    ]
    assert explanations == expected_explanations

    explanations = [freeze(search_candidate_explanations(explanandum, epistemic_state, is_nontrivial_explanation)) for epistemic_state in epistemic_states]
    expected_explanations = [
        freeze([{'AS': False, 'ES_M': True}, {'AS': False, 'ES_J': True}, {'AS': True, 'ES_J': True}, {'ES_J': True, 'ES_M': False}, {'ES_J': True, 'ES_M': True}, {'FF_M': True}, {'FF_J': True}]),
        freeze([{'AS': False, 'ES_M': True}, {'AS': False, 'ES_J': True}, {'AS': True, 'ES_J': True}, {'ES_J': True, 'ES_M': False}, {'ES_J': True, 'ES_M': True}, {'FF_M': True}, {'FF_J': True}])
    ]
    assert explanations == expected_explanations
