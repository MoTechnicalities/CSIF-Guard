"""
Phase geometry primitives for CSIF-Guard (The Agentic Hippocampus)
Implements: wrap_pi, phase_distance, contradiction_threshold, etc.
"""
import math

def wrap_pi(theta):
    """Wrap angle to [-pi, pi]."""
    return ((theta + math.pi) % (2 * math.pi)) - math.pi

def phase_distance(theta_a, theta_b):
    """Angular distance between two phase values."""
    return abs(wrap_pi(theta_a - theta_b))

def normalized_resonance(theta_a, theta_b):
    """Normalized resonance. 0.0 = perfect coherence, 1.0 = maximum opposition."""
    return phase_distance(theta_a, theta_b) / math.pi

def contradiction_threshold(sigma, c=0.5):
    """Adaptive contradiction detection threshold."""
    return math.pi / 2 + c * sigma

def circular_mean(phases):
    """Mean of angles on a circle."""
    sin_sum = sum(math.sin(p) for p in phases)
    cos_sum = sum(math.cos(p) for p in phases)
    return math.atan2(sin_sum, cos_sum)

def compose_path_phase(phases):
    """Compose phase angles along a path."""
    total = sum(phases)
    return wrap_pi(total)

def nudge_phase(theta, error_signal, evidence_weight, alpha=0.1):
    """Apply one outcome-driven phase correction."""
    delta = alpha * error_signal * evidence_weight
    return wrap_pi(theta + delta)

def tighten_sigma(sigma, evidence_weight, rate=0.1):
    """Tighten confidence band with new evidence."""
    return sigma * (1.0 - evidence_weight * rate)
