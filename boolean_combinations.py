from abc import ABC, abstractmethod, ABCMeta
from copy import copy


class BooleanFormula(ABC):
    @abstractmethod
    def normalise(self, causal_model):
        raise NotImplemented

    @abstractmethod
    def entailed_by(self, causal_setting):
        raise NotImplemented


class Verum(BooleanFormula):
    def normalise(self, causal_model):
        return self

    def entailed_by(self, causal_setting):
        return True

    def __str__(self):
        return "True"


class Falsum(BooleanFormula):
    def normalise(self, causal_model):
        return self

    def entailed_by(self, causal_setting):
        return False

    def __str__(self):
        return "False"


class Atom(BooleanFormula):
    def __init__(self, variable):
        self.variable = variable

    def normalise(self, causal_model):
        if self.variable in causal_model.exogenous_variables:
            return self
        else:
            return causal_model.structural_equations[self.variable].normalise(causal_model)

    def entailed_by(self, causal_setting):
        if self.variable not in causal_setting.causal_model.exogenous_variables:
            raise Exception
        return causal_setting.context[self.variable]

    def __str__(self):
        return f"{self.variable}"


class Negation(BooleanFormula):
    def __init__(self, child):
        self.child = child

    def normalise(self, causal_model):
        return Negation(self.child.normalise(causal_model))

    def entailed_by(self, causal_setting):
        return not self.child.entailed_by(causal_setting)

    def __str__(self):
        return f"!{self.child}"


class BinaryFormula(BooleanFormula, metaclass=ABCMeta):
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child


class Conjunction(BinaryFormula):
    def normalise(self, causal_model):
        return Conjunction(self.left_child.normalise(causal_model), self.right_child.normalise(causal_model))

    def entailed_by(self, causal_setting):
        return self.left_child.entailed_by(causal_setting) and self.right_child.entailed_by(causal_setting)

    def __str__(self):
        return f"({self.left_child} & {self.right_child})"


class Disjunction(BinaryFormula):
    def normalise(self, causal_model):
        return Disjunction(self.left_child.normalise(causal_model), self.right_child.normalise(causal_model))

    def entailed_by(self, causal_setting):
        return self.left_child.entailed_by(causal_setting) or self.right_child.entailed_by(causal_setting)

    def __str__(self):
        return f"({self.left_child} | {self.right_child})"


def hypothesis2conjunction(hypothesis, right_child=None):
    hypothesis_remainder = copy(hypothesis)
    variable, value = hypothesis_remainder.popitem()  # pops items in reverse order, which is important for order of operations
    atom = Atom(variable)
    literal = atom if value else Negation(atom)
    formula = Conjunction(literal, right_child) if right_child else literal
    return hypothesis2conjunction(hypothesis_remainder, formula) if hypothesis_remainder else formula
