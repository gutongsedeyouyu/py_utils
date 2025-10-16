import re


#
# Keywords Checker
#

class KeywordsChecker:
    """Prefix trie based keywords checker.
    """

    END_OF_KEYWORD = object()

    def __init__(self, keywords, punctuations_to_trim=' \t\r\n`~!@#$%^&*()-_=+[{]}\\|;:\'",<.>/?｀～！＃¥％…＊（）－—＝＋［｛］｝、｜；：‘’“”，《。》／？'):
        """Initialize with keywords.
        """
        self.keywords_trie = dict()
        for keyword in keywords:
            current_node = self.keywords_trie
            for char in keyword:
                if char not in current_node:
                    new_node = dict()
                    new_node[KeywordsChecker.END_OF_KEYWORD] = False
                    current_node[char] = new_node
                    current_node = new_node
                else:
                    current_node = current_node[char]
            current_node[KeywordsChecker.END_OF_KEYWORD] = True
        if punctuations_to_trim:
            self.trim_pattern = re.compile('[{0}]'.format(''.join([re.escape(c) for c in punctuations_to_trim])))
        else:
            self.trim_pattern = None

    def contains_keywords(self, string):
        """Return True if the string contains any of the keywords, False otherwise.
        """
        if self.trim_pattern:
            string = self.trim_pattern.sub('', string)
        for position in range(len(string)):
            if self.__calculate_matching_length(string, position, True) > 0:
                return True
        return False

    def get_contained_keywords(self, string, maximum_match=False):
        """Return all contained keywords of the string.
        """
        if self.trim_pattern:
            string = self.trim_pattern.sub('', string)
        contained_keywords, length, position = list(), len(string), 0
        while position < length:
            matching_length = self.__calculate_matching_length(string, position, maximum_match)
            if matching_length == 0:
                position += 1
            else:
                contained_keywords.append(string[position: position + matching_length])
                position += matching_length
        return contained_keywords

    def __calculate_matching_length(self, string, begin, maximum_match):
        """Check if a substring from the begin position matches any of the keywords and return the matching length.
        """
        current_node, matching_length = self.keywords_trie, 0
        for position in range(begin, len(string)):
            char = string[position]
            if char not in current_node:
                break
            current_node = current_node[char]
            if current_node[KeywordsChecker.END_OF_KEYWORD]:
                matching_length = position - begin + 1
                if not maximum_match:
                    break
        return matching_length


#
# Edit distance.
#

def edit_distance(s1, s2):
    """Return edit distance (Levenshtein distance) between s1 and s2.
    """
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return max(len1, len2)
    # Space complexity is O(min(len(s1), len(s2)))
    if len1 < len2:
        s1, s2, len1, len2 = s2, s1, len2, len1
    d0, d1 = [x for x in range(len2 + 1)], [0 for _ in range(len2 + 1)]
    # Time complexity is O(len(s1) * len(s2))
    for i in range(len1):
        d1[0] = i + 1
        for j in range(len2):
            if s1[i] == s2[j]:
                d1[j + 1] = d0[j]
            else:
                d1[j + 1] = min(d0[j] + 1, d0[j + 1] + 1, d1[j] + 1)
        d0, d1 = d1, d0
    return d0[len2]
