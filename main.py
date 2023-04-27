

def test_algorithm(observations, states, start_p, trans_p, emit_p):
    probability = {"H": {},
                   "L": {}}  # create prob matrix
    print(probability)
    prob_h = start_p['H'] * emit_p['H'][observations[0]]  # start to 1st observation prob for H
    prob_l = start_p['L'] * emit_p['L'][observations[0]]  # start to 1st observation prob for L
    previous_prob_h = prob_h
    previous_prob_l = prob_l
    probability.update({"H": {observations[0]: prob_h}})  # add prob to dict
    probability.update({"L": {observations[0]: prob_l}})  # add prob to dict

    #  Forward algorithm to calculate the probability of generating given seq:
    for i in range (1, len(observations)):
        prob_h = previous_prob_h * trans_p["H"]["H"] * emit_p['H'][observations[i]] + \
                 previous_prob_l * trans_p["L"]["H"] * emit_p['H'][observations[i]]
        prob_l = previous_prob_l * trans_p["L"]["L"] * emit_p["L"][observations[i]] + \
                 previous_prob_h * trans_p["H"]["L"] * emit_p["L"][observations[i]]
        probability["H"][observations[i] + str(i)] = prob_h
        probability["L"][observations[i] + str(i)] = prob_l
        previous_prob_h = prob_h
        previous_prob_l = prob_l
    print(probability)

    return probability


def viterbi_algorithm(observations, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        print(st)
        V[0][st] = {"prob": start_p[st] * emit_p[st][observations[0]], "prev": None}

    for t in range(1, len(observations)):
        V.append({})
        for st in states:
            max_tr_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob * emit_p[st][observations[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

    for line in dptable(V):
        print(line)

    opt = []
    max_prob = 0.0
    best_st = None

    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st

    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print("The steps of states are " + " ".join(opt) + " with highest probability of %s" % max_prob)
    return V


def dptable(V):
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


def check_seq(seq):
    result = True
    for i in range(0, len(seq)):
        if seq[i] == "A" or seq[i] == "C" or seq[i] == "T" or seq[i] == "G":
            pass
        else:
            result = False
    return result


states = ("H", "L")
start_p = {"H": 0.5, "L": 0.5}
trans_p = {
    "H": {"H": 0.5, "L": 0.5},
    "L": {"H": 0.4, "L": 0.6},
}
emit_p = {
    "H": {"A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2},
    "L": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3},
}
sequence = list('GGCTGAC')
path = list('LLHHHHLLL')

res = check_seq(sequence)
if res:
    prob = test_algorithm(sequence, states, start_p, trans_p, emit_p)
    V = viterbi_algorithm(sequence, states, start_p, trans_p, emit_p)
    dptable(V)
else:
    print("Insert correct sequence(allowed: A C T G")

