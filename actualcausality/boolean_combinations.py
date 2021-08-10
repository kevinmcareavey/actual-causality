from abc import ABC, abstractmethod, ABCMeta
from copy import copy


class Event(ABC):
    @abstractmethod
    def entailed_by(self, causal_setting):
        raise NotImplemented

    @abstractmethod
    def variables(self):
        raise NotImplemented

    def __repr__(self):
        return self.__str__()


class Verum(Event):
    def entailed_by(self, causal_setting):
        return True

    def variables(self):
        return set()

    def __str__(self):
        return "True"


class Falsum(Event):
    def entailed_by(self, causal_setting):
        return False

    def variables(self):
        return set()

    def __str__(self):
        return "False"


class PrimitiveEvent(Event):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def entailed_by(self, causal_setting):
        return causal_setting.values[self.variable] == self.value

    def variables(self):
        return {self.variable}

    def __str__(self):
        return f"{self.variable}={self.value}"


class Negation(Event):
    def __init__(self, child):
        self.child = child

    def entailed_by(self, causal_setting):
        return not self.child.entailed_by(causal_setting)

    def variables(self):
        return self.child.variables()

    def __str__(self):
        return f"!({self.child})"


class BinaryFormula(Event, metaclass=ABCMeta):
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def variables(self):
        return self.left_child.variables() | self.right_child.variables()


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
    primitive_event = PrimitiveEvent(variable, value)
    formula = Conjunction(primitive_event, right_child) if right_child else primitive_event
    return assignments2conjunction(assignments_remainder, formula) if assignments_remainder else formula
