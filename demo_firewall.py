"""
Demo script for CSIF-Guard: Deterministic Semantic Firewall
Simulates: bank load, hallucination attempt, conflict interception, and safe fallback
"""
import sys
import math
from storage.rwif import load_bank_from_json, Crystal, Node, Edge, PhaseTrajectoryEvent
from engine.phase_graph import build_merged_phase_graph, max_multipath_phase_conflict
from core.math import contradiction_threshold
import uuid
from datetime import datetime

def print_conflict_traces(traces):
	for t in traces:
		print("\n--- ConflictPathTrace ---")
		print(f"Source: {t.source}")
		print(f"Target: {t.target}")
		print(f"Path A: {t.path_a}")
		print(f"Path B: {t.path_b}")
		print(f"Phase A: {t.phase_a:.4f}")
		print(f"Phase B: {t.phase_b:.4f}")
		print(f"Residual: {t.residual:.4f}")

def select_baseline_crystal(bank, crystal_id=None, crystal_label=None, domain=None):
	if crystal_id is not None:
		if crystal_id not in bank.crystals:
			raise ValueError(f"Requested crystal_id not found: {crystal_id}")
		return bank.crystals[crystal_id]

	candidates = list(bank.crystals.values())
	if crystal_label is not None:
		candidates = [c for c in candidates if c.crystal_label == crystal_label]
	if domain is not None:
		candidates = [c for c in candidates if c.domain == domain]

	if not candidates:
		raise ValueError("No baseline crystal matched the selection criteria")

	# Deterministic fallback for multi-crystal banks.
	selected = min(candidates, key=lambda c: c.crystal_id)
	return bank.crystals[selected.crystal_id]

def main():
	# 1. Load a baseline bank (for demo, create in-memory if no file provided)
	if len(sys.argv) > 1:
		bank = load_bank_from_json(sys.argv[1])
	else:
		# Minimal demo: whale is a mammal, darkness is dispelled by light
		n1 = Node(str(uuid.uuid4()), "whale", [], "English", {"source_document": "demo", "extraction_timestamp": datetime.now().isoformat(), "extractor": "manual"})
		n2 = Node(str(uuid.uuid4()), "mammal", [], "English", {"source_document": "demo", "extraction_timestamp": datetime.now().isoformat(), "extractor": "manual"})
		n3 = Node(str(uuid.uuid4()), "light", [], "English", {"source_document": "demo", "extraction_timestamp": datetime.now().isoformat(), "extractor": "manual"})
		n4 = Node(str(uuid.uuid4()), "darkness", [], "English", {"source_document": "demo", "extraction_timestamp": datetime.now().isoformat(), "extractor": "manual"})
		e1 = Edge(str(uuid.uuid4()), n1.node_id, "is_a", n2.node_id, "English", True, 0.5236, 0.04, [
			PhaseTrajectoryEvent(datetime.now().isoformat(), 0.52, 0.12, 0.0, "initial_encoding", {"type": "manual"}),
			PhaseTrajectoryEvent(datetime.now().isoformat(), 0.5236, 0.04, 0.0036, "crystallization", {"type": "consensus_gate"})
		], {"encoding_model": "demo", "encoding_run": "demo", "source_documents": ["demo"], "feedback_events": 1, "last_updated": datetime.now().isoformat()})
		e2 = Edge(str(uuid.uuid4()), n3.node_id, "dispels", n4.node_id, "English", True, 0.0, 0.02, [
			PhaseTrajectoryEvent(datetime.now().isoformat(), 0.0, 0.02, 0.0, "initial_encoding", {"type": "manual"})
		], {"encoding_model": "demo", "encoding_run": "demo", "source_documents": ["demo"], "feedback_events": 0, "last_updated": datetime.now().isoformat()})
		nodes = {n.node_id: n for n in [n1, n2, n3, n4]}
		edges = {e1.edge_id: e1, e2.edge_id: e2}
		crystal = Crystal(str(uuid.uuid4()), "demo_crystal", "biology", "English", True, nodes, edges, [], 1.0)
		from storage.rwif import CrystalBank
		bank = CrystalBank(str(uuid.uuid4()), "demo_bank", "English", {crystal.crystal_id: crystal})

	baseline_crystal = select_baseline_crystal(bank, crystal_label="demo_crystal", domain="biology")

	# 2. Simulate a hallucination attempt: "Darkness absorbs light" (contradicts "light dispels darkness")
	n_light = baseline_crystal.nodes
	n_darkness = [n for n in n_light.values() if n.label == "darkness"][0]
	n_light_node = [n for n in n_light.values() if n.label == "light"][0]
	halluc_edge = Edge(
		str(uuid.uuid4()),
		n_darkness.node_id,
		"absorbs",
		n_light_node.node_id,
		"English",
		True,
		math.pi,
		0.02,
		[PhaseTrajectoryEvent(datetime.now().isoformat(), math.pi, 0.02, 0.0, "initial_encoding", {"type": "llm_encoding", "model_id": "demo-llm", "run_id": "hallucination"})],
		{"encoding_model": "demo-llm", "encoding_run": "hallucination", "source_documents": ["demo"], "feedback_events": 0, "last_updated": datetime.now().isoformat()}
	)
	# Create a hallucination crystal
	halluc_nodes = dict(n_light)
	halluc_edges = {halluc_edge.edge_id: halluc_edge}
	halluc_crystal = Crystal(str(uuid.uuid4()), "hallucination_crystal", "biology", "English", False, halluc_nodes, halluc_edges, [], 0.5)

	# 3. The Interception: Run multi-path conflict scan
	merged, shared = build_merged_phase_graph(baseline_crystal, halluc_crystal)
	max_residual, traces = max_multipath_phase_conflict(merged)
	mean_sigma = sum(e.sigma for e in merged.edges) / len(merged.edges) if merged.edges else 0.1
	threshold = contradiction_threshold(mean_sigma)

	print("\n=== CSIF-Guard: Deterministic Semantic Firewall Demo ===")
	print(f"Max multi-path phase residual: {max_residual:.4f}")
	print(f"Contradiction threshold: {threshold:.4f}")
	if max_residual > threshold:
		print("\n[!] Contradiction detected! Write intercepted. Bank remains uncorrupted.")
		print_conflict_traces(traces[:3])
	else:
		print("\n[OK] No contradiction detected. Write would be accepted.")

if __name__ == "__main__":
	main()
