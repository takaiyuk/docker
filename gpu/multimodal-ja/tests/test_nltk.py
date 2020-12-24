import nltk

# nltk.download()


# def test_nltk():
#     sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
#     tokens = nltk.word_tokenize(sentence)
#     token_expected = [
#         "At",
#         "eight",
#         "o'clock",
#         "on",
#         "Thursday",
#         "morning",
#         "Arthur",
#         "did",
#         "n't",
#         "feel",
#         "very",
#         "good",
#         ".",
#     ]
#     assert tokens == token_expected, print(
#         f"acutual: {tokens}, expected: {token_expected}"
#     )

#     tagged = nltk.pos_tag(tokens)
#     tag_expected = [
#         ("At", "IN"),
#         ("eight", "CD"),
#         ("o'clock", "JJ"),
#         ("on", "IN"),
#         ("Thursday", "NNP"),
#         ("morning", "NN"),
#     ]
#     assert tagged[0:6] == tag_expected, print(
#         f"acutual: {tagged[0:6]}, expected: {tag_expected}"
#     )
