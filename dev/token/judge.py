def is_chinese_char(char):
    """Strict Definition of Chinese Characters.
    Includes:
    1. CJK Unified Ideographs (Common)
    2. CJK Unified Ideographs Extension A (Rare but valid)
    3. CJK Compatibility Ideographs
    """
    cp = ord(char)
    return (
        0x4E00 <= cp <= 0x9FFF  # CJK Unified Ideographs
        or 0x3400 <= cp <= 0x4DBF  # CJK Extension A
        or 0xF900 <= cp <= 0xFAFF  # CJK Compatibility Ideographs
    )


def is_cjk_punctuation(char):
    """Checks for Chinese/Japanese/Korean punctuation.
    Includes: 。 、 【 】 ， ？ ！ etc.
    """
    cp = ord(char)
    return (
        0x3000 <= cp <= 0x303F  # CJK Symbols and Punctuation
        or 0xFF00 <= cp <= 0xFFEF  # Full-width ASCII variants (，？)
    )


def is_useful_ascii(char):
    """Checks if a character is 'useful' ASCII.
    - Allows: Letters, Numbers, Punctuation.
    - Rejects: Weird control characters (except space).
    """
    if not char.isascii():
        return False
    # Allow printable characters (A-Z, 0-9, !@#...) and space
    return char.isprintable() or char == " "


def judge_token(token_str) -> bool:
    if not token_str:
        return False

    # 1. Clean Tokenizer Artifacts
    # Qwen/Llama use U+2581 ( ), BERT uses ##, GPT uses Ġ
    # We strip them to check the actual "core" of the token.
    clean_text = token_str.lstrip("##").lstrip("\u2581").lstrip("Ġ")

    if not clean_text:
        # If the token was ONLY an artifact (like just "##"), do you want it?
        # Usually 'False' for "useful words", 'True' if you need structural tokens.
        return False

    # 2. THE STRICT CHECK (The "All" Rule)
    # Every single character must be in our "Safe List".
    # If even ONE character is an Emoji, Greek, Cyrillic, or unprintable -> REJECT.
    for char in clean_text:
        is_valid = is_useful_ascii(char) or is_chinese_char(char) or is_cjk_punctuation(char)
        if not is_valid:
            return False

    return True


if __name__ == "__main__":
    # --- Test Cases to prove strictness ---
    test_tokens = [
        "你好",  # True (Pure Chinese)
        "Hello",  # True (Pure ASCII)
        "T恤",  # True (Mixed useful: T-Shirt)
        "A股",  # True (Mixed useful: A-Shares)
        "hello你好",  # True (Mixed useful)
        "123",  # True (Numbers)
        "，",  # True (Chinese Punctuation)
        # --- The ones we want to REJECT ---
        "❤",  # False (Emoji)
        "你好❤",  # False (Chinese mixed with Emoji)
        "α",  # False (Greek)
        "à",  # False (Latin-1 Extended, not ASCII, not Chinese)
        "\x00",  # False (Control char)
        "★",  # False (Symbol)
        "##",  # False (Empty after clean)
    ]

    print(f"{'Token':<30} | {'Result'}")
    print("-" * 20)
    for t in test_tokens:
        print(f"{t:<10} | {judge_token(t)}")
