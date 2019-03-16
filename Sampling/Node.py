# A node in the bayes network
class Node:
    def __init__(self, n, pa, pr):
        self.name = n
        self.parents = pa
        self.probs = pr
        self.value = None

    '''
    Returns conditional probability of value "true" for the current
    node based on the values of the parent node/s.
    '''
    def conditionalProbability(self):
        index = 0

        for i, p in enumerate(self.parents):
            if p.value == False:
                index += 2 ** (len(self.parents) - i - 1)
        return self.probs[index]
