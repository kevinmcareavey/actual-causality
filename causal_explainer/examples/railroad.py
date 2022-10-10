from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_F': {False, True},
        'U_LB': {False, True},
        'U_RB': {False, True}
    }
    endogenous_domains = {
        'F': exogenous_domains['U_F'],
        'LB': exogenous_domains['U_LB'],
        'RB': exogenous_domains['U_RB'],
        'A': {False, True}
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('F', ['U_F'], lambda parent_values: parent_values['U_F'])
    causal_network.add_dependency('LB', ['U_LB'], lambda parent_values: parent_values['U_LB'])
    causal_network.add_dependency('RB', ['U_RB'], lambda parent_values: parent_values['U_RB'])
    causal_network.add_dependency('A', ['F', 'LB', 'RB'], lambda parent_values: (parent_values['F'] and not parent_values['LB']) or (not parent_values['F'] and not parent_values['RB']))
    context = {'U_F': True, 'U_LB': False, 'U_RB': False}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent('A', True)

    causal_network.write("img/railroad.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'LB': False}, {'F': True, 'RB': False}, {'A': True}])
    assert actual_causes == expected_actual_causes
