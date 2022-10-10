import itertools
import logging

from causal_explainer.halpern_pearl.causes import search_candidate_causes, is_actual_cause, is_sufficient_cause, \
    CausalSetting, Negation
from causal_explainer.utils import issubdict, powerset, powerlist

logger = logging.getLogger("miller_counterfactual")
logging.basicConfig(level=logging.INFO)


def is_partial_cause(candidate, event, causal_setting, sufficient=False):  # sufficient=True uses sufficient causes while sufficient=False used actual causes
    if candidate:
        for cause in search_candidate_causes(event, causal_setting, is_sufficient_cause) if sufficient else search_candidate_causes(event, causal_setting, is_actual_cause):
            if issubdict(candidate, cause):
                logger.debug(f"\t\t\t{candidate} is partial {'sufficient' if sufficient else 'actual'} cause of {event} due to {'sufficient' if sufficient else 'actual'} cause {cause}")
                return True
    return False


def difference_condition(candidate_pair):
    candidate, candidate_alt = candidate_pair
    return all(value != candidate_alt[variable] for variable, value in candidate.items())


def find_exact_assignment_pairs(domains, variables, enforce_difference_condition=True):
    assert variables
    variables_tuple = sorted(variables)
    domains_tuple = [domains[variable] for variable in variables_tuple]
    for values_tuple in itertools.product(*domains_tuple):
        candidate = {variable: value for variable, value in zip(variables_tuple, values_tuple)}
        domains_tuple_alt = [domain - {value} for domain, value in zip(domains_tuple, values_tuple)] if enforce_difference_condition else domains_tuple  # if difference_condition=True then all variables will have unique values
        for values_tuple_alt in itertools.product(*domains_tuple_alt):
            candidate_alt = {variable: value for variable, value in zip(variables_tuple, values_tuple_alt)}
            yield candidate, candidate_alt


def find_all_assignment_pairs(domains):
    for variables in powerset(domains.keys()):
        if variables:
            yield from find_exact_assignment_pairs(domains, variables)


def satisfies_bc1(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
    candidate, _ = candidate_pair
    event, _ = event_pair
    context, _ = context_pair
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    return is_partial_cause(candidate, event, causal_setting, **kwargs)


def satisfies_bc2(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
    _, candidate_alt = candidate_pair
    _, event_alt = event_pair
    _, context_alt = context_pair
    causal_setting_alt = CausalSetting(causal_network, context_alt, exogenous_domains, endogenous_domains)
    return is_partial_cause(candidate_alt, event_alt, causal_setting_alt, **kwargs)


def satisfies_bc3(candidate_pair):
    return difference_condition(candidate_pair)


def satisfies_bc4(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
    candidate, candidate_alt = candidate_pair
    remaining_variables = endogenous_domains.keys() - candidate.keys()
    for subset_remaining_variables in powerset(remaining_variables):
        if subset_remaining_variables:  # only consider proper supersets
            for candidate_extension, candidate_extension_alt in find_exact_assignment_pairs(endogenous_domains, subset_remaining_variables):
                superset_candidate_pair = {**candidate, **candidate_extension}, {**candidate_alt, **candidate_extension_alt}
                if satisfies_bc3(superset_candidate_pair) and satisfies_bc1(superset_candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs) and satisfies_bc2(superset_candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
                    return False
    return True


def is_contrastive_bifactual_cause(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
    if not satisfies_bc3(candidate_pair):
        return False
    if not satisfies_bc1(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
        return False
    if not satisfies_bc2(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
        return False
    if not satisfies_bc4(candidate_pair, event_pair, causal_network, context_pair, exogenous_domains, endogenous_domains, **kwargs):
        return False
    return True


def satisfies_cc1(candidate_pair, event_pair, causal_setting, **kwargs):
    candidate, _ = candidate_pair
    fact, _ = event_pair
    return is_partial_cause(candidate, fact, causal_setting, **kwargs)


def satisfies_cc2(event_pair, causal_setting):
    _, foil = event_pair
    return Negation(foil).entailed_by(causal_setting)


def satisfies_cc3(candidate_pair, event_pair, causal_setting, **kwargs):
    _, candidate_alt = candidate_pair
    _, foil = event_pair
    all_w_variables = sorted(causal_setting.endogenous_domains.keys())
    # all_w_variables = sorted(causal_setting.endogenous_domains.keys() - candidate_alt.keys())
    for w_variables_tuple in powerlist(all_w_variables):
        if w_variables_tuple:
            w_domains_tuple = [causal_setting.endogenous_domains[w_variable] for w_variable in w_variables_tuple]
            for w_values_tuple in itertools.product(*w_domains_tuple):
                w = {variable: value for variable, value in zip(w_variables_tuple, w_values_tuple)}
                new_causal_network = causal_setting.causal_network.intervene(w)
                # new_causal_network = causal_setting.causal_network.intervene({**candidate_alt, **w})
                new_causal_setting = CausalSetting(new_causal_network, causal_setting.context, causal_setting.exogenous_domains, causal_setting.endogenous_domains)
                if is_partial_cause(candidate_alt, foil, new_causal_setting, **kwargs):
                    logger.debug(f"\t\t\tunder intervention {w}")
                    return True
    logger.debug(f"\t\t\tno intervention w such that {candidate_alt} is partial cause of {foil}")
    return False


def satisfies_cc4(candidate_pair):
    return difference_condition(candidate_pair)


def satisfies_cc5(candidate_pair, event_pair, causal_setting, **kwargs):
    candidate, candidate_alt = candidate_pair
    remaining_x_variables = causal_setting.endogenous_domains.keys() - candidate.keys()
    for subset_remaining_x_variables in powerset(remaining_x_variables):
        if subset_remaining_x_variables:  # only consider proper supersets
            for candidate_extension, candidate_extension_alt in find_exact_assignment_pairs(causal_setting.endogenous_domains, subset_remaining_x_variables):
                superset_candidate_pair = {**candidate, **candidate_extension}, {**candidate_alt, **candidate_extension_alt}
                if satisfies_cc4(superset_candidate_pair) and satisfies_cc1(superset_candidate_pair, event_pair, causal_setting, **kwargs) and satisfies_cc3(superset_candidate_pair, event_pair, causal_setting, **kwargs):
                    return False
    return True


def is_contrastive_counterfactual_cause(candidate_pair, event_pair, causal_setting, **kwargs):
    if not satisfies_cc2(event_pair, causal_setting):
        logger.debug(f"\t\tCC2 failed")
        return False
    logger.debug(f"\t\tCC2 passed")
    if not satisfies_cc4(candidate_pair):
        logger.debug(f"\t\tCC4 failed")
        return False
    logger.debug(f"\t\tCC4 passed")
    if not satisfies_cc1(candidate_pair, event_pair, causal_setting, **kwargs):
        logger.debug(f"\t\tCC1 failed")
        return False
    logger.debug(f"\t\tCC1 passed")
    if not satisfies_cc3(candidate_pair, event_pair, causal_setting, **kwargs):
        logger.debug(f"\t\tCC3 failed")
        return False
    logger.debug(f"\t\tCC3 passed")
    if not satisfies_cc5(candidate_pair, event_pair, causal_setting, **kwargs):
        logger.debug(f"\t\tCC5 failed")
        return False
    logger.debug(f"\t\tCC5 passed")
    return True


def find_contrastive_counterfactual_causes(event_pair, causal_setting):
    for candidate_pair in find_all_assignment_pairs(causal_setting.endogenous_domains):
        if is_contrastive_counterfactual_cause(candidate_pair, event_pair, causal_setting):
            yield candidate_pair
