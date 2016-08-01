from random import random
import time
import os


#
# Popular comparison-based sorting algorithms.
#
# -----------------------------------------------------------------------------------------------------------------
# |  Name            |  Time Complexity  |  Memory Complexity  |  Stable  |  Notes                                |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Bubble Sort     |  O(n ** 2)        |  O(1)               |  Yes     |  Simple to understand and implement.  |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Selection Sort  |  O(n ** 2)        |  O(1)               |  No      |  Few memory writes.                   |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Insertion Sort  |  O(n ** 2)        |  O(1)               |  Yes     |  Fast when n is small.                |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Heapsort        |  O(n log n)       |  O(1)               |  No      |  Low memory cost.                     |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Quicksort       |  O(n log n)       |  O(log n)           |  No      |  Fastest O(n log n) sort in general.  |
# |------------------+-------------------+---------------------+----------+---------------------------------------|
# |  Merge Sort      |  O(n log n)       |  O(n)               |  Yes     |  Stable O(n log n) sort.              |
# -----------------------------------------------------------------------------------------------------------------
#

def bubble_sort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Bubble sort.
    """
    for i in range(len(datas) - 1, 0, -1):
        for j in range(i):
            if compare(datas[j], datas[j + 1]) > 0:
                datas[j], datas[j + 1] = datas[j + 1], datas[j]


def selection_sort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Selection sort.
    """
    for i in range(len(datas) - 1):
        min = i
        for j in range(i + 1, len(datas)):
            if compare(datas[min], datas[j]) > 0:
                min = j
        if min != i:
            datas[min], datas[i] = datas[i], datas[min]


def insertion_sort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Insertion sort.
    """
    for i in range(1, len(datas)):
        for j in range(i, 0, -1):
            if compare(datas[j - 1], datas[j]) > 0:
                datas[j - 1], datas[j] = datas[j], datas[j - 1]
            else:
                break


def heapsort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Heapsort.
    """
    # Repair the max heap.
    # Given a parent node with index i, its child nodes' indices are i * 2 + 1 and i * 2 + 2
    def sift_down(datas, parent, max, compare):
        while True:
            child = parent * 2 + 1
            if child >= max:
                return
            if child + 1 < max and compare(datas[child], datas[child + 1]) < 0:
                child += 1
            if compare(datas[parent], datas[child]) > 0:
                return
            datas[parent], datas[child], parent = datas[child], datas[parent], child

    # 1. Heapify the array.
    # Given a child node with index i, its parent node's index is (i - 1) // 2
    length = len(datas)
    for i in range(length // 2 - 1, -1, -1):
        sift_down(datas, i, length, compare)
    # 2. Swap elements and repair the heap repeatedly.
    for i in range(length - 1, 0, -1):
        datas[0], datas[i] = datas[i], datas[0]
        sift_down(datas, 0, i, compare)


def quicksort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Non-recursive quicksort.
    """
    if len(datas) <= 1:
        return
    stack = list()
    stack.append((0, len(datas) - 1))
    while len(stack) > 0:
        # 1. Choose a pivot.
        left, right = stack.pop()
        pivot = left + int(random() * (right - left + 1))
        # 2. Swap elements to make all elements in the left part are no greater than
        # the pivot, while all elements in the right part are no less than the pivot.
        i, j, data = left, right, datas[pivot]
        while i < j:
            while j > pivot and compare(datas[j], data) >= 0:
                j -= 1
            if j > pivot:
                datas[pivot], pivot = datas[j], j
            while i < pivot and compare(datas[i], data) <= 0:
                i += 1
            if i < pivot:
                datas[pivot], pivot = datas[i], i
        datas[pivot] = data
        # 3. Deal with the left part and the right part separately.
        if pivot - 1 > left:
            stack.append((left, pivot - 1))
        if pivot + 1 < right:
            stack.append((pivot + 1, right))


def merge_sort(datas, compare=lambda x1, x2: 0 if x1 == x2 else (-1 if x1 < x2 else 1)):
    """Bottom-up merge sort.
    """
    # Length of merged subarrays after round n is 2 ** n.
    def width_generator(length):
        width = 1
        while width < length:
            yield width
            width *= 2

    # 1. Subarrays of length 1 are already sorted.
    temp1, temp2, length = datas, datas[:], len(datas)
    # 2. Repeatedly merge subarrays untill number of the merged subarrays is 1.
    for width in width_generator(length):
        # 2.1 Do merge subarrays.
        for i in range(0, length, width * 2):
            left, pivot, right = i, min(i + width, length), min(i + width * 2, length)
            j, k = left, pivot
            for pos in range(left, right):
                if (k >= right) or (j < pivot and compare(temp1[j], temp1[k]) <= 0):
                    temp2[pos], j = temp1[j], j + 1
                else:
                    temp2[pos], k = temp1[k], k + 1
        # 2.2 Swap variables instead of simply copy data back.
        temp1, temp2 = temp2, temp1
    # 3. Copy data back.
    for i in range(length):
        datas[i] = temp1[i]


#
# External sorting algorithm.
#

def external_merge_sort(source, temp=None, target=None,
                        compare=lambda x1, x2: 0 if (x1 == x2) else (-1 if x1 < x2 else 1),
                        stable=False, log=print, max_load=10000000, k_way_merge=1):
    """External merge sort.
    """
    # Calculate temp file name with the specified index.
    def temp_file_name(index):
        return '{0}{1}'.format(temp, index)

    # Helper class for loading data from the specified temp file.
    class TempData:
        def __init__(self, max_load):
            self.capacity = max_load + 1
            self.cache = [None for _ in range(self.capacity)]
            self.file, self.next_index, self.last_index = None, 0, 0

        def reinitialize(self, file):
            self.file, self.next_index, self.last_index = file, 0, 0
            return self

        def load(self):
            if self.next_index <= self.last_index:
                # 0 <= self.next_index <= self.last_index < self.capacity
                if self.__do_load(range(self.last_index, self.capacity if self.next_index > 0 else self.capacity - 1)):
                    return
                if self.__do_load(range(0, self.next_index - 1)):
                    return
                self.last_index = self.next_index - 1 if self.next_index > 0 else self.capacity - 1
            else:
                # 0 <= self.last_index < self.next_index < self.capacity
                if self.__do_load(range(self.last_index, self.next_index - 1)):
                    return
                self.last_index = self.next_index - 1

        def __do_load(self, range):
            for i in range:
                line = self.file.readline()
                if len(line) == 0:
                    self.last_index = i
                    return True
                self.cache[i] = line
            return False

        def no_more_in_cache(self):
            return self.next_index == self.last_index

        def next(self):
            return self.cache[self.next_index]

        def pop(self):
            next_element = self.cache[self.next_index]
            self.next_index = self.next_index + 1 if self.next_index < self.capacity - 1 else 0
            return next_element

    # Repair the min heap.
    def sift_down(temp_datas, parent, max, compare):
        while True:
            child = parent * 2 + 1
            if child >= max:
                return
            if child + 1 < max and compare(temp_datas[child].next(), temp_datas[child + 1].next()) > 0:
                child += 1
            if compare(temp_datas[parent].next(), temp_datas[child].next()) <= 0:
                return
            temp_datas[parent], temp_datas[child], parent = temp_datas[child], temp_datas[parent], child

    # 1. Preparation.
    elapsed_time = time.time()
    if temp is None:
        temp = '{0}.temp.'.format(source)
    else:
        temp = '{0}{1}temp.'.format(temp, '' if temp.endswith(os.sep) else os.sep)
    if target is None:
        target = '{0}.sorted'.format(source)
    # 2. Split source file into sorted temp files, each temp file contains up to (max_load) lines.
    temp_files_count, done = 0, False
    with open(source, 'r') as source_file:
        source_datas, source_datas_count = [None for _ in range(max_load)], 0
        while not done:
            # 2.1 Load up to (max_load) lines from source file.
            source_datas_count = max_load
            for i in range(max_load):
                line = source_file.readline()
                if len(line) == 0:
                    source_datas_count, done = i, True
                    break
                source_datas[i] = line
            # 2.2 Perform an in-memory sort and write the sorted result to a temp file.
            if source_datas_count > 0:
                if source_datas_count < max_load:
                    source_datas = source_datas[:source_datas_count]
                if not stable:
                    quicksort(source_datas, compare=compare)
                else:
                    merge_sort(source_datas, compare=compare)
                with open(temp_file_name(temp_files_count), 'w') as temp_file:
                    for i in range(source_datas_count):
                        temp_file.write(source_datas[i])
                    temp_file.flush()
                    temp_files_count += 1
                    log('+ {0}'.format(temp_file.name))
        source_datas = None
    # 3. Merge the temp files.
    # Perform k way merge to the temp files where k is (k_way_merge). If k is no greater than 1 or if it is greater
    # than temp files count, change its value to temp files count. If k is no less than (max_load), change its value
    # to (max_load) - 1.
    if k_way_merge <= 1 or k_way_merge > temp_files_count:
        k_way_merge = temp_files_count
    if k_way_merge >= max_load:
        k_way_merge = max_load - 1
    max_load //= k_way_merge + 1
    temp_file_index_max = temp_files_count
    temp_file_index = 0
    all_temp_datas = [TempData(max_load) for _ in range(k_way_merge)]
    merged_datas = [None for _ in range(max_load)]
    done = False
    while not done:
        temp_files, merged_file = list(), None
        try:
            # 3.1 Determine which temp files will be merged and the merged file as the result for this round.
            while temp_file_index < temp_file_index_max and len(temp_files) < k_way_merge:
                temp_files.append(open(temp_file_name(temp_file_index), 'r'))
                temp_file_index += 1
            if temp_file_index < temp_files_count:
                merged_file, temp_files_count = open(temp_file_name(temp_files_count), 'w'), temp_files_count + 1
                if temp_file_index == temp_file_index_max:
                    temp_file_index_max = temp_files_count
            else:
                merged_file, done = open(target, 'w'), True
            # 3.2 If there is only one file to merge, rename the file will do the merge.
            if len(temp_files) == 1:
                try:
                    merged_file.close()
                except:
                    pass
                try:
                    temp_files[0].close()
                except:
                    pass
                os.renames(temp_files[0].name, merged_file.name)
                log('+ {0}'.format(merged_file.name))
                continue
            # 3.3 Do merge the temp files.
            temp_datas = [all_temp_datas[i].reinitialize(temp_file) for i, temp_file in enumerate(temp_files)]
            while True:
                # 3.3.1 If there is still no more data in cache after a load, then the temp file is done.
                for i in range(len(temp_datas) - 1, -1, -1):
                    temp_datas[i].load()
                    if temp_datas[i].no_more_in_cache():
                        del temp_datas[i]
                # 3.3.2 When all temp files are done, the merge is done.
                if len(temp_datas) == 0:
                    break
                # 3.3.3 Do a k-way merge.
                merged_count = max_load
                if not stable:
                    for i in range(len(temp_datas) // 2 - 1, -1, -1):
                        sift_down(temp_datas, i, len(temp_datas), compare)
                for i in range(max_load):
                    temp_index = 0
                    if not stable:
                        sift_down(temp_datas, 0, len(temp_datas), compare)
                    else:
                        for j in range(1, len(temp_datas)):
                            if compare(temp_datas[temp_index].next(), temp_datas[j].next()) > 0:
                                temp_index = j
                    merged_datas[i] = temp_datas[temp_index].pop()
                    if temp_datas[temp_index].no_more_in_cache():
                        merged_count = i + 1
                        break
                # 3.3.4 Write merged datas to the merged file.
                for i in range(merged_count):
                    merged_file.write(merged_datas[i])
                merged_file.flush()
            log('+ {0}'.format(merged_file.name))
        finally:
            try:
                if not merged_file.closed:
                    merged_file.close()
            except:
                pass
            finally:
                for temp_file in temp_files:
                    try:
                        if not temp_file.closed:
                            temp_file.close()
                        os.remove(temp_file.name)
                        log('    - {0}'.format(temp_file.name))
                    except:
                        pass
    # 4. Done.
    elapsed_time = time.time() - elapsed_time
    log('Done in {0} seconds.'.format(int(elapsed_time)))
