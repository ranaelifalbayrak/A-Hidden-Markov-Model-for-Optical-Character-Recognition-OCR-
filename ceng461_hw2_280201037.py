import numpy as np

np.set_printoptions(suppress=True)

letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def collect_data(path):
    with open(path,"r") as file:
        data = file.readlines()
        for d in range (0, len(data)):
            data[d] = data[d].strip()
            
    file.close()
    return data

def calculate_hmm_probabilities(actual_words, ocr_outputs, letters):

    size = len(letters)
    initial_letter_counts = np.zeros(size)
    transition_counts = np.zeros((size,size))
    emission_counts = np.zeros((size,size))
    for j in range(0,len(actual_words)):
        word = actual_words[j]
        word = word.strip()
        ocr_output = ocr_outputs[j]
        ocr_output = ocr_output.strip()
        initial = word[0]
        initial_index = letters.index(initial)
        initial_letter_counts[initial_index] += 1
        for i in range (0,len(word)-1):
            current_letter = word[i]
            next_letter = word[i + 1]
            current_letter_index = letters.index(current_letter)
            next_letter_index = letters.index(next_letter)
            transition_counts[current_letter_index][next_letter_index] += 1
        for i in range (0,len(word)):
            actual_letter = word[i]
            ocr_output_letter = ocr_output[i]
            actual_letter_index = letters.index(actual_letter)
            ocr_output_letter_index = letters.index(ocr_output_letter)
            emission_counts[actual_letter_index][ocr_output_letter_index] += 1


    initial_prob = []
    transition_prob = []
    emission_prob = []

    for count in initial_letter_counts:
        initial_prob.append(count/50000)
    for count_row in transition_counts:
        row = []
        for count in count_row:
            row.append(count/sum(count_row))
        transition_prob.append(row)
    for count_row in emission_counts:
        row = []
        for count in count_row:
            row.append(count/sum(count_row))
        emission_prob.append(row)
    
    transition_prob = np.array(transition_prob)
    emission_prob = np.array(emission_prob)
    initial_prob = np.array(initial_prob)

    return initial_prob, transition_prob, emission_prob
   
def viterbi(ocr_output, transition_prob, emission_prob, initial_prob, letters):

    letter_indexes = []
    for letter in ocr_output:
        letter_indexes.append(letters.index(letter))

    rows = transition_prob.shape[0]
    cols = len(letter_indexes)

    table = np.zeros((rows, cols))
    path = np.zeros((rows, cols), dtype=int)

    for i in range(len(initial_prob)):
        table[i][0] = initial_prob[i] * emission_prob[i][letter_indexes[0]]

    for t in range(1, cols):
        for n in range(rows):
            seq_probs = np.zeros(rows)  
            for i in range(rows):  
                seq_probs[i] = table[i][t - 1] * transition_prob[i][n] * emission_prob[n][letter_indexes[t]]
            max_index = np.argmax(seq_probs)
            max_value = seq_probs[max_index]
            table[n][t] = max_value
            path[n][t] = max_index

    best_seq = np.zeros(cols, dtype=int)
    last_column_values = []

    for row in range(rows):
        last_column_values.append(table[row][cols - 1])

    best_seq[-1] = np.argmax(last_column_values)

    for t in range(cols - 2, -1, -1):
        best_seq[t] = path[best_seq[t + 1]][t + 1]


    most_likely_seq = []
    for state in best_seq:
        most_likely_seq.append(letters[state])

    return most_likely_seq


 

actual_words = collect_data("data_actual_words.txt")
ocr_outputs = collect_data("data_ocr_outputs.txt")

initial_prob, transition_prob, emission_prob = calculate_hmm_probabilities(actual_words[:50000], ocr_outputs[:50000],letters)

#printing initial probabilities
for i in range(0, len(letters)):
    print("P("+letters[i]+"_1):",initial_prob[i])
print()
#printing transition probabilities
for i in range(0,len(transition_prob)):
    for j in range(0,len(transition_prob[i])):
        print("P("+letters[j]+"_n|"+letters[i]+"_(n-1)):",transition_prob[i][j])
print()
#printing emission probabilities
for i in range(0,len(emission_prob)):
    for j in range(0,len(emission_prob[i])):
        print("P("+letters[j]+"_n|"+letters[i]+"_n):",emission_prob[i][j])

print()

faulty_letters = 0
corrected_letters = 0

for i in range(50000, 60244):  
    actual_word = actual_words[i]
    ocr_output = ocr_outputs[i]
   
    
    for l in range (0, len(actual_word)):
        if actual_word[l] != ocr_output[l]:
            faulty_letters += 1
        

    estimated_word = viterbi(ocr_output, transition_prob, emission_prob, initial_prob,letters)
    estimated_word = ''.join(estimated_word)

    if ocr_output != estimated_word:
        print("Actual Word:", actual_word)
        print("OCR Output:", ocr_output)
        print("Estimated Word:", estimated_word)
        print()

    for l in range(0, len(actual_word)):
        if actual_word[l] != ocr_output[l] and estimated_word[l] == actual_word[l]:
            corrected_letters += 1
    
    
print("Number of Faulty Letters:",faulty_letters)
print("Number of Corrected Letters:",corrected_letters)