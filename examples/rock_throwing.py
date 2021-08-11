from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
U_ST, U_BT = Variable("U_ST"), Variable("U_BT")
ST, BT, SH, BH, BS = Variable("ST"), Variable("BT"), Variable("SH"), Variable("BH"), Variable("BS")
exogenous_variables = {U_ST, U_BT}
endogenous_domains = {
    ST: {False, True},
    BT: {False, True},
    SH: {False, True},
    BH: {False, True},
    BS: {False, True}
}
causal_network = CausalNetwork()
causal_network.add_dependency(ST, [U_ST], lambda parent_values: parent_values[U_ST])
causal_network.add_dependency(BT, [U_BT], lambda parent_values: parent_values[U_BT])
causal_network.add_dependency(SH, [ST], lambda parent_values: parent_values[ST])
causal_network.add_dependency(BH, [BT, SH], lambda parent_values: parent_values[BT] and not parent_values[SH])
causal_network.add_dependency(BS, [SH, BH], lambda parent_values: parent_values[SH] or parent_values[BH])
context = {U_ST: True, U_BT: True}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(BS, True)
# list(find_actual_causes(event, causal_setting))
# degrees_of_responsibility(event, causal_setting)

causal_network.write("rock_throwing.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{ST: True}, {BS: True}, {SH: True}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {ST: {True: 0.5, False: 0}, BT: {True: 0, False: 0}, BS: {True: 1.0, False: 0}, SH: {True: 0.5, False: 0}, BH: {True: 0, False: 0}}
assert actual_degrees_of_responsibility == expected_degrees_of_responsibility

