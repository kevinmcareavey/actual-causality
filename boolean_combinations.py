from abc import ABC, abstractmethod, ABCMeta
from copy import copy


class BooleanFormula(ABC):
    @abstractmethod
    def entailed_by(self, causal_setting):
        raise NotImplemented

    def __repr__(self):
        return self.__str__()


class Verum(BooleanFormula):
    def entailed_by(self, causal_setting):
        return True

    def __str__(self):
        return "True"


class Falsum(BooleanFormula):
    def entailed_by(self, causal_setting):
        return False

    def __str__(self):
        return "False"


class Atom(BooleanFormula):
    def __init__(self, variable):
        self.variable = variable

    def entailed_by(self, causal_setting):
        if self.variable in causal_setting.causal_model.exogenous_variables:
            return causal_setting.context[self.variable]
        else:
            return causal_setting.causal_model.structural_equations[self.variable].entailed_by(causal_setting)

    def __str__(self):
        return f"{self.variable}"


class Negation(BooleanFormula):
    def __init__(self, child):
        self.child = child

    def entailed_by(self, causal_setting):
        return not self.child.entailed_by(causal_setting)

    def __str__(self):
        return f"!{self.child}"


class BinaryFormula(BooleanFormula, metaclass=ABCMeta):
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child


class Conjunction(BinaryFormula):
    def entailed_by(self, causal_setting):
        return self.left_child.entailed_by(causal_setting) and self.right_child.entailed_by(causal_setting)

    def __str__(self):
        return f"({self.left_child} & {self.right_child})"


class Disjunction(BinaryFormula):
    def entailed_by(self, causal_setting):
        return self.left_child.entailed_by(causal_setting) or self.right_child.entailed_by(causal_setting)

    def __str__(self):
        return f"({self.left_child} | {self.right_child})"


def assignments2conjunction(assignments, right_child=None):
    if not assignments:
        return Verum()
    assignments_remainder = copy(assignments)
    variable, value = assignments_remainder.popitem()  # pops items in reverse order, which is important for respecting order of operations
    atom = Atom(variable)
    literal = atom if value else Negation(atom)
    formula = Conjunction(literal, right_child) if right_child else literal
    return assignments2conjunction(assignments_remainder, formula) if assignments_remainder else formula
