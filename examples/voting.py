from frozendict import frozendict
from actualcausality.boolean_combinations import PrimitiveEvent
from actualcausality.hp_definition import Variable, CausalNetwork, CausalSetting, find_actual_causes, degrees_of_responsibility
num_voters = 4
U = [Variable(f"U_V{i+1}") for i in range(num_voters)]
V, W = [Variable(f"V{i+1}") for i in range(num_voters)], Variable("W")
exogenous_variables = set(U)
endogenous_domains = {
    **{v: {"Suzy", "Billy"} for v in V},
    W: {"Suzy", "Billy", "tie"}
}
causal_network = CausalNetwork()
for i in range(num_voters):
    structural_equation = (lambda i: lambda parent_values: parent_values[U[i]])(i)  # WARNING: https://stackoverflow.com/questions/19837486/lambda-in-a-loop
    causal_network.add_dependency(V[i], [U[i]], structural_equation)
causal_network.add_dependency(
    W,
    V,
    lambda parent_values:
        "Suzy" if len([v for v in V if parent_values[v] == "Suzy"]) > (num_voters / 2) else "Billy" if len([v for v in V if parent_values[v] == "Billy"]) > (num_voters / 2) else "tie"
)
context = {
    **{u: "Suzy" for u in U[:num_voters//2]},
    **{u: "Billy" for u in U[num_voters//2:]}
}
causal_setting = CausalSetting(causal_network, context, endogenous_domains)
event = PrimitiveEvent(W, causal_setting.values[W])
list(find_actual_causes(event, causal_setting))
degrees_of_responsibility(event, causal_setting)

causal_network.write("voting.png")

actual_causes = {frozendict(actual_cause) for actual_cause in find_actual_causes(event, causal_setting)}
expected_causes = [{v: "Suzy"} for v in V[:num_voters//2]] + [{v: "Billy"} for v in V[num_voters//2:]] + [{W: 'tie'}]
assert actual_causes == {frozendict(expected_cause) for expected_cause in expected_causes}
actual_degrees_of_responsibility = degrees_of_responsibility(event, causal_setting)
expected_degrees_of_responsibility = {
    **{v: {"Billy": 0, "Suzy": 1.0} for v in V[:num_voters//2]},
    **{v: {"Billy": 1.0, "Suzy": 0} for v in V[num_voters//2:]},
    W: {"Suzy": 0, "tie": 1.0, "Billy": 0}
}
assert actual_degrees_of_responsibility == expected_degrees_of_responsibility
