import unittest
import utils.sorting
from random import random


class Element:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return 'Element({0}, {1})'.format(self.value, self.priority)


class SortingUtilsTest(unittest.TestCase):
    def do_test_none(self, sort):
        with self.assertRaises(TypeError):
            sort(None)

    def test_none(self):
        """Test sort behavior with None argument.
        """
        self.do_test_none(utils.sorting.bubble_sort)
        self.do_test_none(utils.sorting.selection_sort)
        self.do_test_none(utils.sorting.insertion_sort)
        self.do_test_none(utils.sorting.heapsort)
        self.do_test_none(utils.sorting.quicksort)
        self.do_test_none(utils.sorting.merge_sort)

    def do_test_length_n(self, n, sort):
        datas, expected = list(range(n)), list(range(n))
        for i in range(int(random() * (n * 2 + 1))):
            j, k = int(random() * n), int(random() * n)
            datas[j], datas[k] = datas[k], datas[j]
        sort(datas)
        self.assertEqual(datas, expected)

    def test_length_0_to_127(self):
        """Test sort behavior with 0-127 length array.
        """
        for i in range(128):
            self.do_test_length_n(i, utils.sorting.bubble_sort)
            self.do_test_length_n(i, utils.sorting.selection_sort)
            self.do_test_length_n(i, utils.sorting.insertion_sort)
            self.do_test_length_n(i, utils.sorting.heapsort)
            self.do_test_length_n(i, utils.sorting.quicksort)
            self.do_test_length_n(i, utils.sorting.merge_sort)

    def do_test_stable(self, sort):
        length = 128
        datas = [Element(int(random() * length), i) for i in range(length)]
        sort(datas)
        for i in range(length - 1):
            e1, e2 = datas[i], datas[i + 1]
            self.assertTrue((e1.value < e2.value) or (e1.value == e2.value and e1.priority < e2.priority))

    def test_stable(self):
        """Bubble sort, insertion sort and merge sort are stable.
        """
        for i in range(1):
            self.do_test_stable(utils.sorting.bubble_sort)
            self.do_test_stable(utils.sorting.insertion_sort)
            self.do_test_stable(utils.sorting.merge_sort)

    def do_test_external_merge_sort(self, data_size, max_load, k_way_merge, stable):
        source = 'test_external_merge_sort_{0}_{1}.source'.format(data_size, 'stable' if stable else 'nonstable')
        target = 'test_external_merge_sort_{0}_{1}.sorted'.format(data_size, 'stable' if stable else 'nonstable')
        sep = ', '
        compare, log = lambda x1, x2: int(x1.split(sep)[0]) - int(x2.split(sep)[0]), lambda m: None
        with open(source, 'w') as source_file:
            for i in range(data_size):
                source_file.write('{0}{1}{2}\n'.format(int(random() * data_size), sep, i))
        utils.sorting.external_merge_sort(source, target=target, compare=compare,
                                          stable=stable, log=log,
                                          max_load=max_load, k_way_merge=k_way_merge)
        with open(target, 'r') as target_file:
            previous_line = None
            for i in range(data_size):
                current_line = target_file.readline()
                self.assertTrue(len(current_line) > 0)
                if previous_line is None:
                    previous_line = current_line
                    continue
                previous_value, previous_priority = int(previous_line.split(sep)[0]), int(previous_line.split(sep)[1])
                current_value, current_priority = int(current_line.split(sep)[0]), int(current_line.split(sep)[1])
                if stable:
                    self.assertTrue((previous_value < current_value) or
                                    (previous_value == current_value and previous_priority < current_priority))
                else:
                    self.assertTrue(previous_value <= current_value)
                previous_line = current_line
            self.assertTrue(len(target_file.readline()) == 0)
        import os
        os.remove(source)
        os.remove(target)

    def test_external_merge_sort(self):
        """Test external merge sort.
        -------------------------------------------------------
        |  Factor       |  Possible Values  |  Default Value  |
        |---------------+-------------------+-----------------|
        |  data_size    |  0 ~ 2000         |  1000           |
        |  max_load     |  10 ~ 1000        |  100            |
        |  k_way_merge  |  1 ~ 30           |  1              |
        -------------------------------------------------------
        """
        def data_size(default=True):
            return 1000 if default else int(random() * (2000 + 1))

        def max_load(default=True):
            return 100 if default else 10 + int(random() * (1000 - 10 + 1))

        def k_way_merge(default=True):
            return 1 if default else 1 + int(random() * 30)

        #
        # Test external merge sort with empty source.
        #
        self.do_test_external_merge_sort(0, max_load(True), k_way_merge(True), stable=False)
        self.do_test_external_merge_sort(0, max_load(True), k_way_merge(True), stable=True)
        #
        # Test external merge sort with default factor values.
        #
        self.do_test_external_merge_sort(data_size(True), max_load(True), k_way_merge(True), stable=False)
        self.do_test_external_merge_sort(data_size(True), max_load(True), k_way_merge(True), stable=True)
        #
        # Test external merge sort with 9-way-merge and 10 temp files.
        #
        self.do_test_external_merge_sort(100, 10, 9, stable=False)
        self.do_test_external_merge_sort(100, 10, 9, stable=True)
        #
        # Test external merge sort with k_way_merge >= max_load.
        #
        self.do_test_external_merge_sort(100, 10, 10, stable=False)
        self.do_test_external_merge_sort(100, 10, 10, stable=True)
        #
        # Test external merge sort with random factor values.
        #
        for i in range(1):
            self.do_test_external_merge_sort(data_size(False), max_load(False), k_way_merge(False), stable=False)
            self.do_test_external_merge_sort(data_size(False), max_load(False), k_way_merge(False), stable=True)
