from causal_explainer.halpern_pearl.causes import CausalNetwork, CausalSetting, PrimitiveEvent, search_candidate_causes, \
    is_actual_cause
from causal_explainer.utils import freeze

if __name__ == "__main__":
    num_voters = 4
    U = [f'U_V{i+1}' for i in range(num_voters)]
    V, W = [f'V{i+1}' for i in range(num_voters)], 'W'
    exogenous_domains = {u: {"Suzy", "Billy"} for u in U}
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
        **{u: "Billy" for u in U[num_voters//2:]},
        **{u: "Suzy" for u in U[:num_voters//2 + (0 if num_voters % 2 == 0 else 1)]}  # even split unless num_voters is odd, in which case Suzy gets the additional vote
    }
    causal_setting = CausalSetting(causal_network, context, exogenous_domains, endogenous_domains)
    event = PrimitiveEvent(W, causal_setting.values[W])

    causal_network.write("img/voting.png")

    actual_causes = freeze(search_candidate_causes(event, causal_setting, is_actual_cause))
    if num_voters % 2 == 0:
        expected_actual_causes = freeze([{v: "Suzy"} for v in V[:num_voters//2]] + [{v: "Billy"} for v in V[num_voters//2:]] + [{W: "tie"}])
        assert actual_causes == expected_actual_causes
    else:
        expected_actual_causes = freeze([{v: "Suzy"} for v in V[:num_voters//2 + 1]] + [{W: "Suzy"}])
        assert actual_causes == expected_actual_causes
