from setuptools import setup

setup(
    name="pycausalexplainer",
    packages=["causal_explainer"],
    version="0.1.0",
    description="A simple Python implementation of causes and explanations based on the Halpern-Pearl definition of actual causality using structural causal models",
    author="Kevin McAreavey",
    author_email="kevin.mcareavey@bristol.ac.uk",
    license="MIT",
    install_requires=["frozendict", "networkx", "pygraphviz"],
    classifiers=[],
    include_package_data=True,
    platforms="any",
)
