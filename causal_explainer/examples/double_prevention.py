from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_BGU': {False, True},
        'U_ESU': {False, True}
    }
    endogenous_domains = {
        'BGU': exogenous_domains['U_BGU'],
        'ESU': exogenous_domains['U_ESU'],
        'BPT': {False, True},
        'EE': {False, True},
        'ESS': {False, True},
        'SBT': {False, True},
        'TD': {False, True}
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('BGU', ['U_BGU'], lambda parent_values: parent_values['U_BGU'])
    causal_network.add_dependency('ESU', ['U_ESU'], lambda parent_values: parent_values['U_ESU'])
    causal_network.add_dependency('BPT', ['BGU', 'ESU'], lambda parent_values: parent_values['BGU'] and parent_values['ESU'])
    causal_network.add_dependency('EE', ['ESU', 'BPT'], lambda parent_values: parent_values['ESU'] and not parent_values['BPT'])
    causal_network.add_dependency('ESS', ['EE'], lambda parent_values: parent_values['EE'])
    causal_network.add_dependency('SBT', ['ESS'], lambda parent_values: not parent_values['ESS'])
    causal_network.add_dependency('TD', ['SBT'], lambda parent_values: parent_values['SBT'])
    context = {'U_BGU': True, 'U_ESU': False}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent('TD', True)

    causal_network.write("img/double_prevention.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'ESU': False}, {'EE': False}, {'ESS': False}, {'SBT': True}, {'TD': True}])
    assert actual_causes == expected_actual_causes
