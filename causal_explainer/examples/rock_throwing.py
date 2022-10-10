from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_ST': {False, True},
        'U_BT': {False, True}
    }
    endogenous_domains = {
        'ST': exogenous_domains['U_ST'],
        'BT': exogenous_domains['U_BT'],
        'SH': {False, True},
        'BH': {False, True},
        'BS': {False, True}
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('ST', ['U_ST'], lambda parent_values: parent_values['U_ST'])
    causal_network.add_dependency('BT', ['U_BT'], lambda parent_values: parent_values['U_BT'])
    causal_network.add_dependency('SH', ['ST'], lambda parent_values: parent_values['ST'])
    causal_network.add_dependency('BH', ['BT', 'SH'], lambda parent_values: parent_values['BT'] and not parent_values['SH'])
    causal_network.add_dependency('BS', ['SH', 'BH'], lambda parent_values: parent_values['SH'] or parent_values['BH'])
    context = {'U_ST': True, 'U_BT': True}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent('BS', True)

    causal_network.write("img/rock_throwing.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'ST': True}, {'BS': True}, {'SH': True}])
    assert actual_causes == expected_actual_causes
