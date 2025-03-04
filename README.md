
This contains work written by Andy Worcester. Work leveraged chatGPT for various pieces of code,
and leveraged others' work for the metrics' reporting.

# Purpose

To better understand road network algorithms that use preprocessing, Contraction Hierarchies (CH) and
Transit Node Routing (TNR) were built and experimented upon.

For SP 2025 school class group project, University of Colorado - Colorado Springs (UCCS),
CS 5080, taught by Professor Philip Brown.

CH-based TNR is implemented where a "k" value is chosen representing the top "k" nodes in the node ordering
provided by CH. CH uses the node orderings from CH, but otherwise does its additional pre-processing and queries
on the original graph, not the CH graph.

The 4 variations of CH are:
-Offline: both edge difference and degree-based
-online:  both edge difference and degree-based

Tie breakers for CH are to pick a node with the least number of edges being added for both cases.

# Main run:

**Run** "Project1Analysis.py" to:
- generate graphs of Falcon without shortcuts added, add with shortcuts for each CH type.
- Run tests on CH and TNR against built-in shortest path functions to help ensure correctness.
- Run metric tests on CH and TNR to form final metrics.
On a typical PC may take around an hour to run this.

**Run** TDD testing framework for all CH variations:
run "TestVerification.py" to do this analysis. It tests against the hard coded "example Graph.png". For Each CH variation, it tests for:
- preprocessing: node ordering returned, and shortcuts that were added
- query: to have the proper length returned, and proper nodes explored during the query.

Note: although I could've used pytest, you can be assured here that all tests passed when the exit code returns 0 here.
If the exit code is "1", an error message has been printed about the error found.

**Run** other example graphs with small graph tests in the algorithm files: "CHAlgorithmBase", "TNRAlgorithmExtension.py"
However, these files are mainly used as the code housing for the CH algorithm and the TNR algorithms respectively.

Note: TNRAlgorithmExtension.py (TNR alg), per its name, is an extension of CHAlgorithmBase.py (CH alg), but only via
duck-typing. It calls CH to complete the TNR algorithm, but it is not an actual proper subclass of CH algorithm.



Final Note: A few of the output .png graphs of Falcon (and the TDD example) are provided.