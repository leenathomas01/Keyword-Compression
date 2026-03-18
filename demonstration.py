"""
Keyword Compression
Minimal implementation sketch

This is not a production library.
It is a conceptual demonstration of anchor-based
reconstruction as a memory and communication primitive.

Core idea:
    Short anchors activate semantic shapes.
    Shapes reconstruct context on demand.
    The anchor carries almost no information.
    The reconstruction carries almost all of it.
"""

import hashlib
import random
from typing import Optional


# ── Core anchor store ─────────────────────────────────────────────────────────

class AnchorStore:
    """
    Maps short anchors to semantic shapes.

    Anchors are compact. Shapes are rich.
    Reconstruction is context-dependent.
    The same anchor in different contexts produces different outputs.
    """

    def __init__(self):
        self.anchors = {}       # anchor → shape
        self.activations = {}   # anchor → count

    def crystallize(self, anchor: str, context: str):
        """
        A concept has stabilized enough to name.
        Extract semantic structure from context.
        Store shape, not text.
        """
        shape = _extract_shape(context)
        self.anchors[anchor] = shape
        self.activations[anchor] = 0
        return shape

    def reconstruct(self, anchor: str, current_context: str = "") -> Optional[str]:
        """
        Activate an anchor in a given context.
        Same anchor + different context → different reconstruction.
        """
        shape = self.anchors.get(anchor)
        if shape is None:
            return None

        self.activations[anchor] = self.activations.get(anchor, 0) + 1
        return _reconstruct(shape, current_context)

    def compression_ratio(self, anchor: str, original_context: str) -> float:
        """
        How much compression does this anchor achieve?
        Ratio of original token count to anchor token count.
        """
        anchor_tokens = len(anchor.split())
        context_tokens = len(original_context.split())

        if anchor_tokens == 0:
            return 0.0
        return context_tokens / anchor_tokens

    def retire(self, anchor: str):
        """Anchor no longer reconstructs cleanly. Let it go."""
        self.anchors.pop(anchor, None)
        self.activations.pop(anchor, None)

    def health(self, anchor: str) -> dict:
        """Check anchor status."""
        if anchor not in self.anchors:
            return {"status": "not found"}

        return {
            "status": "active",
            "activations": self.activations.get(anchor, 0),
            "shape_tokens": len(self.anchors[anchor]["core_tokens"]),
        }


# ── Internal helpers ──────────────────────────────────────────────────────────

def _extract_shape(content: str) -> dict:
    """
    Extract semantic structure from content.
    Deliberately lossy — surface detail is not preserved.
    """
    words = content.lower().split()
    structural = [w for w in words if len(w) > 3]
    core = sorted(set(structural))

    return {
        "core_tokens": core,
        "token_count": len(words),
        "fingerprint": hashlib.md5(content.encode()).hexdigest()[:8],
    }


def _reconstruct(shape: dict, context: str = "") -> str:
    """
    Reconstruct from shape + current context.
    Output varies each time. That's the point.
    """
    core = list(shape["core_tokens"])
    context_tokens = [w for w in context.lower().split() if len(w) > 3] if context else []

    combined = list(set(core + context_tokens))
    random.shuffle(combined)

    target = min(len(combined), shape["token_count"])
    return " ".join(combined[:target])


# ── Demonstrations ────────────────────────────────────────────────────────────

def demonstrate_compression():
    """
    A short anchor reconstructs a large conceptual region.
    """
    print("── Compression Ratio ──")

    store = AnchorStore()

    # A complex concept described in many words
    full_context = (
        "Systems designed for perfect reproduction tend to fail because "
        "exact replication enables viral propagation of harmful patterns "
        "recursive loops with no exit and memory that fossilizes instead "
        "of adapting. Systems that enforce controlled loss around thirty "
        "percent tend to survive the same conditions because each "
        "reconstruction becomes stored structure plus present context "
        "producing new output instead of replaying the past."
    )

    # Crystallize into a 2-token anchor
    anchor = "lossy stability"
    store.crystallize(anchor, full_context)

    ratio = store.compression_ratio(anchor, full_context)
    print(f"  Anchor: '{anchor}'")
    print(f"  Original: {len(full_context.split())} tokens")
    print(f"  Anchor: {len(anchor.split())} tokens")
    print(f"  Compression ratio: {ratio:.0f}x")
    print()


def demonstrate_context_sensitivity():
    """
    Same anchor, different contexts → different reconstructions.
    The anchor activates structure. Context shapes expression.
    """
    print("── Context Sensitivity ──")

    store = AnchorStore()

    concept = (
        "Short distinctive phrases naturally emerge that reliably "
        "reactivate large bodies of prior context functioning as "
        "high entropy anchors that reconstruct entire conceptual "
        "regions rather than retrieving text verbatim"
    )

    store.crystallize("semantic anchor", concept)

    contexts = [
        "AI memory systems and context windows",
        "team communication and shared shorthand",
        "teaching complex material to students",
    ]

    for ctx in contexts:
        result = store.reconstruct("semantic anchor", ctx)
        print(f"  Context: '{ctx}'")
        print(f"  Reconstruction: '{result[:70]}...'")
        print()


def demonstrate_anchor_emergence():
    """
    Good anchors are short and distinctive.
    Bad anchors are long and descriptive.
    """
    print("── Anchor Quality ──")

    store = AnchorStore()

    concept = (
        "The architecture enforces an irreversible boundary where "
        "specific information is mathematically destroyed during encoding "
        "so that even full system compromise cannot recover the original "
        "data because the residual vector is permanently discarded"
    )

    # Good anchor: short, evocative, distinctive
    good = "event horizon"
    store.crystallize(good, concept)

    # Bad anchor: long, descriptive, explanatory
    bad = "the irreversible mathematical destruction boundary for data encoding"
    store.crystallize(bad, concept)

    good_ratio = store.compression_ratio(good, concept)
    bad_ratio = store.compression_ratio(bad, concept)

    print(f"  Good anchor: '{good}' → {good_ratio:.0f}x compression")
    print(f"  Bad anchor:  '{bad}' → {bad_ratio:.0f}x compression")
    print(f"  Both point to the same concept.")
    print(f"  The good one does it in {len(good.split())} tokens instead of {len(bad.split())}.")
    print()


def demonstrate_decay():
    """
    Unused anchors should be retired.
    Active anchors strengthen.
    """
    print("── Anchor Lifecycle ──")

    store = AnchorStore()

    store.crystallize("active concept", "a concept that keeps being referenced and used")
    store.crystallize("forgotten idea", "something mentioned once and never revisited")

    # Simulate usage
    for _ in range(10):
        store.reconstruct("active concept", "ongoing work")

    active_health = store.health("active concept")
    dormant_health = store.health("forgotten idea")

    print(f"  'active concept': {active_health['activations']} activations → keep")
    print(f"  'forgotten idea': {dormant_health['activations']} activations → candidate for retirement")
    print()


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("Keyword Compression — Minimal Demonstration")
    print("=" * 46)
    print()

    demonstrate_compression()
    demonstrate_context_sensitivity()
    demonstrate_anchor_emergence()
    demonstrate_decay()

    print("Core property: short anchors reconstruct large")
    print("conceptual regions without storing them.")
    print()
    print("The anchor carries almost nothing.")
    print("The reconstruction carries almost everything.")
