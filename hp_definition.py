from copy import copy

from boolean_combinations import Verum, Falsum, hypothesis2conjunction
from utils import format_dict


class Variable(str):
    def __repr__(self):
        return f"{self}"


class CausalModel:
    def __init__(self, exogenous_variables, structural_equations):
        self.exogenous_variables = exogenous_variables
        self.structural_equations = structural_equations

    def signature(self):
        return self.exogenous_variables, set(self.structural_equations.keys())

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
        self.context = context

    def value(self, variable):
        if variable in self.context:
            return self.context[variable]
        else:
            return self.causal_model.structural_equations[variable](self.context)

    def is_actual_cause(self, hypothesis, event):
        print(f"is {hypothesis} an actual cause of {event} in {self}?")
        if not hypothesis2conjunction(hypothesis).normalise(self.causal_model).entailed_by(self):
            return False
        print(f"{self} |= {hypothesis2conjunction(hypothesis)}")
        if not event.normalise(self.causal_model).entailed_by(self):
            return False
        print(f"{self} |= {event}")
        print("YES")
        return True

    def __str__(self):
        return f"{self.causal_model} / {format_dict(self.context)}"


class CausalFormula:
    def __init__(self, intervention, event):
        self.intervention = intervention
        self.event = event

    def entailed_by(self, causal_setting):
        new_causal_model = causal_setting.causal_model.intervene(self.intervention)
        new_causal_setting = CausalSetting(new_causal_model, causal_setting.context)
        new_event = self.event.normalise(new_causal_model)
        return new_event.entailed_by(new_causal_setting)

    def __str__(self):
        return f"[{format_dict(self.intervention, delim=';', sep='<-', brackets=False)}]({self.event})"
