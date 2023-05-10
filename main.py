import pandas as pd
import cowsay

#  Function to test sum of probabilities of each state (must be 1.0 for transitios and 1.0 for observations)
def test_matrix_prob(matrix1, matrix2):
    result = True
    for n in range(matrix1.shape[0]):
        sum_value = round(matrix1[n:n+1].sum(1).values[0], 5)
        if sum_value == 1.0:
            pass
        else:
            result = False

    for n in range(matrix2.shape[0]):
        sum_value = round(matrix2[n:n+1].sum(1).values[0], 5)
        if sum_value == 1.0:
            pass
        else:
            result = False

    return result


#  Function to test shapes of matrixes (transitions must be quadratic) and correctness of headers and indexes names
def test_matrix_shape(transitions, emissions, chain):
    result = True
    transitions_shape = transitions.shape

    if transitions_shape[0] == transitions_shape[1]:
        pass
    else:
        result = False

    emissions_headers = list(emissions.columns)
    emssions_index = list(emissions.head().index)
    transitions_index = list(transitions.head().index)[1:]

    if emssions_index == transitions_index:
        pass
    else:
        result = False

    for item in chain:
        if item in emissions_headers:
           pass
        else:
            result = False

    return result


def forward_algorithm(transitions, emissions, chain):
    states = list(transitions.columns)  # list of states

    probabilities = {}  # empty dict
    keys = range(1, transitions.shape[0])  # create keys to add to dict

    for i in keys:
        probabilities[i] = {}  # add keys to dict

    # calculate
    for m in range(1, len(states)):
        probabilities[m][chain[0]] = transitions[states[m]].values[0] * emissions[chain[0]].values[m-1]

    # previous observation
    previous = chain[0]

    #  forward algorithm:
    for k in range(1, len(chain)):  # this loop change observation
        obser_number = str(k) + '_' + chain[k]  # create key for observation
        for i in range(1, len(states)):  # this loop change state
            probabilities[i][obser_number] = 0
            for j in range(1, len(states)):  # this loop adds probabilities for 'k' observation at 'i' state
                probabilities[i][obser_number] = probabilities[i][obser_number] + probabilities[j][previous] * \
                                             transitions[states[i]].values[j] * emissions[chain[k]].values[i-1]
        previous = obser_number  # remember previous observation name

    total_probability = 0
    #  sum probabilities
    for i in keys:
        total_probability = total_probability + probabilities[i][previous]

    return total_probability


transitions_matrix = pd.read_csv('transitions_matrix.csv', header=0, index_col=0)  # read transitions matrix
# (in next steps emssions matrix and chain) to DataFrame
emission_matrix = pd.read_csv('emissions_matrix.csv', header=0, index_col=0)
chain = pd.read_csv('chain.csv', header=None)
observations = chain[0:1].values[0]
print("Observations:", observations)
print(transitions_matrix)
print(emission_matrix)
result = test_matrix_prob(transitions_matrix, emission_matrix)
result2 = test_matrix_shape(transitions_matrix, emission_matrix, observations)
#  If both 'test matrix' functions return True 'forward_algorithm' calculate the probability
if result:
    if result2:
        total = forward_algorithm(transitions_matrix, emission_matrix, observations)
        # print("Probability of given path is:", total)

else:
    print("Check instruction")


