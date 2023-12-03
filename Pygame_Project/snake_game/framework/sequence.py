from typing import List
import time


def iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


class Sequence:
    """함수 절차 리스트 클래스"""

    def __init__(self, *func):
        self.func_list = list(func)
        self.arg_list = [[] for i in self.func_list]
        self.delay = 0  # type: int

    def __add__(self, other):
        if callable(other):
            func_list = self.func_list + [other]
            return Sequence(*func_list)

        elif iterable(other) and all([callable(func) for func in other]):
            func_list = self.func_list + list(other)
            return Sequence(*func_list)

        elif iterable(other) and (callable(other[0]) and iterable(other[1])):
            func_list = self.func_list + [other[0]]
            new = Sequence(*func_list)
            new.set_arg(-1, *other[1])
            return new

        else:
            return

    def __iter__(self):
        return (func for func in self.func_list)

    def __len__(self):
        return len(self.func_list)

    def set_delay(self, delay: int):
        """지연 시간을 설정한다. 단위는 ms"""
        self.delay = delay

    def set_arg(self, index, *arg):
        """특정 함수에 인자를 설정한다."""
        self.arg_list[index] = arg

    def shift(self, index: int, new_index: int):
        """특정 함수의 순서를 변경한다."""
        func = self.func_list.pop(index)
        arg = self.arg_list.pop(index - 1)

        if new_index < 0:
            new_index += len(self) + 1
        self.func_list.insert(new_index, func)
        self.arg_list.insert(new_index, arg)

    def exchange(self, index1: int, index2: int):
        """두 함수의 순서를 교체한다."""
        func_save = self.func_list[index1]
        arg_save = self.arg_list[index1]

        self.func_list[index1] = self.func_list[index2]
        self.func_list[index2] = func_save

        self.arg_list[index1] = self.arg_list[index2]
        self.arg_list[index2] = arg_save

    def call(self, flag: bool = True, *except_list):
        """함수를 절차적으로 실행한다. 인덱스를 넣으면 해당 순서의 함수 실행은 스킵한다."""
        for idx, func in enumerate(self.func_list):
            if not flag:
                return

            if idx in except_list:
                continue

            func(*self.arg_list[idx])
            time.sleep(self.delay / 1000.0)
