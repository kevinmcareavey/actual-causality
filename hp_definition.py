from copy import copy

from boolean_combinations import Verum, Falsum, assignments2conjunction, Negation
from utils import format_dict, powerset_dict


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
        return f"[{format_dict(self.intervention, delim=';', sep='<-', brackets=False)}]({self.event})"


def satisfies_ac1(hypothesis, event, causal_setting):
    if not assignments2conjunction(hypothesis).entailed_by(causal_setting):
        return False
    if not event.entailed_by(causal_setting):
        return False
    return True


def satisfies_ac2(hypothesis, event, causal_setting):
    original_values = causal_setting.values()

    x_values = {hypothesis_variable: original_values[hypothesis_variable] for hypothesis_variable in hypothesis}
    w_values = {witness_variable: original_values[witness_variable] for witness_variable in causal_setting.causal_model.endogenous_variables() - hypothesis.keys()}
    assert not (x_values.keys() & w_values.keys())  # x_values and w_values should not intersect

    for subset_x_values in powerset_dict(x_values):
        if subset_x_values:  # at least one X variable must be negated
            x_prime_values = {hypothesis_variable: not hypothesis_value if hypothesis_variable in subset_x_values else hypothesis_value for hypothesis_variable, hypothesis_value in hypothesis.items()}
            for subset_w_values in powerset_dict(w_values):
                casual_formula = CausalFormula({**x_prime_values, **subset_w_values}, Negation(event))
                if casual_formula.entailed_by(causal_setting):
                    return True

    return False


def satisfies_ac3(hypothesis, event, causal_setting):
    for subset_hypothesis in powerset_dict(hypothesis):
        if subset_hypothesis != hypothesis:
            if satisfies_ac1(subset_hypothesis, event, causal_setting) and satisfies_ac2(subset_hypothesis, event, causal_setting):
                return False
    return True


def is_actual_cause(hypothesis, event, causal_setting):
    if not satisfies_ac1(hypothesis, event, causal_setting):
        return False
    if not satisfies_ac2(hypothesis, event, causal_setting):
        return False
    if not satisfies_ac3(hypothesis, event, causal_setting):
        return False
    return True
