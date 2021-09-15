from frozendict import frozendict
from lib.halpern_pearl import Variable, CausalNetwork, CausalSetting, find_actual_causes, PrimitiveEvent
U_BGU, U_ESU = Variable("U_BGU"), Variable("U_ESU")
BGU, ESU, BPT, EE, ESS, SBT, TD = Variable("BGU"), Variable("ESU"), Variable("BPT"), Variable("EE"), Variable("ESS"), Variable("SBT"), Variable("TD")
exogenous_domains = {
    U_BGU: {False, True},
    U_ESU: {False, True}
}
endogenous_domains = {
    BGU: {False, True},
    ESU: {False, True},
    BPT: {False, True},
    EE: {False, True},
    ESS: {False, True},
    SBT: {False, True},
    TD: {False, True}
}
causal_network = CausalNetwork()
causal_network.add_dependency(BGU, [U_BGU], lambda parent_values: parent_values[U_BGU])
causal_network.add_dependency(ESU, [U_ESU], lambda parent_values: parent_values[U_ESU])
causal_network.add_dependency(BPT, [BGU, ESU], lambda parent_values: parent_values[BGU] and parent_values[ESU])
causal_network.add_dependency(EE, [ESU, BPT], lambda parent_values: parent_values[ESU] and not parent_values[BPT])
causal_network.add_dependency(ESS, [EE], lambda parent_values: parent_values[EE])
causal_network.add_dependency(SBT, [ESS], lambda parent_values: not parent_values[ESS])
causal_network.add_dependency(TD, [SBT], lambda parent_values: parent_values[SBT])
context = {U_BGU: True, U_ESU: False}
causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
event = PrimitiveEvent(TD, True)
# list(find_actual_causes(event, causal_setting))

causal_network.write("double_prevention.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_actual_causes = [{ESU: False}, {EE: False}, {ESS: False}, {SBT: True}, {TD: True}]
assert actual_causes == {frozendict(expected_actual_cause) for expected_actual_cause in expected_actual_causes}
