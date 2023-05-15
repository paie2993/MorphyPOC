import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from nltk.corpus import wordnet
from nltk.corpus.reader import ADJ_SAT, ADJ, ADV, NOUN, VERB

import query_engine
from chunker import chunk
from definition import Definition
from separators import sentence_split, word_trim

THREADS = 5


class TextProcessor:
    __pos = [ADJ, ADJ_SAT, ADV, NOUN, VERB]

    def __sentences(self, text):
        return [sentence.strip() for sentence in re.split(sentence_split, text)]

    def __words(self, sentence):
        return [brute_word.strip(word_trim) for brute_word in re.split(" ", sentence)]

    def __collocations(self, words):
        collocations = []
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                collocation_components = words[i: j + 1]
                collocations.append(" ".join(collocation_components))
        return collocations

    def process_text(self, text) -> list:
        # the set of already processed base forms; we don't want to process a base form multiple times
        processed = {}
        result_definitions: list[Definition] = []
        # get all the sentences from the given text; needed for collocations (they can't exist inter-sentence)
        sentences = self.__sentences(text)

        for sentence in sentences:
            # let's call words or collocations 'tokens'
            words = self.__words(sentence)
            collocations = self.__collocations(words)
            tokens = [*words, *collocations]

            # all the base forms for each token
            base_forms = {base_form for token in tokens for base_form in self.all_base_forms(token, processed)}

            # all the definitions for all the base forms present in the sentence
            glosses = query_engine.definitions(base_forms)
            result_definitions.extend(glosses)

        return result_definitions

    def all_base_forms(self, token, processed):
        forms = []
        for p in self.__pos:
            base_forms_for_pos = wordnet._morphy(token, p)
            if base_forms_for_pos is not None:
                for base_form in base_forms_for_pos:
                    if base_form not in processed:
                        forms.append(base_form)
                        processed = {*processed, base_form}
        return forms


text_processor = TextProcessor()

if __name__ == '__main__':
    wordnet.ensure_loaded()

    text = '''She loved the smell of fresh flowers in the spring.
He couldn’t believe his luck when he found a hundred-dollar bill on the street.
They decided to go for a hike in the mountains and enjoy the scenery.
She was nervous about her presentation, but she did a great job and impressed everyone.
He always dreamed of becoming a famous writer, but he never finished his novel.'''
    chunks = chunk(text, THREADS)

    for chunk in chunks:
        definitions: list[Definition] = text_processor.process_text(chunk)
        for definition in definitions:
            print(definition)

    # executor = ThreadPoolExecutor(max_workers=THREADS)
    #
    # futures = [executor.submit(text_processor.process_text, chunk) for chunk in chunks]
    # for completed in as_completed(futures):
    #     result = completed.result()
    #     print(result)
