
from collections import Counter
import string

# Define your list of text (e.g. text_list)
text_list = processed_texts

# Split the text into individual words and create a list of all words
all_words = [word for text in text_list for word in text.split()]

# Count the frequency of each word using the Counter object
word_freq = Counter(all_words)

# Print the 10 most frequent words
print(word_freq.most_common(20))
