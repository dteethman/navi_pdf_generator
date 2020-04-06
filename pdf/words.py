from reportlab.lib.units import mm


def count_chars(string: str) -> int:
    if '<br/>' in string:
        s = string.split('<br/>')
        length = len(s[0]) if s[0] > s[1] else len(s[1])
    else:
        length = len(string)
    return length - string.count('&nbsp;') * 5 - string.count('&amp;') * 4


def get_font_settings(string: str) -> tuple:
    n = count_chars(string)
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
