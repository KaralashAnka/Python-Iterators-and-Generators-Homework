import types


# Задание 1: Простой итератор для списков списков
class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0  # индекс текущего внешнего списка
        self.inner_index = 0  # индекс текущего элемента во внутреннем списке

    def __iter__(self):
        self.outer_index = 0
        self.inner_index = 0
        return self

    def __next__(self):
        # Проверяем, что мы не вышли за границы внешнего списка
        while self.outer_index < len(self.list_of_list):
            current_inner_list = self.list_of_list[self.outer_index]

            # Проверяем, что мы не вышли за границы внутреннего списка
            if self.inner_index < len(current_inner_list):
                item = current_inner_list[self.inner_index]
                self.inner_index += 1
                return item
            else:
                # Переходим к следующему внутреннему списку
                self.outer_index += 1
                self.inner_index = 0

        # Если дошли до конца всех списков
        raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    print("Тест 1 пройден успешно!")


# Задание 2: Простой генератор для списков списков
def flat_generator(list_of_lists):
    for inner_list in list_of_lists:
        for item in inner_list:
            yield item


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print("Тест 2 пройден успешно!")


# Задание 3: Итератор для многоуровневой вложенности
class FlatIteratorAdvanced:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.stack = []  # стек для хранения состояния итерации

    def __iter__(self):
        # Инициализируем стек с исходным списком
        self.stack = [(self.list_of_list, 0)]
        return self

    def __next__(self):
        while self.stack:
            current_list, index = self.stack[-1]

            # Если достигли конца текущего списка, удаляем его из стека
            if index >= len(current_list):
                self.stack.pop()
                continue

            item = current_list[index]
            # Увеличиваем индекс для следующей итерации
            self.stack[-1] = (current_list, index + 1)

            # Если элемент - список, добавляем его в стек
            if isinstance(item, list):
                self.stack.append((item, 0))
            else:
                # Возвращаем элемент, который не является списком
                return item

        # Если стек пуст, значит обход завершен
        raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIteratorAdvanced(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorAdvanced(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    print("Тест 3 пройден успешно!")


# Задание 4: Генератор для многоуровневой вложенности
def flat_generator_advanced(list_of_list):
    for item in list_of_list:
        if isinstance(item, list):
            # Рекурсивно обрабатываем вложенные списки
            yield from flat_generator_advanced(item)
        else:
            yield item


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_advanced(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_advanced(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_advanced(list_of_lists_2), types.GeneratorType)
    print("Тест 4 пройден успешно!")


if __name__ == '__main__':
    print("Запуск всех тестов...")
    test_1()
    test_2()
    test_3()
    test_4()
    print("Все тесты пройдены успешно!")