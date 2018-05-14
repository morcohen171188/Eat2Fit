from nltk.corpus import wordnet

def calculateSemanticWordSimilarity(word1, wordList):
    result_list = []
    result = 0.0
    # Computing English word similarity using Li method
    # Not taking the most common syn beacuse food is not always the most common
    synword1 = wordnet.synsets(word1)

    for word in wordList:
        synword2 = wordnet.synsets(word)

        if synword1 and synword2:
            #for syn1 in synword1[:3]:
                #for syn2 in synword2[:3]:
                    #s = syn1.wup_similarity(syn2)
            s = synword1[0].wup_similarity(synword2[0])
            if s is not None:
                result_list.append(s)
    result = max(result_list) if (result_list != []) else 0

    return result


