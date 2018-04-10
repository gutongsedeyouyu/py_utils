import unittest
import utils.text


class KeywordsCheckerTest(unittest.TestCase):
    def setUp(self):
        keywords = ['暴力', '违法网站', '敏感', '敏感词']
        self.keywordsChecker = utils.text.KeywordsChecker(keywords)

    #
    # Test KeywordsChecker.contains_keywords
    #
    def test_key_words_checker_contains_keywords_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker.contains_keywords(None)

    def test_key_words_checker_contains_keywords_empty(self):
        self.assertFalse(self.keywordsChecker.contains_keywords(''))

    def test_key_words_checker_contains_keywords(self):
        self.assertFalse(self.keywordsChecker.contains_keywords('孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也。'))
        self.assertTrue(self.keywordsChecker.contains_keywords('暴力是不能解决问题的'))
        self.assertFalse(self.keywordsChecker.contains_keywords('暴%力`是$不能解决问题的'))
        self.assertTrue(self.keywordsChecker.contains_keywords('警方查封了一个违法网站'))
        self.assertFalse(self.keywordsChecker.contains_keywords('警方查封了一#个*违-法+网=站'))

    #
    # Test KeywordsChecker.contains_keywords with trim_punctuation=True
    #
    def test_key_words_checker_contains_keywords_trim_punctuation_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker.contains_keywords(None, trim_punctuation=True)

    def test_key_words_checker_contains_keywords_trim_punctuation_empty(self):
        self.assertFalse(self.keywordsChecker.contains_keywords('', trim_punctuation=True))

    def test_key_words_checker_contains_keywords_trim_punctuation(self):
        self.assertFalse(self.keywordsChecker.contains_keywords('孙子曰：兵者，国之大事，死生之地，存亡之道，不可不察也。', trim_punctuation=True))
        self.assertTrue(self.keywordsChecker.contains_keywords('暴力是不能解决问题的', trim_punctuation=True))
        self.assertTrue(self.keywordsChecker.contains_keywords('暴%力`是$不能解决问题的', trim_punctuation=True))
        self.assertTrue(self.keywordsChecker.contains_keywords('警方查封了一个违法网站', trim_punctuation=True))
        self.assertTrue(self.keywordsChecker.contains_keywords('警方查封了一#个*违-法+网=站', trim_punctuation=True))

    #
    # Test KeywordsChecker.get_contained_keywords
    #
    def test_key_words_checker_get_contained_keywords_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker.get_contained_keywords(None, trim_punctuation=True)

    def test_key_words_checker_get_contained_keywords_empty(self):
        contained_keywords = self.keywordsChecker.get_contained_keywords('')
        self.assertEqual(len(contained_keywords), 0)

    def test_key_words_checker_get_contained_keywords(self):
        contained_keywords = self.keywordsChecker.get_contained_keywords('如何根据敏感词过滤违法网站？')
        self.assertTrue('敏感' in contained_keywords)
        self.assertTrue('违法网站' in contained_keywords)
        self.assertEqual(len(contained_keywords), 2)

    #
    # Test KeywordsChecker.get_contained_keywords with maximum_match=True
    #
    def test_key_words_checker_get_contained_keywords_maximum_match_none(self):
        with self.assertRaises(TypeError):
            self.keywordsChecker.get_contained_keywords(None, maximum_match=True)

    def test_key_words_checker_get_contained_keywords_maximum_match_empty(self):
        contained_keywords = self.keywordsChecker.get_contained_keywords('', maximum_match=True)
        self.assertEqual(len(contained_keywords), 0)

    def test_key_words_checker_get_contained_keywords_maximum_match(self):
        contained_keywords = self.keywordsChecker.get_contained_keywords('如何根据敏感词过滤违法网站？', maximum_match=True)
        self.assertTrue('敏感词' in contained_keywords)
        self.assertTrue('违法网站' in contained_keywords)
        self.assertEqual(len(contained_keywords), 2)


class ChineseToPinyinTest(unittest.TestCase):
    def test_gb2312_to_pinyin_none(self):
        with self.assertRaises(TypeError):
            utils.text.gb2312_to_pinyin(None)

    def test_gb2312_to_pinyin_empty(self):
        self.assertEqual(utils.text.gb2312_to_pinyin(''), '')

    def test_gb2312_to_pinyin_non_gb2312(self):
        self.assertEqual(utils.text.gb2312_to_pinyin('周鸿祎'), 'ZhouHong*')

    def test_gb2312_to_pinyin(self):
        self.assertEqual(utils.text.gb2312_to_pinyin('Python是一种面向对象、解释型计算机程序设计语言。'),
                         'PythonShiYiZhongMianXiangDuiXiangJieShiXingJiSuanJiChengXuSheJiYuYan')
        self.assertEqual(utils.text.gb2312_to_pinyin('天下武功出少林', acronym=True), 'TXWGCSL')


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


class SimplifiedTraditionalConverterTest(unittest.TestCase):
    def test_simplified_to_traditional(self):
        converter = utils.text.SimplifiedTraditionalConverter()
        self.assertEqual(converter.convert('梅长苏，琅琊榜首，天下第一大帮江左盟宗主。'), '梅長蘇，琅琊榜首，天下第壹大幫江左盟宗主。')
        self.assertEqual(converter.convert('乐高公司创办于丹麦，至今已有85年的发展历史，追本溯源，还得从它的金字招牌LEGO说起。'), '樂高公司創辦於丹麥，至今已有85年的發展曆史，追本溯源，還得從它的金字招牌LEGO說起。')

    def test_traditional_to_simplified(self):
        converter = utils.text.SimplifiedTraditionalConverter()
        converter.simplified_to_traditional = False
        self.assertEqual(converter.convert('這次，請和我壹起學習壹個簡單的漢語句子。'), '这次，请和我一起学习一个简单的汉语句子。')
        self.assertEqual(converter.convert('《變形金剛 第壹代》是歐美類型動漫,于2016-12-29上映。愛奇藝在線觀看《變形金剛 第壹代》全集高清視頻'), '《变形金刚 第一代》是欧美类型动漫,于2016-12-29上映。爱奇艺在线观看《变形金刚 第一代》全集高清视频')
