# program to split the sample into training and testing datasets
import sys

# opening the files
#sample = open("C:\\Users\\ericr\\pycharm-workspace\\ML-BOT-NAIVE-BAYES-DTS\\Sampling\\samples.txt", "r")
sample = open(sys.argv[1], "r")

training_dataset = open("training_dataset.txt", "w")
testing_dataset = open("testing_dataset.txt", "w")


sample_number = len(sample.readlines())
print("Total number of examples = ", sample_number)

training_cut_parameter = int(sample_number * 0.7)
print("Number of training examples = ", training_cut_parameter)
testing_cut_parameter = int(sample_number * 0.3)
print("Number of testing examples = ", testing_cut_parameter)

# return to the sample file start
sample.seek(0)

# splitting the sample into 70% training dataset
for example in range(training_cut_parameter):
    training_dataset.write(sample.readline())

# and 30% testing dataset
for example in range(testing_cut_parameter):
    testing_dataset.write(sample.readline())

# safely closing the files
sample.close()
training_dataset.close()
testing_dataset.close()
