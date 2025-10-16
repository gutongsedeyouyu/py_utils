import unittest
import utils.text


class KeywordsCheckerTest(unittest.TestCase):
    def setUp(self):
        keywords = ['暴力', '违法网站', '敏感', '敏感词']
        self.keywordsChecker1 = utils.text.KeywordsChecker(keywords)
        self.keywordsChecker2 = utils.text.KeywordsChecker(keywords, punctuations_to_trim='')

    #
    # Test KeywordsChecker.contains_keywords NO punctuations_to_trim
    #
    def test_key_words_checker_contains_keywords_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker2.contains_keywords(None)

    def test_key_words_checker_contains_keywords_empty(self):
        self.assertFalse(self.keywordsChecker2.contains_keywords(''))

    def test_key_words_checker_contains_keywords(self):
        self.assertFalse(self.keywordsChecker2.contains_keywords('孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也。'))
        self.assertTrue(self.keywordsChecker2.contains_keywords('暴力是不能解决问题的'))
        self.assertFalse(self.keywordsChecker2.contains_keywords('暴%力`是$不能解决问题的'))
        self.assertTrue(self.keywordsChecker2.contains_keywords('警方查封了一个违法网站'))
        self.assertFalse(self.keywordsChecker2.contains_keywords('警方查封了一#个*违-法+网=站'))

    #
    # Test KeywordsChecker.contains_keywords with DEFAULT punctuations_to_trim
    #
    def test_key_words_checker_contains_keywords_trim_punctuation_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker1.contains_keywords(None)

    def test_key_words_checker_contains_keywords_trim_punctuation_empty(self):
        self.assertFalse(self.keywordsChecker1.contains_keywords(''))

    def test_key_words_checker_contains_keywords_trim_punctuation(self):
        self.assertFalse(self.keywordsChecker1.contains_keywords('孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也。'))
        self.assertTrue(self.keywordsChecker1.contains_keywords('暴力是不能解决问题的'))
        self.assertTrue(self.keywordsChecker1.contains_keywords('暴%力`是$不能解决问题的'))
        self.assertTrue(self.keywordsChecker1.contains_keywords('警方查封了一个违法网站'))
        self.assertTrue(self.keywordsChecker1.contains_keywords('警方查封了一#个*违-法+网=站'))

    #
    # Test KeywordsChecker.get_contained_keywords
    #
    def test_key_words_checker_get_contained_keywords_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker1.get_contained_keywords(None)

    def test_key_words_checker_get_contained_keywords_empty(self):
        contained_keywords = self.keywordsChecker1.get_contained_keywords('')
        self.assertEqual(len(contained_keywords), 0)

    def test_key_words_checker_get_contained_keywords(self):
        contained_keywords = self.keywordsChecker1.get_contained_keywords('如何根据敏感词过滤违法网站？')
        self.assertTrue('敏感' in contained_keywords)
        self.assertTrue('违法网站' in contained_keywords)
        self.assertEqual(len(contained_keywords), 2)

    #
    # Test KeywordsChecker.get_contained_keywords with maximum_match=True
    #
    def test_key_words_checker_get_contained_keywords_maximum_match_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker1.get_contained_keywords(None, maximum_match=True)

    def test_key_words_checker_get_contained_keywords_maximum_match_empty(self):
        contained_keywords = self.keywordsChecker1.get_contained_keywords('', maximum_match=True)
        self.assertEqual(len(contained_keywords), 0)

    def test_key_words_checker_get_contained_keywords_maximum_match(self):
        contained_keywords = self.keywordsChecker1.get_contained_keywords('如何根据敏感词过滤违法网站？', maximum_match=True)
        self.assertTrue('敏感词' in contained_keywords)
        self.assertTrue('违法网站' in contained_keywords)
        self.assertEqual(len(contained_keywords), 2)


class EditDistanceTest(unittest.TestCase):
    def test_edit_distance_none(self):
        with self.assertRaises(TypeError):
            utils.text.edit_distance(None, None)
        with self.assertRaises(TypeError):
            utils.text.edit_distance(None, '')
        with self.assertRaises(TypeError):
            utils.text.edit_distance('', None)

    def test_edit_distance_empty(self):
        self.assertEqual(utils.text.edit_distance('', ''), 0)
        self.assertEqual(utils.text.edit_distance('a', ''), 1)
        self.assertEqual(utils.text.edit_distance('', 'abc'), 3)

    def test_edit_distance(self):
        self.assertEqual(utils.text.edit_distance('hello', 'hello'), 0)
        self.assertEqual(utils.text.edit_distance('hello', 'world'), 4)
        self.assertEqual(utils.text.edit_distance('hello', 'happy'), 4)
        self.assertEqual(utils.text.edit_distance('happy', 'birthday'), 7)
        self.assertEqual(utils.text.edit_distance('new year', 'happy'), 7)
        self.assertEqual(utils.text.edit_distance('hello', '你好'), 5)
        self.assertEqual(utils.text.edit_distance('XX有限责任公司', 'XX有限公司'), 2)
