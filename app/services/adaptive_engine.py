import math

def irt_probability(theta, difficulty):
    return 1 / (1 + math.exp(-(theta - difficulty)))

def update_ability(theta, difficulty, correct, lr=0.1):
    p = irt_probability(theta, difficulty)

    if correct:
        theta = theta + lr * (1 - p)
    else:
        theta = theta - lr * p

    return theta