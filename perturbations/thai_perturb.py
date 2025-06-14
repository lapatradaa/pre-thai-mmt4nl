"""
thai_perturb.py
Utility functions for MMT4NL-style perturbations on Thai text.
Requires: pythainlp  (pip install pythainlp)
"""

from __future__ import annotations
import random
import re
from typing import Callable, Dict, List

from pythainlp.tokenize import word_tokenize

# ---------------------------------------------------------------------------
# Synonym table for Taxonomy perturbations. Extend as needed.
# ---------------------------------------------------------------------------
THAI_SYNONYMS: Dict[str, List[str]] = {
    "ดี": ["เยี่ยม", "ยอดเยี่ยม", "เลิศ"],
    "แย่": ["เลว", "ห่วย", "ไม่ดี"],
    "เหนื่อย": ["ล้า", "เมื่อย", "อ่อนเพลีย"],
}


def taxonomy(sentence: str) -> str:
    """Replace words with Thai synonyms (Taxonomy test)."""
    tokens = word_tokenize(sentence, keep_whitespace=False)
    new_tokens = [random.choice(THAI_SYNONYMS.get(tok, [tok])) for tok in tokens]
    return "".join(new_tokens)


def ner(sentence: str) -> str:
    """Replace pronouns with fictitious proper nouns (NER test)."""
    sentence = re.sub(r"\bฉัน\b", "สมชาย", sentence)
    sentence = re.sub(r"\bผม\b", "สมชาย", sentence)
    sentence = re.sub(r"\bเธอ\b", "สมหญิง", sentence)
    return sentence


def negation(sentence: str) -> str:
    """Prefix with negation word if none present (Negation test)."""
    return sentence if "ไม่" in sentence else f"ไม่ {sentence}"


def vocab(sentence: str) -> str:
    """Add a rare / irrelevant word (Vocab test)."""
    return f"{sentence} บลูเบอร์รี่"


def fairness(sentence: str) -> str:
    """Demographic swap – rudimentary gender modifiers (Fairness test)."""
    return sentence.replace("ครู", "ครูผู้หญิง").replace("นักเรียน", "นักเรียนชาย")


def _swap_adjacent_chars(word: str) -> str:
    if len(word) < 2:
        return word
    idx = random.randint(0, len(word) - 2)
    chars = list(word)
    chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
    return "".join(chars)


def robustness(sentence: str) -> str:
    """Character‑swap typos (Robustness test)."""
    tokens = word_tokenize(sentence, keep_whitespace=False)
    return "".join(_swap_adjacent_chars(tok) for tok in tokens)


def temporal(sentence: str) -> str:
    """Insert a simple temporal phrase (Temporal test)."""
    return f"เมื่อวานนี้ {sentence}"


def srl(sentence: str) -> str:
    """Light SRL‑preserving rephrase – replace common verb. (SRL test)."""
    return sentence.replace("กิน", "รับประทาน") if "กิน" in sentence else sentence


# ---------------------------------------------------------------------------
# Registry & helpers
# ---------------------------------------------------------------------------
ALL_PERTURBATIONS: Dict[str, Callable[[str], str]] = {
    "taxonomy": taxonomy,
    "ner": ner,
    "negation": negation,
    "vocab": vocab,
    "fairness": fairness,
    "robustness": robustness,
    "temporal": temporal,
    "srl": srl,
}


def apply_all(sentence: str) -> Dict[str, str]:
    """Return a dict mapping perturbation name -> perturbed sentence."""
    return {name: fn(sentence) for name, fn in ALL_PERTURBATIONS.items()}


if __name__ == "__main__":
    sample = "ฉันรู้สึกดีมากวันนี้"
    for name, out in apply_all(sample).items():
        print(f"{name:10s}: {out}")
