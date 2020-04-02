def rebuild_lines(string: str) -> str:
    # s = string.split(' ')
    # for word in s:
    #     l = count_chars(word)
    # return None
    if len(string) <= 19:
        return string.replace(' ', '&nbsp;')
    return string


def count_chars(word: str) -> int:
    return len(word) - word.count('&nbsp;') * 5


def get_font_size(n: int) -> tuple:
    a = {
        13: 24,
        14: 23,
        15: 21,
        16: 20,
        17: 18,
        18: 17,
        19: 16,
    }
    if 13 <= n <= 19:
        return a[n], a[n] + 2
    elif n < 13:
        return a[13], a[13] + 2
    return a[19], a[19] + 2


if __name__ == '__main__':
    print(rebuild_lines('Костнопроводящие наушники'), 'Костнопроводящие<br/>наушники')
    print(rebuild_lines('Константинопольский Константинопольский'), 'Константинопольский<br/>Константинопольский')
    print(rebuild_lines('A5 2020 и A9 2020'), 'A5&nbsp;2020&nbsp;и&nbsp;A9&nbsp;2020')
    print(rebuild_lines('Чехлы чехлы Чехлы чехлы'), 'Чехлы&nbsp;чехлы<br/>Чехлы&nbsp;чехлы')
    print(rebuild_lines('iPhone 11 Pro Max'), 'iPhone&nbsp;11&nbsp;Pro&nbsp;Max')
