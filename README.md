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

# Related Software
- [hp2sat](https://github.com/amjadKhalifah/HP2SAT1.0): Java library for actual causality computation

# References
- Joseph Y. Halpern. [Actual causality](https://mitpress.mit.edu/books/actual-causality). MIT Press, 2016.
- Joseph Y. Halpern. [A Modification of the Halpern-Pearl Definition of Causality](https://www.ijcai.org/Proceedings/15/Papers/427.pdf). In *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI'15)*, pages 3022-3033, 2015.
