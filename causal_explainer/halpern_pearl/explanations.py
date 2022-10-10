from causal_explainer.halpern_pearl.causes import CausalSetting, Conjunction, assignments2conjunction, satisfies_sc2, \
    CausalFormula, Negation, find_all_assignments
from causal_explainer.utils import powerdict


class EpistemicState:
    def __init__(self, causal_network, contexts, exogenous_domains, endogenous_domains):
        self.causal_network = causal_network
        self.contexts = contexts
        self.exogenous_domains = exogenous_domains
        self.endogenous_domains = endogenous_domains

    def causal_settings(self):
        for context in self.contexts:
            yield CausalSetting(self.causal_network, context, self.exogenous_domains, self.endogenous_domains)


def satisfies_ex1(candidate, event, epistemic_state):
    for causal_setting in epistemic_state.causal_settings():
        if Conjunction(assignments2conjunction(candidate), event).entailed_by(causal_setting):
            if not satisfies_sc2(candidate, event, causal_setting):
                return False
        if not CausalFormula(candidate, event).entailed_by(causal_setting):
            return False
    return True


def satisfies_ex2(candidate, event, epistemic_state):
    for subset_candidate in powerdict(candidate):
        if subset_candidate and subset_candidate != candidate:
            if satisfies_ex1(subset_candidate, event, epistemic_state):
                return False
    return True


def satisfies_ex3(candidate, event, epistemic_state):
    for causal_setting in epistemic_state.causal_settings():
        if Conjunction(assignments2conjunction(candidate), event).entailed_by(causal_setting):
            return True
    return False


def satisfies_ex4(candidate, event, epistemic_state):
    for causal_setting in epistemic_state.causal_settings():
        if event.entailed_by(causal_setting):
            if Negation(assignments2conjunction(candidate)).entailed_by(causal_setting):
                return True
    return False


def is_explanation(candidate, event, epistemic_state):
    if not satisfies_ex1(candidate, event, epistemic_state):
        return False
    if not satisfies_ex2(candidate, event, epistemic_state):
        return False
    if not satisfies_ex3(candidate, event, epistemic_state):
        return False
    return True


def is_nontrivial_explanation(candidate, event, epistemic_state):
    if not is_explanation(candidate, event, epistemic_state):
        return False
    if not satisfies_ex4(candidate, event, epistemic_state):
        return False
    return True


def is_trivial_explanation(candidate, event, epistemic_state):
    if not is_explanation(candidate, event, epistemic_state):
        return False
    if satisfies_ex4(candidate, event, epistemic_state):
        return False
    return True


def search_candidate_explanations(event, epistemic_state, condition):
    for candidate in find_all_assignments(epistemic_state.endogenous_domains):
        if condition(candidate, event, epistemic_state):
            yield candidate