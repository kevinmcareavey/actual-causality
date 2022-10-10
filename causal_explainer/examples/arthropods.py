from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import issubdict, freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_L': {6, 8},
        'U_S': {False, True},
        'U_E': {2, 5, 8},
        'U_C': {False, True},
        'U_W': {0, 2, 4}
    }
    endogenous_domains = {
        'L': exogenous_domains['U_L'],
        'S': exogenous_domains['U_S'],
        'E': exogenous_domains['U_E'],
        'C': exogenous_domains['U_C'],
        'W': exogenous_domains['U_W'],
        'O': {"spider", "beetle", "bee", "fly", "unknown"}
    }
    causal_network = CausalNetwork()
    causal_network.add_dependency('L', ['U_L'], lambda parent_values: parent_values['U_L'])
    causal_network.add_dependency('S', ['U_S'], lambda parent_values: parent_values['U_S'])
    causal_network.add_dependency('E', ['U_E'], lambda parent_values: parent_values['U_E'])
    causal_network.add_dependency('C', ['U_C'], lambda parent_values: parent_values['U_C'])
    causal_network.add_dependency('W', ['U_W'], lambda parent_values: parent_values['U_W'])
    causal_network.add_dependency(
        'O',
        ['L', 'S', 'E', 'C', 'W'],
        lambda parent_values:
            "spider" if issubdict({'L': 8, 'S': False, 'E': 8, 'C': False, 'W': 0}, parent_values)
            else "beetle" if issubdict({'L': 6, 'S': False, 'E': 2, 'C': True, 'W': 2}, parent_values)
            else "bee" if issubdict({'L': 6, 'S': True, 'E': 5, 'C': True, 'W': 4}, parent_values)
            else "fly" if issubdict({'L': 6, 'S': False, 'E': 5, 'C': True, 'W': 2}, parent_values)
            else "unknown"
    )
    context = {'U_L': 6, 'U_S': True, 'U_E': 5, 'U_C': True, 'U_W': 4}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    fact = PrimitiveEvent('O', "bee")
    foil = PrimitiveEvent('O', "fly")
    explanandum = fact, foil

    causal_network.write("img/arthropods.png")

    actual_causes = freeze(search_candidate_causes(fact, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'L': 6}, {'S': True}, {'E': 5}, {'C': True}, {'W': 4}, {'O': "bee"}])
    assert actual_causes == expected_actual_causes
