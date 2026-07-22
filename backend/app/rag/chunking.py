def chunk_text(text: str, target_words: int = 350, overlap_words: int = 50) -> list[str]:
    """
    Splits text into paragraph-aware chunks of roughly target_words each,
    with overlap_words repeated between consecutive chunks so a fact
    split across a boundary still appears whole in at least one chunk.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    current_words: list[str] = []

    for paragraph in paragraphs:
        current_words.extend(paragraph.split())

        if len(current_words) >= target_words:
            chunks.append(" ".join(current_words))
            # keep the last `overlap_words` as the start of the next chunk
            current_words = current_words[-overlap_words:]

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks