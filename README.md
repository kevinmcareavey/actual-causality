# PyActualCausality
A simple Python implementation of the (modified) Halpern-Pearl definition of actual causality.

*Note that causal models are restricted to those with Boolean variables and structural equations are restricted to propositional formulas.*

## Examples

### Forest Fire
This example involves three endogenous variables: a forest fire `FF`, a lightning strike `L`, and a match dropped by an arsonist `MD`.
The values of these variables are defined in two different causal models, known as the conjunctive and disjunctive models, based on two exogenous variables `U_L` and `U_MD`.

#### Conjunctive Model
In the conjunctive model the structural equations are defined as `FF = (L & MD)`, `L = U_L`, and `MD = U_MD`.

```python
>>> from actualcausality.boolean_combinations import Atom, Conjunction
>>> from actualcausality.hp_definition import CausalModel, CausalSetting, Variable, find_actual_causes, degrees_of_responsibility
>>> u_l, u_md = Variable("U_L"), Variable("U_MD")
>>> ff, l, md = Variable("FF"), Variable("L"), Variable("MD")
>>> exogenous_variables = {u_l, u_md}
>>> structural_equations = {
...     ff: Conjunction(Atom(l), Atom(md)),
...     l: Atom(u_l),
...     md: Atom(u_md)
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_l: True, u_md: True}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(ff)
>>> list(find_actual_causes(event, causal_setting))
[{FF: True}, {L: True}, {MD: True}]
>>> degrees_of_responsibility(event, causal_setting)
{FF: {True: 1.0, False: 0}, L: {True: 1.0, False: 0}, MD: {True: 1.0, False: 0}}
```

![](examples/forest_fire_disjunctive.png)

#### Disjunctive Model
In the disjunctive model the structural equations are defined as `FF = (L | MD)`, `L = U_L`, and `MD = U_MD`.

```python
>>> from actualcausality.boolean_combinations import Atom, Disjunction, Negation
>>> from actualcausality.hp_definition import CausalModel, CausalSetting, Variable, find_actual_causes, CausalFormula, degrees_of_responsibility
>>> u_l, u_md = Variable("U_L"), Variable("U_MD")
>>> ff, l, md = Variable("FF"), Variable("L"), Variable("MD")
>>> exogenous_variables = {u_l, u_md}
>>> structural_equations = {
...     ff: Disjunction(Atom(l), Atom(md)),
...     l: Atom(u_l),
...     md: Atom(u_md)
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_l: True, u_md: True}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(ff)
>>> list(find_actual_causes(event, causal_setting))
[{FF: True}, {L: True, MD: True}]
>>> degrees_of_responsibility(event, causal_setting)
{L: {True: 0.5, False: 0}, FF: {True: 1.0, False: 0}, MD: {True: 0.5, False: 0}}
```

![](examples/forest_fire_conjunctive.png)

### Rock Throwing
This example involves five endogenous variables: Suzy throws a rock `ST`, Billy throws a rock `BT`, Suzy hits the bottle `SH`, Billy hits the bottle `BH`, and the bottle shatters `BS`.
The values of these variables are defined in a causal model based on two exogenous variables `U_ST` and `U_BT` where the structural equations are defined as `ST = U_ST`, `BT = U_BT`, `SH = ST`, `BH = (BT & !SH)`, and `BS = (SH | BH)`.

```python
>>> from actualcausality.boolean_combinations import Atom, Conjunction, Negation, Disjunction
>>> from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
>>> u_st, u_bt = Variable("U_ST"), Variable("U_BT")
>>> st, bt, sh, bh, bs = Variable("ST"), Variable("BT"), Variable("SH"), Variable("BH"), Variable("BS")
>>> exogenous_variables = {u_st, u_bt}
>>> structural_equations = {
...     st: Atom(u_st),
...     bt: Atom(u_bt),
...     sh: Atom(st),
...     bh: Conjunction(Atom(bt), Negation(Atom(sh))),
...     bs: Disjunction(Atom(sh), Atom(bh))
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_st: True, u_bt: True}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(bs)
>>> list(find_actual_causes(event, causal_setting))
[{ST: True}, {SH: True}, {BS: True}]
>>> degrees_of_responsibility(event, causal_setting)
{BT: {True: 0, False: 0}, BH: {True: 0, False: 0}, ST: {True: 0.5, False: 0}, SH: {True: 0.5, False: 0}, BS: {True: 1.0, False: 0}}
```

![](examples/rock_throwing.png)

### Voting
This example involves four endogenous variables: person 1 votes for Suzy `V1`, person 2 votes for Suzy `V2`, person 3 votes for Suzy `V3`, and Suzy wins `W`.
The values of these variables are defined in a causal model based on three exogenous variables `U_V1`, `U_V2`, and `U_V3` where the structural equations are defined as `V1 = U_V1`, `V2 = U_V2`, `V3 = U_V3`, and `W = ((V1 & V2) | (V1 & V3) | (V2 & V3))`.

```python
>>> from actualcausality.boolean_combinations import Atom, Conjunction, Disjunction
>>> from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
>>> u_v1, u_v2, u_v3 = Variable("U_V1"), Variable("U_V2"), Variable("U_V3")
>>> v1, v2, v3, w = Variable("V1"), Variable("V2"), Variable("V3"), Variable("W")
>>> exogenous_variables = {u_v1, u_v2, u_v3}
>>> structural_equations = {
...     v1: Atom(u_v1),
...     v2: Atom(u_v2),
...     v3: Atom(u_v3),
...     w: Disjunction(Disjunction(Conjunction(Atom(v1), Atom(v2)), Conjunction(Atom(v1), Atom(v3))), Conjunction(Atom(v2), Atom(v3)))
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_v1: True, u_v2: True, u_v3: True}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(w)
>>> list(find_actual_causes(event, causal_setting))
[{V1: True, V3: True}, {V1: True, V2: True}, {V3: True, V2: True}, {W: True}]
>>> degrees_of_responsibility(event, causal_setting)
{V1: {True: 0.5, False: 0}, V3: {True: 0.5, False: 0}, V2: {True: 0.5, False: 0}, W: {True: 1.0, False: 0}}
```

![](examples/voting.png)

### Double Prevention
This example involves seven endogenous variables: Billy goes up `BGU`, enemy shows up `ESU`, Billy pulls trigger `BPT`, enemy eludes `EE`, enemy shoots Suzy `ESS`, Suzy bombs target `SBT`, and target is destroyed `TD`.
The values of these variables are defined in a causal model based on two exogenous variables `U_BGU` and `U_ESU` where the structural equations are defined as `BGU = U_BGU`, `ESU = U_ESU`, `BPT = (BGU & ESU)`, `EE = (ESU & !BPT)`, `ESS = EE`, `SBT = !ESS`, and `TD = SBT`.

```python
>>> from actualcausality.boolean_combinations import Atom, Negation, Conjunction
>>> from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
>>> u_bgu, u_esu = Variable("U_BGU"), Variable("U_ESU")
>>> bgu, esu, bpt, ee, ess, sbt, td = Variable("BGU"), Variable("ESU"), Variable("BPT"), Variable("EE"), Variable("ESS"), Variable("SBT"), Variable("TD")
>>> exogenous_variables = {u_bgu, u_esu}
>>> structural_equations = {
...     bgu: Atom(u_bgu),
...     esu: Atom(u_esu),
...     bpt: Conjunction(Atom(bgu), Atom(esu)),
...     ee: Conjunction(Atom(esu), Negation(Atom(bpt))),
...     ess: Atom(ee),
...     sbt: Negation(Atom(ess)),
...     td: Atom(sbt)
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_bgu: True, u_esu: False}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(td)
>>> list(find_actual_causes(event, causal_setting))
[{ESS: False}, {SBT: True}, {ESU: False}, {EE: False}, {TD: True}]
>>> degrees_of_responsibility(event, causal_setting)
{ESS: {True: 0, False: 1.0}, BGU: {True: 0, False: 0}, BPT: {True: 0, False: 0}, SBT: {True: 1.0, False: 0}, ESU: {True: 0, False: 0.5}, EE: {True: 0, False: 1.0}, TD: {True: 1.0, False: 0}}
```

![](examples/double_prevention.png)

### Railroad
This example involves four endogenous variables: engineer flips the switch `F`, left track is blocked `LB`, right track is blocked `RB`, and the train arrives `A`.
The values of these variables are defined in a causal model based on three exogenous variables `U_F`, `U_LB`, and `U_RB` where the structural equations are defined as `F = U_F`, `LB = U_LB`, `RB = U_RB`, and `A = ((F & !LB) | (!F & !RB))`.

```python
>>> from actualcausality.boolean_combinations import Atom, Conjunction, Negation, Disjunction
>>> from actualcausality.hp_definition import Variable, CausalSetting, find_actual_causes, CausalModel, degrees_of_responsibility
>>> u_f, u_lb, u_rb = Variable("U_F"), Variable("U_LB"), Variable("U_RB")
>>> f, lb, rb, a = Variable("F"), Variable("LB"), Variable("RB"), Variable("A")
>>> exogenous_variables = {u_f, u_lb, u_rb}
>>> structural_equations = {
...     f: Atom(u_f),
...     lb: Atom(u_lb),
...     rb: Atom(u_rb),
...     a: Disjunction(Conjunction(Atom(f), Negation(Atom(lb))), Conjunction(Negation(Atom(f)), Negation(Atom(rb))))
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {u_f: True, u_lb: False, u_rb: False}
>>> causal_setting = CausalSetting(causal_model, context)
>>> event = Atom(a)
>>> list(find_actual_causes(event, causal_setting))
[{LB: False}, {A: True}, {F: True, RB: False}]
>>> degrees_of_responsibility(event, causal_setting)
{F: {True: 0.5, False: 0}, LB: {True: 0, False: 1.0}, A: {True: 1.0, False: 0}, RB: {True: 0, False: 0.5}}
```

![](examples/railroad.png)

# Related Software
- [hp2sat](https://github.com/amjadKhalifah/HP2SAT1.0): Java library for actual causality computation

# References
- Joseph Y. Halpern. [Actual causality](https://mitpress.mit.edu/books/actual-causality). MIT Press, 2016.
- Joseph Y. Halpern. [A Modification of the Halpern-Pearl Definition of Causality](https://www.ijcai.org/Proceedings/15/Papers/427.pdf). In *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI'15)*, pages 3022-3033, 2015.
