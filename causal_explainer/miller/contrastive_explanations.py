import logging

from causal_explainer.halpern_pearl.causes import find_all_assignments
from causal_explainer.halpern_pearl.explanations import search_candidate_explanations, is_explanation, EpistemicState
from causal_explainer.miller.contrastive_causes import difference_condition, find_exact_assignment_pairs, find_all_assignment_pairs
from causal_explainer.utils import issubdict, powerset

logger = logging.getLogger("explanations")
logging.basicConfig(level=logging.INFO)


def is_partial_explanation(candidate, event, epistemic_state, nontrivial=False):  # nontrivial=False permits trivial explanations
    if candidate:
        for explanation in search_candidate_explanations(event, epistemic_state, is_nontrivial_explanation) if nontrivial else search_candidate_explanations(event, epistemic_state, is_explanation):
            if issubdict(candidate, explanation):
                logger.debug(f"\t\t\t{candidate} is partial {'nontrivial' if nontrivial else ''} explanation of {event} due to {'nontrivial' if nontrivial else ''} explanation {explanation}")
                return True
    return False


def satisfies_ce1(candidate_pair, event_pair, epistemic_state, **kwargs):
    candidate, _ = candidate_pair
    fact, _ = event_pair
    return is_partial_explanation(candidate, fact, epistemic_state, **kwargs)


def satisfies_ce2(candidate_pair, event_pair, epistemic_state, **kwargs):
    _, candidate_alt = candidate_pair
    _, foil = event_pair
    for w in find_all_assignments(epistemic_state.endogenous_domains):
        new_causal_network = epistemic_state.causal_network.intervene(w)
        new_epistemic_state = EpistemicState(new_causal_network, epistemic_state.contexts, epistemic_state.exogenous_domains, epistemic_state.endogenous_domains)
        if is_partial_explanation(candidate_alt, foil, new_epistemic_state, **kwargs):
            return True
    return False


def satisfies_ce3(candidate_pair):
    return difference_condition(candidate_pair)


def satisfies_ce4(candidate_pair, event_pair, epistemic_state, **kwargs):
    candidate, candidate_alt = candidate_pair
    remaining_variables = epistemic_state.endogenous_domains.keys() - candidate.keys()
    for subset_remaining_variables in powerset(remaining_variables):
        if subset_remaining_variables:  # only consider proper supersets
            for candidate_extension, candidate_extension_alt in find_exact_assignment_pairs(epistemic_state.endogenous_domains, subset_remaining_variables):
                superset_candidate_pair = {**candidate, **candidate_extension}, {**candidate_alt, **candidate_extension_alt}
                if satisfies_ce3(superset_candidate_pair) and satisfies_ce1(superset_candidate_pair, event_pair, epistemic_state, **kwargs) and satisfies_ce2(superset_candidate_pair, event_pair, epistemic_state):
                    return False
    return True


def is_contrastive_counterfactual_explanation(candidate_pair, event_pair, epistemic_state, **kwargs):
    if not satisfies_ce3(candidate_pair):
        return False
    if not satisfies_ce1(candidate_pair, event_pair, epistemic_state, **kwargs):
        return False
    if not satisfies_ce2(candidate_pair, event_pair, epistemic_state):
        return False
    if not satisfies_ce4(candidate_pair, event_pair, epistemic_state):
        return False
    return True


def find_contrastive_counterfactual_explanations(event_pair, epistemic_state, **kwargs):
    for candidate_pair in find_all_assignment_pairs(epistemic_state.endogenous_domains):
        if is_contrastive_counterfactual_explanation(candidate_pair, event_pair, epistemic_state, **kwargs):
            yield candidate_pair
