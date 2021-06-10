from copy import copy

from pygraphviz import AGraph

from actualcausality.boolean_combinations import assignments2conjunction, Negation, Verum, Falsum
from actualcausality.utils import format_dict, powerdict, powerset


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


class CausalModel:
    def __init__(self, exogenous_variables, structural_equations):
        self.exogenous_variables = exogenous_variables  # set of exogenous variables
        self.structural_equations = structural_equations  # dict mapping endogenous variables to Boolean formulas over (exogenous and/or endogenous) variables

    def endogenous_variables(self):
        return set(self.structural_equations.keys())

    def signature(self):
        return self.exogenous_variables, self.endogenous_variables()

    def intervene(self, intervention):
        new_structural_equations = copy(self.structural_equations)
        for variable, value in intervention.items():
            new_structural_equations[variable] = Verum() if value else Falsum()
        return CausalModel(self.exogenous_variables, new_structural_equations)

    def causal_network(self):
        network = AGraph(directed=True)
        for exogenous_variable in self.exogenous_variables:
            network.add_node(str(exogenous_variable))
        for endogenous_variable, equation in self.structural_equations.items():
            network.add_node(str(endogenous_variable), xlabel=f"{endogenous_variable} = {equation}")
        for endogenous_variable, equation in self.structural_equations.items():
            for variable in equation.variables():
                network.add_edge(str(variable), str(endogenous_variable))
        return network

    def __str__(self):
        return f"({self.exogenous_variables}, {format_dict(self.structural_equations)})"


class CausalSetting:
    def __init__(self, causal_model, context):
        self.causal_model = causal_model
        self.context = context  # dict mapping exogenous variables to values

        assert self.causal_model.exogenous_variables == self.context.keys()

    def values(self):
        endogenous_values = {endogenous_variable: self.causal_model.structural_equations[endogenous_variable].entailed_by(self) for endogenous_variable in self.causal_model.endogenous_variables()}
        return {**self.context, **endogenous_values}

    def __str__(self):
        return f"({format_dict(self.context)}, {format_dict(self.causal_model.structural_equations)})"


class CausalFormula:
    def __init__(self, intervention, event):
        self.intervention = intervention  # dict mapping endogenous variables to values
        self.event = event  # Boolean formula over endogenous variables

    def entailed_by(self, causal_setting):
        new_causal_model = causal_setting.causal_model.intervene(self.intervention)
        new_causal_setting = CausalSetting(new_causal_model, causal_setting.context)
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
    actual_values = causal_setting.values()

    x_values = {candidate_variable: actual_values[candidate_variable] for candidate_variable in candidate}
    w_values = {other_variable: actual_values[other_variable] for other_variable in causal_setting.causal_model.endogenous_variables() - candidate.keys()}
    assert not (x_values.keys() & w_values.keys())  # x_values and w_values should not intersect

    for subset_x_values in powerdict(x_values):
        if subset_x_values:  # at least one X variable must be negated
            x_prime_values = {candidate_variable: not candidate_value if candidate_variable in subset_x_values else candidate_value for candidate_variable, candidate_value in candidate.items()}
            for subset_w_values in powerdict(w_values):
                witness = {**x_prime_values, **subset_w_values}
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


def find_actual_causes(event, causal_setting, expected_causes=None):
    for candidate_variables in powerset(causal_setting.causal_model.endogenous_variables()):
        if candidate_variables:
            initial_candidate = {variable: True for variable in candidate_variables}
            for negated_candidate_variables in powerset(candidate_variables):
                candidate = {variable: not value if variable in negated_candidate_variables else value for variable, value in initial_candidate.items()}
                candidate_is_actual_cause = is_actual_cause(candidate, event, causal_setting)
                if expected_causes:
                    assert candidate_is_actual_cause == (candidate in expected_causes)
                if candidate_is_actual_cause:
                    yield candidate


def degree_of_responsibility(exogenous_variable, value, event, causal_setting):
    k_values = set()
    for actual_cause in find_actual_causes(event, causal_setting):
        if exogenous_variable in actual_cause and actual_cause[exogenous_variable] == value:  # if exogenous_variable=value is "part of a cause"
            k_values.add(min(len(witness) for witness in find_witnesses_ac2(actual_cause, event, causal_setting)))
    return 1 / min(k_values) if k_values else 0
