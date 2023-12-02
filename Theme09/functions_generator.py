def my_range(start, stop, step=1):
    value = start
    while (step > 0 and value < stop) or (step < 0 and value > stop):
        yield value
        value += step


def my_map(func, iterable):
    for item in iterable:
        yield func(item)


# Пример использования
original_list = [1, 2, 3, 4, 5]

# Используем my_map для удвоения значений
result = list(my_map(lambda x: x * 2, original_list))

print(result)
