from reportlab.lib.units import mm


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


def get_font_settings(n: int) -> tuple:
    size_and_offset = {
        13: (24, 3*mm),
        14: (23, 3.5*mm),
        15: (21, 4*mm),
        16: (20, 4.5*mm),
        17: (18, 5*mm),
        18: (17, 5.5*mm),
        19: (16, 6*mm)
    }
    if 13 <= n <= 19:
        return size_and_offset[n][0], size_and_offset[n][0] + 2, size_and_offset[n][1]
    elif n < 13:
        return size_and_offset[13][0], size_and_offset[13][0] + 2, size_and_offset[13][1]
    return size_and_offset[19][0], size_and_offset[19][0] + 2, size_and_offset[19][1]


if __name__ == '__main__':
    print(rebuild_lines('Костнопроводящие наушники'), 'Костнопроводящие<br/>наушники')
    print(rebuild_lines('Константинопольский Константинопольский'), 'Константинопольский<br/>Константинопольский')
    print(rebuild_lines('A5 2020 и A9 2020'), 'A5&nbsp;2020&nbsp;и&nbsp;A9&nbsp;2020')
    print(rebuild_lines('Чехлы чехлы Чехлы чехлы'), 'Чехлы&nbsp;чехлы<br/>Чехлы&nbsp;чехлы')
    print(rebuild_lines('iPhone 11 Pro Max'), 'iPhone&nbsp;11&nbsp;Pro&nbsp;Max')
