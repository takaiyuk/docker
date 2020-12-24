import neologdn


def test_normalize():
    assert neologdn.normalize("ﾊﾝｶｸｶﾅ") == "ハンカクカナ"
