def get_middle_text(text, start_char, end_char):
    """
    获取文本中两个特定字符之间的部分。

    :param text: 完整的字符串。
    :param start_char: 开始字符。
    :param end_char: 结束字符。
    :return: 子字符串，如果未找到则返回空字符串。
    """
    start_index = text.find(start_char)
    if start_index == -1:
        return ""  # 未找到开始字符

    start_index += len(start_char)  # 跳过开始字符本身
    end_index = text.find(end_char, start_index)
    if end_index == -1:
        return ""  # 未找到结束字符

    return text[start_index:end_index]

