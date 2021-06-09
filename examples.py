from boolean_combinations import Disjunction, Atom, Conjunction, Negation, assignments2conjunction
from hp_definition import Variable, CausalModel, CausalFormula, CausalSetting, is_actual_cause
from utils import powerset_set


def forest_fire(disjunction=True):
    u_l = Variable("U_L")
    u_md = Variable("U_MD")

    ff = Variable("FF")
    l = Variable("L")
    md = Variable("MD")

    assert ff == ff
    assert ff == Variable("FF")
    assert Variable("FF") == Variable("FF")
    assert type(ff) == Variable

    cm = CausalModel(
        {u_l, u_md},
        {
            ff: Disjunction(Atom(l), Atom(md)) if disjunction else Conjunction(Atom(l), Atom(md)),
            l: Atom(u_l),
            md: Atom(u_md)
        }
    )

    # cm.causal_network().draw(f"examples/{'dis' if disjunction else 'con'}junctive_forest_fire.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

    c = {
        u_l: True,
        u_md: True
    }

    cs = CausalSetting(cm, c)

    cf1 = CausalFormula(
        {md: False},
        Atom(ff)
    )
    assert not disjunction or cf1.entailed_by(cs)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{cs} |= {cf1} : {cf1.entailed_by(cs)}")

    cf2 = CausalFormula(
        {l: False},
        Atom(ff)
    )
    assert not disjunction or cf2.entailed_by(cs)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{cs} |= {cf2} : {cf2.entailed_by(cs)}")

    cf3 = CausalFormula(
        {l: False, md: False},
        Negation(Atom(ff))
    )
    assert not disjunction or cf3.entailed_by(cs)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]
    print(f"{cs} |= {cf3} : {cf3.entailed_by(cs)}")


def rock_throwing():
    st_exo = Variable("ST_exo")
    bt_exo = Variable("BT_exo")

    st = Variable("ST")
    bt = Variable("BT")
    sh = Variable("SH")
    bh = Variable("BH")
    bs = Variable("BS")

    cm = CausalModel(
        {st_exo, bt_exo},
        {
            st: Atom(st_exo),
            bt: Atom(bt_exo),
            sh: Atom(st),
            bh: Conjunction(Atom(bt), Negation(Atom(sh))),
            bs: Disjunction(Atom(sh), Atom(bh))
        }
    )

    # cm.causal_network().draw("examples/rock_throwing.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

    c = {
        st_exo: True,
        bt_exo: True
    }

    cs = CausalSetting(cm, c)

    def is_correct(assignments, result):
        if assignments == {st: True} or assignments == {sh: True} or assignments == {bs: True}:
            return result is True
        else:
            return result is False

    for candidate_variables in powerset_set(cm.endogenous_variables()):
        if candidate_variables:
            initial_candidate = {variable: True for variable in candidate_variables}
            for negated_candidate_variables in powerset_set(candidate_variables):
                candidate = {variable: not value if variable in negated_candidate_variables else value for variable, value in initial_candidate.items()}
                actual_cause = is_actual_cause(candidate, Atom(bs), cs)
                assert is_correct(candidate, actual_cause)
                if actual_cause:
                    print(f"{assignments2conjunction(candidate)} is an actual cause of {Atom(bs)} in causal setting {cs}")
