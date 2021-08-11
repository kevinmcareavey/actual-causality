import itertools
from copy import copy

from networkx import DiGraph, topological_sort
from networkx.drawing.nx_agraph import to_agraph

from actualcausality.boolean_combinations import assignments2conjunction, Negation
from actualcausality.utils import powerset, format_dict, powerdict


class Variable:
    def __init__(self, symbol):
        self.symbol = symbol

    def __hash__(self):
        return hash((type(self), self.symbol))

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __str__(self):
        return f"{self.symbol}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.symbol < other.symbol


class CausalNetwork:
    def __init__(self):
        self.graph = DiGraph()

        self.structural_equations = dict()
        self.endogenous_bindings = dict()

    def add_dependency(self, endogenous_variable, parents, structural_equation):
        for parent_variable in parents:
            self.graph.add_edge(parent_variable, endogenous_variable)
        self.structural_equations[endogenous_variable] = structural_equation

    def evaluate(self, context):
        values = copy(context)
        for variable in topological_sort(self.graph):
            if variable not in values:
                values[variable] = self.structural_equation(variable, values)
        return {key: value for key, value in values.items() if key not in context}

    def signature(self):
        in_degrees = self.graph.in_degree()
        return {v for v, d in in_degrees if d == 0}, {v for v, d in in_degrees if d != 0}

    def structural_equation(self, variable, parent_values):
        return self.endogenous_bindings[variable] if variable in self.endogenous_bindings else self.structural_equations[variable](parent_values)

    def intervene(self, intervention):
        new_causal_network = CausalNetwork()
        _, endogenous_variables = self.signature()
        for variable in endogenous_variables:
            new_causal_network.add_dependency(variable, self.graph.predecessors(variable), self.structural_equations[variable])
        for variable, value in intervention.items():
            new_causal_network.endogenous_bindings[variable] = value
        return new_causal_network

    def write(self, path, prog="dot"):  # prog=neato|dot|twopi|circo|fdp|nop
        to_agraph(self.graph).draw(path, prog=prog)


class CausalSetting:
    def __init__(self, causal_network, context, endogenous_domains):
        self.causal_network = causal_network
        self.context = context  # dict mapping exogenous variables to values
        self.endogenous_domains = endogenous_domains

        exogenous_variables, endogenous_variables = self.causal_network.signature()
        assert exogenous_variables == set(self.context.keys())
        assert endogenous_variables == set(self.endogenous_domains.keys())

        self.derived_values = self.causal_network.evaluate(self.context)
        self.values = {**self.context, **self.derived_values}

    def find_candidate_causes(self):
        _, endogenous_variables = self.causal_network.signature()
        for candidate_variables in powerset(endogenous_variables):
            if candidate_variables:
                candidate_domains = [self.endogenous_domains[candidate_variable] for candidate_variable in candidate_variables]
                for candidate_values in itertools.product(*candidate_domains):
                    yield {candidate_variable: candidate_value for candidate_variable, candidate_value in zip(candidate_variables, candidate_values)}


class CausalFormula:
    def __init__(self, intervention, event):
        self.intervention = intervention  # dict mapping endogenous variables to values
        self.event = event  # Boolean combination of primitive events

    def entailed_by(self, causal_setting):
        new_causal_network = causal_setting.causal_network.intervene(self.intervention)
        new_causal_setting = CausalSetting(new_causal_network, causal_setting.context, causal_setting.endogenous_domains)
        return self.event.entailed_by(new_causal_setting)

    def __str__(self):
        return f"[{format_dict(self.intervention, sep_item='; ', sep_key_value='<-', brackets=False)}]({self.event})"


def satisfies_ac1(candidate, event, causal_setting):
    if not assignments2conjunction(candidate).entailed_by(causal_setting):
        return False
    if not event.entailed_by(causal_setting):
        return False
    return True


def find_witnesses_ac2(candidate, event, causal_setting):
    x = {candidate_variable: causal_setting.values[candidate_variable] for candidate_variable in candidate}
    all_w = {other_variable: causal_setting.values[other_variable] for other_variable in causal_setting.endogenous_domains.keys() - candidate.keys()}

    x_variables = sorted(x.keys())
    x_domains = [causal_setting.endogenous_domains[variable] - {x[variable]} for variable in x_variables]  # only consider "remaining" values in domain

    for x_prime_tuple in itertools.product(*x_domains):
        x_prime = {variable: value for variable, value in zip(x_variables, x_prime_tuple)}
        for w in powerdict(all_w):
            witness = {**x_prime, **w}
            casual_formula = CausalFormula(witness, Negation(event))
            if casual_formula.entailed_by(causal_setting):
                yield witness


def satisfies_ac2(candidate, event, causal_setting):
    for _ in find_witnesses_ac2(candidate, event, causal_setting):
        return True  # there is at least one witness
    return False


def satisfies_ac3(candidate, event, causal_setting):
    for subset_candidate in powerdict(candidate):
        if subset_candidate != candidate:
            if satisfies_ac1(subset_candidate, event, causal_setting) and satisfies_ac2(subset_candidate, event, causal_setting):
                return False
    return True


def is_actual_cause(candidate, event, causal_setting):
    if not satisfies_ac1(candidate, event, causal_setting):
        return False
    if not satisfies_ac2(candidate, event, causal_setting):
        return False
    if not satisfies_ac3(candidate, event, causal_setting):
        return False
    return True


def find_actual_causes(event, causal_setting):
    for candidate in causal_setting.find_candidate_causes():
        if is_actual_cause(candidate, event, causal_setting):
            yield candidate


def degree_of_responsibility(endogenous_variable, value, event, causal_setting):
    k_values = set()
    for actual_cause in find_actual_causes(event, causal_setting):
        if endogenous_variable in actual_cause and actual_cause[endogenous_variable] == value:  # if endogenous_variable=value is "part of" this cause
            k_values.add(min(len(witness) for witness in find_witnesses_ac2(actual_cause, event, causal_setting)))
    return 1 / min(k_values) if k_values else 0


def degrees_of_responsibility(event, causal_setting):
    return {endogenous_variable: {value: degree_of_responsibility(endogenous_variable, value, event, causal_setting) for value in domain} for endogenous_variable, domain in causal_setting.endogenous_domains.items()}


class EpistemicState:
    def __init__(self, probabilities, float_error=0.00000000001):
        self.probabilities = probabilities

        assert abs(sum(self.probabilities.values()) - 1) < float_error
        first_causal_setting = next(iter(self.causal_settings()))
        exogenous_variables = first_causal_setting.causal_model.exogenous_variables
        assert all(causal_setting.causal_model.exogenous_variables == exogenous_variables for causal_setting in self.causal_settings())
        endogenous_variables = first_causal_setting.causal_model.endogenous_variables()
        assert all(causal_setting.causal_model.endogenous_variables() == endogenous_variables for causal_setting in self.causal_settings())

    def causal_settings(self):
        return self.probabilities.keys()


def degree_of_blame(endogenous_variable, polarity, event, epistemic_state):
    return sum(degree_of_responsibility(endogenous_variable, polarity, event, causal_setting) * probability for causal_setting, probability in epistemic_state.probabilities.items())


def degrees_of_blame(event, epistemic_state):
    polarities = [True, False]
    return {endogenous_variable: {polarity: degree_of_blame(endogenous_variable, polarity, event, epistemic_state) for polarity in polarities} for endogenous_variable in epistemic_state.causal_model.endogenous_variables()}
