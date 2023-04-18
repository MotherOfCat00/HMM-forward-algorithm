# Algorytm Viterbiego
import random


def test_algorithm(start_p, trans_p, emit_p, series):
    series_length = len(series) - 1
    status = series[0]
    prob = start_p[status]
    print("START")
    print("Start ->", status, prob)

    for i in range(1, series_length - 1):
        new_status = series[i]
        prob = trans_p[status][new_status] * prob
        print(status, "->",  new_status, prob)
        status = new_status

    prob = emit_p[status][series[series_length]] * prob
    print(series[series_length-1], "->", series[series_length], prob)
    print("END")
    return prob


def check_corr(series):
    result = True
    if len(series) < 2:
        result = False
    for i in range(0, len(series) - 1):

        if series[i] == "S1" or series[i] == "S2":
            pass
        else:
            result = False

    if series[-1] != "O1" and series[-1] != "O2" and series[-1] != "O3":
        result = False

    return result


def rand_series(obser, state):
    length = random.randint(1, 20)
    ser = []
    array = state+state+state+state+state+state+obser
    for i in range (0, length):
        ser.append(random.choice(array))
    #  print(ser)
    return ser


observations = ("O1", "O2", "O3")
states = ("S1", "S2")
start_p = {"S1": 0.6, "S2": 0.4}
trans_p = {
    "S1": {"S1": 0.7, "S2": 0.3},
    "S2": {"S1": 0.4, "S2": 0.6},
}
emit_p = {
    "S1": {"O1": 0.5, "O2": 0.4, "O3": 0.1},
    "S2": {"O1": 0.1, "O2": 0.3, "O3": 0.6},
}
count = 0
for i in range(0, 500):
    randser = rand_series(observations, states)
    series = ["S1", "S1", "S2", "S1", "S1", "S2", "S1", "S1", "S2", "S1", "S1", "S1", "S2", "S1", "O3"]
    # series = ["S1", "O2"]
    res = check_corr(randser)
    if res:
        prob = test_algorithm(start_p, trans_p, emit_p, randser)
        print(randser)
        print("Probability %0.8f%%" % (prob * 100))
        count += 1
    # else:
    #     print("Insert correct series")
print(count)

