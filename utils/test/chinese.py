import unittest
import utils.chinese


class ChineseToPinyinTest(unittest.TestCase):
    def test_gb2312_to_pinyin_none(self):
        with self.assertRaises(TypeError):
            utils.chinese.gb2312_to_pinyin(None)

    def test_gb2312_to_pinyin_empty(self):
        self.assertEqual(utils.chinese.gb2312_to_pinyin(''), '')

    def test_gb2312_to_pinyin_non_gb2312(self):
        self.assertEqual(utils.chinese.gb2312_to_pinyin('周鸿祎'), 'ZhouHong*')

    def test_gb2312_to_pinyin(self):
        self.assertEqual(utils.chinese.gb2312_to_pinyin('Python是一种面向对象、解释型计算机程序设计语言。'),
                         'PythonShiYiZhongMianXiangDuiXiangJieShiXingJiSuanJiChengXuSheJiYuYan')
        self.assertEqual(utils.chinese.gb2312_to_pinyin('天下武功出少林', acronym=True), 'TXWGCSL')


class SimplifiedTraditionalConverterTest(unittest.TestCase):
    def test_simplified_to_traditional(self):
        converter = utils.chinese.SimplifiedTraditionalConverter()
        self.assertEqual(converter.convert('梅长苏，琅琊榜首，天下第一大帮江左盟宗主。'), '梅長蘇，琅琊榜首，天下第壹大幫江左盟宗主。')
        self.assertEqual(converter.convert('乐高公司创办于丹麦，至今已有85年的发展历史，追本溯源，还得从它的金字招牌LEGO说起。'), '樂高公司創辦於丹麥，至今已有85年的發展曆史，追本溯源，還得從它的金字招牌LEGO說起。')

    def test_traditional_to_simplified(self):
        converter = utils.chinese.SimplifiedTraditionalConverter()
        converter.simplified_to_traditional = False
        self.assertEqual(converter.convert('這次，請和我壹起學習壹個簡單的漢語句子。'), '这次，请和我一起学习一个简单的汉语句子。')
        self.assertEqual(converter.convert('《變形金剛 第壹代》是歐美類型動漫,于2016-12-29上映。愛奇藝在線觀看《變形金剛 第壹代》全集高清視頻'), '《变形金刚 第一代》是欧美类型动漫,于2016-12-29上映。爱奇艺在线观看《变形金刚 第一代》全集高清视频')


class PrcIdChecksumTest(unittest.TestCase):
    def test_prc_id_checksum(self):
        self.assertEqual(utils.chinese.prc_id_checksum('34052419800101001'), 'X')
