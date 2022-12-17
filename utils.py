import argparse


def get_middle_line(comment:str, header_len: int):
    comment_len = len(comment)
    spaces_len = header_len - 2 - comment_len
    if spaces_len > 0:
        spaces_left = spaces_len // 2
        spaces_right = spaces_len - spaces_left
        return '#' + ' ' * spaces_left + comment + ' ' * spaces_right + '#'


def generate_comment_header(comment: str, header_type: str = 'large') -> str:
    if header_type == 'large':
        HEADER_LEN = 75
        case_func = str.upper
    elif header_type == 'medium':
        HEADER_LEN = 50
        case_func = str.lower

    else:
        raise NotImplementedError

    first = '#' * HEADER_LEN
    comment_line = case_func(comment)
    middle = get_middle_line(comment_line, HEADER_LEN)

    header = f'{first}\n{middle}\n{first}\n\n\n'
    print(header)

    return header


generate_comment_header('Maintenance endpoints', header_type='medium')

