from lib.halpern_pearl import find_actual_causes, find_witnesses_ac2


def degree_of_responsibility(endogenous_variable, value, event, causal_setting):
    k_values = set()
    for actual_cause in find_actual_causes(event, causal_setting):
        if endogenous_variable in actual_cause and actual_cause[endogenous_variable] == value:  # if endogenous_variable=value is "part of" this cause
            k_values.add(min(len(witness) for witness in find_witnesses_ac2(actual_cause, event, causal_setting)))
    return 1 / min(k_values) if k_values else 0


def degrees_of_responsibility(event, causal_setting):
    return {endogenous_variable: {value: degree_of_responsibility(endogenous_variable, value, event, causal_setting) for value in domain} for endogenous_variable, domain in causal_setting.endogenous_domains.items()}
