from boolean_combinations import Disjunction, Atom, Conjunction, Negation, assignments2conjunction
from hp_definition import Variable, CausalModel, CausalFormula, CausalSetting, find_actual_causes


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

    causal_model = CausalModel(
        {u_l, u_md},
        {
            ff: Disjunction(Atom(l), Atom(md)) if disjunction else Conjunction(Atom(l), Atom(md)),
            l: Atom(u_l),
            md: Atom(u_md)
        }
    )

    # causal_model.causal_network().draw(f"examples/{'dis' if disjunction else 'con'}junctive_forest_fire.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

    context = {
        u_l: True,
        u_md: True
    }

    causal_setting = CausalSetting(causal_model, context)

    causal_formula1 = CausalFormula(
        {md: False},
        Atom(ff)
    )
    assert not disjunction or causal_formula1.entailed_by(causal_setting)  # (Md, (1, 1)) |= [MD ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{causal_setting} |= {causal_formula1} : {causal_formula1.entailed_by(causal_setting)}")

    causal_formula2 = CausalFormula(
        {l: False},
        Atom(ff)
    )
    assert not disjunction or causal_formula2.entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0](FF = 1) example from Page 21 [Halpern, 2016]
    print(f"{causal_setting} |= {causal_formula2} : {causal_formula2.entailed_by(causal_setting)}")

    causal_formula3 = CausalFormula(
        {l: False, md: False},
        Negation(Atom(ff))
    )
    assert not disjunction or causal_formula3.entailed_by(causal_setting)  # (Md, (1, 1)) |= [L ← 0; MD ← 0](FF = 0) example from Page 21 [Halpern, 2016]
    print(f"{causal_setting} |= {causal_formula3} : {causal_formula3.entailed_by(causal_setting)}")

    event = Atom(ff)
    actual_causes = find_actual_causes(event, causal_setting, expected_causes=[{ff: True}, {l: True, md: True}] if disjunction else [{ff: True}, {l: True}, {md: True}])
    for actual_cause in actual_causes:
        print(f"{assignments2conjunction(actual_cause)} is an actual cause of {event} in causal setting {causal_setting}")


def rock_throwing():
    st_exo = Variable("ST_exo")
    bt_exo = Variable("BT_exo")

    st = Variable("ST")
    bt = Variable("BT")
    sh = Variable("SH")
    bh = Variable("BH")
    bs = Variable("BS")

    causal_model = CausalModel(
        {st_exo, bt_exo},
        {
            st: Atom(st_exo),
            bt: Atom(bt_exo),
            sh: Atom(st),
            bh: Conjunction(Atom(bt), Negation(Atom(sh))),
            bs: Disjunction(Atom(sh), Atom(bh))
        }
    )

    # causal_model.causal_network().draw("examples/rock_throwing.png", prog="dot")  # prog=neato|dot|twopi|circo|fdp|nop

    context = {
        st_exo: True,
        bt_exo: True
    }

    causal_setting = CausalSetting(causal_model, context)

    event = Atom(bs)
    actual_causes = find_actual_causes(event, causal_setting, expected_causes=[{st: True}, {sh: True}, {bs: True}])
    for actual_cause in actual_causes:
        print(f"{assignments2conjunction(actual_cause)} is an actual cause of {event} in causal setting {causal_setting}")
