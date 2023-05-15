from nltk.corpus import wordnet

from definition import Definition


def definitions(base_forms) -> list[Definition]:
    result_definitions = []
    for base_form in base_forms:

        # to build each definition, keep track of definition count
        counter = 1
        current_definitions = []

        # fetch all synsets for a given base form (each word can appear in multiple synsets)
        synsets = wordnet.synsets(base_form)

        for synset in synsets:
            # each synset in the WordNet database has only one definition
            definition = synset.definition()
            current_definitions.append(str(counter) + '. ' + definition)
            counter += 1
        result_definitions.append(Definition(base_form, current_definitions))

    return result_definitions
