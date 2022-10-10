from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import issubdict, freeze

if __name__ == "__main__":
    exogenous_domains = {
        'U_L': {6, 7, 8},
        'U_S': {False, True},
        'U_E': {2, 5, 8},
        'U_C': {False, True},
        'U_W': {0, 2, 4},
        'U_A': {"spider", "beetle", "bee", "fly", "unknown"}
    }
    endogenous_domains = {
        'L': exogenous_domains['U_L'],
        'S': exogenous_domains['U_S'],
        'E': exogenous_domains['U_E'],
        'C': exogenous_domains['U_C'],
        'W': exogenous_domains['U_W'],
        'O': {"spider", "beetle", "bee", "fly", "unknown"},
        'A': exogenous_domains['U_A'],
        'V': {"pass", "fail"}
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
    causal_network.add_dependency('A', ['U_A'], lambda parent_values: parent_values['U_A'])
    causal_network.add_dependency('V', ['O', 'A'], lambda parent_values: "pass" if parent_values['O'] == parent_values['A'] or parent_values['O'] == "unknown" or parent_values['A'] == "unknown" else "fail")
    context = {'U_L': 7, 'U_S': False, 'U_E': 8, 'U_C': False, 'U_W': 0, 'U_A': "unknown"}
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent('V', "pass")

    causal_network.write("img/arthropods_classifier.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    expected_actual_causes = freeze([{'V': 'pass'}, {'O': 'unknown', 'A': 'unknown'}, {'L': 7, 'A': 'unknown'}])
    assert actual_causes == expected_actual_causes
