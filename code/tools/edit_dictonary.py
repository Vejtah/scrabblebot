from tqdm import tqdm

import enchant
d = enchant.Dict("en_US")


with open("/home/vpalaga/orgs/vp/sb/virtual/enable1.txt", "r") as file:
    file_content = file.read()
    file.close()

save = open("/home/vpalaga/orgs/vp/sb/virtual/save.txt", "a")

file = file_content.split("\n")

print(file)

amt_words = len(file)

words_test = []

for _ in range(100):
    words_test.append(file[_])

def is_word(word: str) -> bool:
    # Basic checks
    if len(word) <= 2:
        return False
    if not word.isalpha():
        return False
    
    # Optional: Exclude all-uppercase or weird cApItAlIzAtIoNs
    if not word.islower():
        return False


    # Check dictionary
    if not d.check(word.lower()):
        return False

    # Optional: Exclude archaic forms that have synonyms suggested by enchant
    suggestions = d.suggest(word.lower())
    if suggestions and suggestions[0].lower() != word.lower():
        # might indicate this is archaic or a variant
        return False

    return True

for word in tqdm(file):
    if is_word(word):
        save.write(f"{word}\n")

save.close()

 
with open("/home/vpalaga/orgs/vp/sb/virtual/save.txt", "r") as save:
    save_contend = save.read()
    save.close()

len_save = len(save_contend.split("\n"))
print(len_save)
print(f"finished with {100 * (1 - (len_save / amt_words))}% of the words eliminated")

