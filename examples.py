from boolean_combinations import Disjunction, Atom, Conjunction, Negation
from hp_definition import Variable, CausalModel, CausalFormula, CausalSetting


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

    c = {
        u_l: True,
        u_md: True
    }

    cs = CausalSetting(cm, c)

    cf1 = CausalFormula(
        {md: False},
        Atom(ff)
    )
    if disjunction:
        assert cf1.entailed_by(cs)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{cs} |= {cf1} : {cf1.entailed_by(cs)}")

    cf2 = CausalFormula(
        {l: False},
        Atom(ff)
    )
    if disjunction:
        assert cf2.entailed_by(cs)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{cs} |= {cf2} : {cf2.entailed_by(cs)}")

    cf3 = CausalFormula(
        {l: False, md: False},
        Negation(Atom(ff))
    )
    if disjunction:
        assert cf3.entailed_by(cs)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]
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

    c = {
        st_exo: True,
        bt_exo: True
    }

    cs = CausalSetting(cm, c)

    cs.is_actual_cause({st: True}, Atom(bs))
