# actual-causality
A simple Python implementation of the (modified) Halpern-Pearl definition of actual causality where all variables are Boolean variables and all structural equations are propositional formulas.

## Examples

### Forest Fire

#### Conjunctive Model
```python
>>> from boolean_combinations import Atom, Conjunction
>>> from hp_definition import CausalModel, CausalSetting, Variable, is_actual_cause
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
>>> casual_setting = CausalSetting(causal_model, context)
>>> event = Atom(ff)
>>> is_actual_cause({l: True}, event, casual_setting)
True
>>> is_actual_cause({md: True}, event, casual_setting)
True
>>> is_actual_cause({l: True, md: True}, event, casual_setting)
False
```

![](examples/disjunctive_forest_fire.png)

#### Disjunctive Model
```python
>>> from boolean_combinations import Atom, Disjunction
>>> from hp_definition import CausalModel, CausalSetting, Variable, is_actual_cause
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
>>> casual_setting = CausalSetting(causal_model, context)
>>> event = Atom(ff)
>>> is_actual_cause({l: True}, event, casual_setting)
False
>>> is_actual_cause({md: True}, event, casual_setting)
False
>>> is_actual_cause({l: True, md: True}, event, casual_setting)
True
```

![](examples/conjunctive_forest_fire.png)

### Rock Throwing
```python
>>> from boolean_combinations import Atom, Conjunction, Disjunction, Negation
>>> from hp_definition import CausalModel, CausalSetting, Variable, is_actual_cause
>>> st_exo, bt_exo = Variable("ST_exo"), Variable("BT_exo")
>>> st, bt, sh, bh, bs = Variable("ST"), Variable("BT"), Variable("SH"), Variable("BH"), Variable("BS")
>>> exogenous_variables = {st_exo, bt_exo}
>>> structural_equations = {
...     st: Atom(st_exo),
...     bt: Atom(bt_exo),
...     sh: Atom(st),
...     bh: Conjunction(Atom(bt), Negation(Atom(sh))),
...     bs: Disjunction(Atom(sh), Atom(bh))
... }
>>> causal_model = CausalModel(exogenous_variables, structural_equations)
>>> context = {st_exo: True, bt_exo: True}
>>> casual_setting = CausalSetting(causal_model, context)
>>> event = Atom(bs)
>>> is_actual_cause({st: True}, event, casual_setting)
True
>>> is_actual_cause({bt: True}, event, casual_setting)
False
>>> is_actual_cause({st: True, bt: True}, event, casual_setting)
False
```

![](examples/rock_throwing.png)

# Related Software
- [hp2sat](https://github.com/amjadKhalifah/HP2SAT1.0): Java library for actual causality computation

# References
- Joseph Y. Halpern. [Actual causality](https://mitpress.mit.edu/books/actual-causality). MIT Press, 2016.
- Joseph Y. Halpern. [A Modification of the Halpern-Pearl Definition of Causality](https://www.ijcai.org/Proceedings/15/Papers/427.pdf). In *Proceedings of the 24th International Joint Conference on Artificial Intelligence (IJCAI'15)*, pages 3022-3033, 2015.
