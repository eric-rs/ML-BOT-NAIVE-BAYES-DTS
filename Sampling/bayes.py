from Node import Node
import random

PLAYING_EXAMPLES = [(True, False), (True, False), (True, True),
                    (True, False), (True, False), (False, True),
                    (False, False), (False, True), (False, True),
                    (False, True), (False, False), (False, True),
                    (False, True)]

class BayesNet:
    # The nodes in the network
    nodes = []

    # Build the initial network
    def __init__(self):
        self.nodes.append(Node("Visit to Asia", [], [0.01])) #index=0
        self.nodes.append(Node("Smoking", [], [0.5])) #index=1


        '''
                Visit Asia+ |   Visit asia-
            T    0.5                0.1
        '''
        self.nodes.append(Node("Tuberculosis",
                               [self.nodes[0]],
                               [0.5, 0.1])) #index=2

        '''
                Lung Cancer+ |   Lung Cancer-
        Smoking    0.10                0.01
        '''
        self.nodes.append(Node("Lung Cancer",
                               [self.nodes[1]],
                               [0.1, 0.01])) #index=3
        '''
                Bronchitis+ |   Bronchitis-
        Smoking    0.6                0.3
        '''
        self.nodes.append(Node("Bronchitis",
                               [self.nodes[1]],
                               [0.6, 0.3])) #index=4
        '''
            Tuberculosis | Lung Cancer | Tuberculosis or Cancer = True |  Tuberculosis or Cancer = False
                True            True                    1                               0
                True            False                   1                               0
                False           True                    1                               0
                False           False                   0                               1

        '''
        self.nodes.append(Node("Tuberculosis or Cancer",
                               [self.nodes[2], self.nodes[3]],
                               [1, 1, 1, 0])) #index=5


        '''
                Tuberculosis or Cancer+ | Tuberculosis or Cancer-
         XRay           0.98                        0.05
        '''
        self.nodes.append(Node("X-Ray Result", [self.nodes[5]], [0.98, 0.05])) #index=6

        '''
                    Tuberculosis or Cancer | Bronchitis | Dyspnea=True | Dyspnea=False
                            True            True               0.90             0.1
                            True            False              0.70             0.3
                            False           True               0.80             0.2
                            False           False              0.10             0.90


        '''
        self.nodes.append(Node("Dyspnea", [self.nodes[5], self.nodes[4]],
                          [0.90,0.70,0.80,0.10]))
        self.nodes.append(self.nodes.pop(5))

    # Prints the current state of the network to stdout
    def printState(self):
        strings = []
        for node in self.nodes:
            strings.append(node.name + " = " + str(node.value))

        print(", ".join(strings))

    def calculatePlayOutsideProbabilities(self, rainingInstances):
        playing = [0, 0]
        total = [0, 0]
        prob = [0.0, 0.0]

        for sample in rainingInstances:
            if sample[0]:
                playing[0] += 1 if sample[1] else 0
                total[0] += 1
            else:
                playing[1] += 1 if sample[1] else 0
                total[1] += 1

        prob[0] = float(playing[0]) / float(total[0])
        prob[1] = float(playing[1]) / float(total[1])

        return prob

    '''
    This method will sample the value for a node given its
    conditional probability.
    '''
    def sampleNode(self, node):
        node.value = True if random.random() <= node.conditionalProbability() else False

    '''
    This method assigns new values to the nodes in the network by
    sampling from the joint distribution.  Based on the PRIOR-SAMPLE
    from the text book/slides
    '''
    def priorSample(self):
        for n in self.nodes:
            self.sampleNode(n)

        return self.nodes
    '''
    This method will return true if all the evidence variables in the
    network have the value specified by the evidence values.
    '''
    def testModel(self, indicesOfEvidenceNodes, evidenceValues):
        for i in range(len(indicesOfEvidenceNodes)):
            if (self.nodes[indicesOfEvidenceNodes[i]].value != evidenceValues[i]):
                return False

        return True

    def printState(self):
        strings = []
        for node in self.nodes:
            strings.append(node.name + " = " + str(node.value))

        print(", ".join(strings))

    '''
        this method receives an number n of samples that will generate with prior sampling
        the result is an array of maps consisting of key values
        EX:
        [{Visit to Asia:False},{Smoking:False},{Tuberculosis:False},{Lung Cancer:False},{Bronchitis:True},{Tuberculosis or Cancer:False},{X-Ray Result:False},{Dyspnea:True}]
    '''
    def getSamples(self, n):
        result = []
        sublist = []
        for i in range(n):
            for node in self.priorSample():
                sublist.append({node.name: node.value})

            result.append(sublist)
            #self.printState()

        return result

    '''
        this method receives an number n of samples that will generate with prior sampling
        the result is file named sampling.txt created in the folder of tthe project with strings consisting of key values
        EX:
        {Visit to Asia:False},{Smoking:False},{Tuberculosis:False},{Lung Cancer:False},{Bronchitis:True},{Tuberculosis or Cancer:False},{X-Ray Result:False},{Dyspnea:True}

    '''
    def beginSamplingAndSaveToFile(self,n):
        result = []

        for i in range(n):
            strings = []
            for node in self.priorSample():
                strings.append(node.name + ":" + str(node.value))

            self.appendStringToFile("samples.csv", ",".join(strings))

            #self.printState()


        return result

    # helper method that gets a file name and a string and saves the string to the file
    def appendStringToFile(self, filename, input):
        with open(filename, 'a') as file:
                file.write(input + "\n")

if __name__ == "__main__":
    with open("samples.csv",'w'):
        pass
    b = BayesNet() # Creates a bayes net
    num = input("Numero:")
    nodes = b.beginSamplingAndSaveToFile(int(num)) #creates and saves 100 thousands of samples from the net
    print("Concluido.")
    '''
    strings = []
    for node in nodes:
        for colums in node:
            strings.append(colums)

    print(strings)

    '''
