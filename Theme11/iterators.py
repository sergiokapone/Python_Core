class MyIterator:
    """Итератор в Python — это объект, который реализует метод __next__(), возвращающий следующий элемент итерируемого объекта при каждом вызове, и бросающий исключение StopIteration, когда элементы закончились.

    Итератор получают с помощью функции iter().

    """

    def __init__(self, data):
        self.data = data
        self.index = 0

    def __next__(self):
        if self.index == len(self.data):
            raise StopIteration
        result = self.data[self.index]
        self.index += 1
        return result


class MyIterable:
    """Итерируемый объект в Python — это любой объект, от которого можно получить итератор.

    Такими объектами являются, например, списки, кортежи, строки и словари.

    Итерируемыми объектами могут быть и пользовательские объекты, если в их
    классе реализован специальный метод __iter__().

    Или другое определение:

    Итерируемый объект (iterable) - это объект, который реализует метод __iter__() и возвращает итератор.

    """

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return MyIterator(self.data)


iterable = MyIterable([1, 2, 3])
iterator = iter(iterable)

# next можно вызывать от итератора
print(next(iterator))
print(next(iterator))
print(next(iterator))


print(next(iter([1, 2, 3])))


class DoubleIteratorAndIterable:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = self.data[self.index] * 2
        self.index += 1
        return result


# Пример использования
iterable_and_iterator = DoubleIteratorAndIterable([1, 2, 3])
iterator = iter(iterable_and_iterator)

print(next(iterator))
print(next(iterator))
print(next(iterator))
