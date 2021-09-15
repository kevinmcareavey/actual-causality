from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, PrimitiveEvent
U_ST, U_BT = Variable("U_ST"), Variable("U_BT")
ST, BT, SH, BH, BS = Variable("ST"), Variable("BT"), Variable("SH"), Variable("BH"), Variable("BS")
exogenous_domains = {
    U_ST: {False, True},
    U_BT: {False, True}
}
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
causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
event = PrimitiveEvent(BS, True)
# list(find_actual_causes(event, causal_setting))

causal_network.write("rock_throwing.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_actual_causes = [{ST: True}, {BS: True}, {SH: True}]
assert actual_causes == {frozendict(expected_actual_cause) for expected_actual_cause in expected_actual_causes}

