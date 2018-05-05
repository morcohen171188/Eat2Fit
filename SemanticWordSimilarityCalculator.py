from nltk.corpus import wordnet


def calculateSemanticWordSimilarity(word1, word2):
    result_list = []
    result = 0.0
    # Computing English word similarity using Li method
    # Not taking the most common syn beacuse food is not always the most common
    synword1 = wordnet.synsets(word1)
    synword2 = wordnet.synsets(word2)

    if synword1 and synword2:
        for syn1 in synword1:
            for syn2 in synword2:
                s = syn1.wup_similarity(syn2)
                if s is not None:
                    result_list.append(s)
        result = max(result_list)

    return result


