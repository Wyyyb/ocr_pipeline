def split_string(s: str, max_length=1000, split_symbol=".") -> list:
    if len(s) <= max_length:
        return [s]

    # 根据句号切分
    sentences = s.split(split_symbol)

    result = []
    current_chunk = ""

    for sentence in sentences:
        # 加上句号，因为我们在split时已经移除了它们
        temp_sentence = sentence + split_symbol

        if len(current_chunk) + len(temp_sentence) <= max_length:
            current_chunk += temp_sentence
        else:
            result.append(current_chunk)
            current_chunk = temp_sentence

    # 添加最后一个块，如果它不为空
    if current_chunk:
        result.append(current_chunk)

    return result


if __name__ == "__main__":
    # 示例
    s = "这是一个测试。This is a test. Another test."
    result = split_string(s*100)
    for r in result:
        print(len(r), r[:50] + "...")  # 打印长度和前50个字符作为示例
