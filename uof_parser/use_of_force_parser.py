import re


def convert_input_to_regex(raw_input):
    """
    ... is replaced with \s?.+\s
    spaces are replaced with \s+
    :param raw_input: string
    :return: string
    """
    return raw_input.replace('...', r'\s?.+\s').replace(' ', r'\s+')


def is_enumerated_list(block_of_text):
    """
    Given a block of text, determine if there is some sort of enumerated list. This accounts for the following
    structures:
    Enumerated by letters
        (a)
        (b)
        etc.
    :param block_of_text: string
    :return: boolean
    """

    # Check if the block of text has list that is denoted by letters within parentheses. ex: (a) (b) etc.
    matches = re.findall(r'\(\w\)', block_of_text)
    if len(matches) > 1:
        return True

    return False


def clean_content_list(content_as_a_list):
    """
    This is a helper function to clean a list so that it starts with a non blank value or a unique phrase.
    Common phrases are removed because they might be a footer. As an example, Footers contain common language such as
    "Published with permission by..."
    :param content_as_a_list: list of strings
    :return: list of strings
    """

    ignore_common_phrases = [r'Use of Force - \d', 'Published with permission by']
    while True:
        # Pop values out of sentence_split_by_line until it starts with a non blank value
        while content_as_a_list[0] == '':
            content_as_a_list.pop(0)

        # Pop out lines that should be ignored. This includes common headers or footers seen on pages.
        for ignore_common_phrase in ignore_common_phrases:
            if re.findall(ignore_common_phrase, content_as_a_list[0]):
                content_as_a_list.pop(0)
                break
        else:
            break
    return content_as_a_list


class UOFParser:
    content = ''
    content_as_sentences = []
    content_as_lines = []
    lexipol = None
    year_of_policy = ''

    def __init__(self, content):
        # Save the content as a property of the class.
        # Split the content by periods for a list of sentences.
        # Split the content by lines for a list of lines.
        self.content = content
        self.content_as_sentences = content.split('.')
        self.content_as_lines = content.split('\n')

        # Determine whether the content is lexipol and save that as a property of the class
        self.lexipol = 'lexipol' in content.lower()
        if self.lexipol:
            print('This document has been identified as a Lexipol document\n')
        else:
            print('This document is not a Lexipol document\n')

        # Get year of policy
        if self.lexipol:
            regex_to_find_year = r'copyright lexipol.+(\d{4})\/\d{2}\/\d{2}'
            for line in self.content_as_lines:
                matches = re.findall(regex_to_find_year, line.lower())
                if matches:
                    self.year_of_policy = matches[0]
                    break

    def get_line_location_from_sentence_location(self, sentence_location_integer):
        """
        Finds the line number of a sentence given the sentence's location integer.
        :param sentence_location_integer: integer
        :return: integer
        """
        # Get the sentence and split it by line breaks
        sentence = self.content_as_sentences[sentence_location_integer]
        sentence_split_by_line = sentence.split('\n')
        clean_sentence_split_by_line = clean_content_list(sentence_split_by_line)

        for i, line in enumerate(self.content_as_lines):
            if clean_sentence_split_by_line[0] in line:
                # If there are no additional lines to find, then return this location integer
                if len(clean_sentence_split_by_line) == 1:
                    return i

                # Confirm this is the correct line by checking if the next lines are equal. If any are not, then
                # go back into the for loop. Make sure to ignore periods in the content_as_lines list.
                additional_line_counter = 0
                for additional_line in clean_sentence_split_by_line[1:]:
                    additional_line_counter += 1
                    next_line_in_list = self.content_as_lines[i + additional_line_counter].split('.')[0]
                    if additional_line.strip() != next_line_in_list:
                        break
                else:
                    return i

        raise Exception(f"Could not find the line where '{clean_sentence_split_by_line[0]}' occurs. "
                        f"The given sentence index was {sentence_location_integer}")

    def get_lexipol_section(self, sentence_location_integer):
        """
        Returns the title of the section for a sentence for lexipol documents.
        :param sentence_location_integer: integer
        :return: string
        """
        # Find the sentence in the content_as_lines list
        line_location = self.get_line_location_from_sentence_location(sentence_location_integer)

        # Reverse the content_as_lines list up to the line_location.
        reversed_lines_list = self.content_as_lines[:line_location + 1].copy()
        reversed_lines_list.reverse()

        # Extract the title once you find the first instance of '300'
        for i, line in enumerate(reversed_lines_list):
            if '300' in line:
                return line

    def perform_search(self, phrases_to_search, positive_indicator_phrases):
        """
        This will search each sentence for specific phrases. Then it will use a list of additional phrases to determine
        a positive indicator. It will also return the phrase found with the regex. If the positive indicator was not
        set, then all of the found phrases will be returned in the second part of the tuple
        :param phrases_to_search: list of strings
        :param positive_indicator_phrases: list of strings
        :return: Tuple (boolean, string)
        """

        # Convert none types to empty lists
        if phrases_to_search is None:
            phrases_to_search = []
        if positive_indicator_phrases is None:
            positive_indicator_phrases = []

        # Translate inputs to their regex phrases
        regex_phrases_to_search = [convert_input_to_regex(phrase) for phrase in phrases_to_search]
        regex_positive_indicator_phrases = [convert_input_to_regex(phrase) for phrase in positive_indicator_phrases]

        # Perform search
        language_found = ''
        for sentence_index, sentence in enumerate(self.content_as_sentences):

            # Search for desired terms and check where they are mentioned in the document
            for phrase_to_search_index, regex_phrase_to_search in enumerate(regex_phrases_to_search):
                if re.findall(regex_phrase_to_search, sentence.lower()):
                    # Report the phrase that has been found
                    phrase_found = phrases_to_search[phrase_to_search_index]
                    print(f"Found '{phrase_found}' at index {sentence_index} within content_as_sentences")

                    # Append each sentence found
                    language_found += f'{sentence}\n\n'

                    # Check all regex phrases for a positive indicator
                    for regex_positive_indicator_phrase in regex_positive_indicator_phrases:
                        if re.findall(regex_positive_indicator_phrase, sentence.lower()):
                            # Find the section for additional context.
                            section = self.get_lexipol_section(sentence_index) if self.lexipol else ''
                            print(f'This sentence was found under the section {section}\n')
                            return True, f'{section}\n\n{sentence}'

                    # Check if the phrase that was found is part of a list. If so, check previous sentences for context
                    if is_enumerated_list(sentence):
                        for previous_sentence in self.content_as_sentences[sentence_index-2:sentence_index]:
                            for regex_positive_indicator_phrase in regex_positive_indicator_phrases:
                                if re.findall(regex_positive_indicator_phrase, previous_sentence.lower()):
                                    # Find the section for additional context.
                                    section = self.get_lexipol_section(sentence_index) if self.lexipol else ''
                                    print(f'This sentence was found under the section {section}\n')
                                    return True, f'{section}\n\n{previous_sentence}\n{sentence}'

        return False, language_found
