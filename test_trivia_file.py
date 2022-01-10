import random 
# omg hi
with open('trivia_questions.txt', 'r', encoding='cp437') as File1:
    # from video in case we need later: lines = File1.readlines()
    questions = []
    for line in File1:
        questions.append(line)
File1.close()

# Text file with all answers
with open('trivia_answers.txt', 'r', encoding='cp437') as File2:
    # from video in case we need later: lines = File2.readlines()
    answers = []
    for line in File2:
        answers.append(line)
File2.close()
            
# Filter the question list to remove \n
filtered_questions = []
for item in questions:
    filtered_questions.append(item.strip())

# Filter the answer list to remove \n
filtered_answers = []
for item in answers:
    filtered_answers.append(item.strip())

print(filtered_answers)

# Actual Game

trivia = True
# While game is running
while trivia == True:
    # Make a random number generator to get random questions
    num_questions = len(filtered_questions) - 1
    random_question_number = random.randint(0,num_questions)
    print("Your question is: ", filtered_questions[random_question_number])
    

