from examples import rock_throwing, forest_fire

if __name__ == "__main__":
    print("Forest fire (disjunctive model):")
    forest_fire(disjunction=True)

    print("\nForest fire (conjunctive model):")
    forest_fire(disjunction=False)

    print("\nRock throwing:")
    rock_throwing()
