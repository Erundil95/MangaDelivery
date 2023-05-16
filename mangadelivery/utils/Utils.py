def replace_special_numbers(self, string):
    pattern = r'[①-⑳]'  # match any circled number from 1 to 20
    char_map = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5',
                '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10',
                '⑪': '11', '⑫': '12', '⑬': '13', '⑭': '14', '⑮': '15',
                '⑯': '16', '⑰': '17', '⑱': '18', '⑲': '19', '⑳': '20'}
    return re.sub(pattern, lambda match: char_map[match.group()], string)
