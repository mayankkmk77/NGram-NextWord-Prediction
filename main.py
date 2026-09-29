import re
from collections import Counter

# ==========================================
# 1. READ DATASET
# ==========================================

with open("data/corpus.txt", "r", encoding="utf-8") as file:
    text = file.read()


# ==========================================
# 2. TOKENIZATION
# ==========================================

words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

print("Total words:", len(words))


# ==========================================
# 3. CREATE N-GRAMS
# ==========================================

bigrams = list(zip(words, words[1:]))
trigrams = list(zip(words, words[1:], words[2:]))


# ==========================================
# 4. COUNT FREQUENCIES
# ==========================================

word_counts = Counter(words)

bigram_counts = Counter(bigrams)

trigram_counts = Counter(trigrams)

bigram_context_counts = Counter(bigrams)


# ==========================================
# 5. VOCABULARY
# ==========================================

vocabulary = set(words)

vocab_size = len(vocabulary)

print("Vocabulary size:", vocab_size)


# ==========================================
# 6. BIGRAM PROBABILITY
# ==========================================

def bigram_probability(word1, word2):

    count = bigram_counts[(word1, word2)]

    context_count = word_counts[word1]

    probability = (
        count + 1
    ) / (
        context_count + vocab_size
    )

    return probability


# ==========================================
# 7. TRIGRAM PROBABILITY
# ==========================================

def trigram_probability(word1, word2, word3):

    count = trigram_counts[(word1, word2, word3)]

    context_count = bigram_context_counts[(word1, word2)]

    probability = (
        count + 1
    ) / (
        context_count + vocab_size
    )

    return probability


# ==========================================
# 8. BIGRAM NEXT-WORD PREDICTION
# ==========================================

def predict_bigram(input_word):

    predictions = []

    input_word = input_word.lower()

    for (word1, word2), count in bigram_counts.items():

        if word1 == input_word:

            probability = bigram_probability(
                word1,
                word2
            )

            predictions.append(
                (word2, probability)
            )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return predictions[:3]

# ==========================================
# 9. TRIGRAM NEXT-WORD PREDICTION
# ==========================================

def predict_trigram(word1, word2):

    predictions = []

    word1 = word1.lower()
    word2 = word2.lower()

    for (w1, w2, w3), count in trigram_counts.items():

        if w1 == word1 and w2 == word2:

            probability = trigram_probability(
                w1,
                w2,
                w3
            )

            predictions.append(
                (w3, probability)
            )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return predictions[:3]

# ==========================================
# 10. INTERACTIVE NEXT-WORD PREDICTION
# ==========================================

print("\n================================")
print(" N-GRAM NEXT-WORD PREDICTOR")
print("================================")

user_input = input("\nEnter text: ").strip().lower()

input_words = re.findall(
    r"\b[a-zA-Z]+\b",
    user_input
)


# Check the number of words entered

if len(input_words) == 0:

    print("Please enter some text.")

elif len(input_words) == 1:

    # Bigram prediction
    last_word = input_words[-1]

    predictions = predict_bigram(last_word)

    print("\nUsing Bigram Model")
    print("Next-word predictions:")

    if predictions:

        for i, (word, probability) in enumerate(
            predictions, start=1
        ):

            print(
                f"{i}. {word} "
                f"(probability: {probability:.4f})"
            )

    else:

        print("No prediction found.")


else:

    # Trigram prediction
    word1 = input_words[-2]
    word2 = input_words[-1]

    predictions = predict_trigram(
        word1,
        word2
    )

    print("\nUsing Trigram Model")
    print("Context:", word1, word2)
    print("Next-word predictions:")

    if predictions:

        for i, (word, probability) in enumerate(
            predictions, start=1
        ):

            print(
                f"{i}. {word} "
                f"(probability: {probability:.4f})"
            )

    else:

        print(
            "No prediction found for this context."
        )


# ==========================================
# 11. MODEL EVALUATION
# ==========================================

print("\n================================")
print(" MODEL EVALUATION")
print("================================")

test_cases = [
    ("student", "is", "studying"),
    ("student", "is", "learning"),
    ("student", "is", "preparing"),
    ("teacher", "is", "teaching"),
    ("teacher", "is", "explaining"),
    ("computer", "is", "running"),
    ("computer", "is", "processing"),
    ("machine", "learning", "helps"),
    ("language", "model", "predicts"),
    ("system", "generates", "a")
]

top1_correct = 0
top3_correct = 0

for word1, word2, actual_word in test_cases:

    predictions = predict_trigram(word1, word2)

    predicted_words = [word for word, probability in predictions]

    if len(predicted_words) > 0:
        if predicted_words[0] == actual_word:
            top1_correct += 1

        if actual_word in predicted_words:
            top3_correct += 1

total_tests = len(test_cases)

top1_accuracy = (top1_correct / total_tests) * 100
top3_accuracy = (top3_correct / total_tests) * 100

print("Total test cases:", total_tests)
print("Top-1 Correct:", top1_correct)
print("Top-3 Correct:", top3_correct)

print(f"Top-1 Accuracy: {top1_accuracy:.2f}%")
print(f"Top-3 Accuracy: {top3_accuracy:.2f}%")