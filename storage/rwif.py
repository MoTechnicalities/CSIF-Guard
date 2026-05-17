"""
RWIF Crystal and Bank serialization/parsing for CSIF-Guard
Implements: .rwif-crystal and .rwif-bank JSON schema, append-only phase_trajectory
"""
import json
import uuid
from datetime import datetime

class PhaseTrajectoryEvent:
	def __init__(self, timestamp, phase, confidence_band, drift_delta, event_type, source):
		self.timestamp = timestamp
		self.phase = phase
		self.confidence_band = confidence_band
		self.drift_delta = drift_delta
		self.event_type = event_type
		self.source = source

	def to_dict(self):
		return {
			"timestamp": self.timestamp,
			"phase": self.phase,
			"confidence_band": self.confidence_band,
			"drift_delta": self.drift_delta,
			"event_type": self.event_type,
			"source": self.source
		}

	@staticmethod
	def from_dict(d):
		return PhaseTrajectoryEvent(
			d["timestamp"], d["phase"], d["confidence_band"],
			d["drift_delta"], d["event_type"], d["source"]
		)

class Node:
	def __init__(self, node_id, label, aliases, lobe, provenance):
		self.node_id = node_id
		self.label = label
		self.aliases = aliases or []
		self.lobe = lobe
		self.provenance = provenance

	def to_dict(self):
		return {
			"node_id": self.node_id,
			"label": self.label,
			"aliases": self.aliases,
			"lobe": self.lobe,
			"provenance": self.provenance
		}

	@staticmethod
	def from_dict(d):
		return Node(d["node_id"], d["label"], d.get("aliases", []), d["lobe"], d["provenance"])

class Edge:
	def __init__(self, edge_id, source_node, relation, target_node, lobe, reinforcing, base_phase, confidence_band, phase_trajectory, provenance):
		self.edge_id = edge_id
		self.source_node = source_node
		self.relation = relation
		self.target_node = target_node
		self.lobe = lobe
		self.reinforcing = reinforcing
		self.base_phase = base_phase
		self.confidence_band = confidence_band
		self.phase_trajectory = phase_trajectory  # list of PhaseTrajectoryEvent
		self.provenance = provenance

	def to_dict(self):
		return {
			"edge_id": self.edge_id,
			"source_node": self.source_node,
			"relation": self.relation,
			"target_node": self.target_node,
			"lobe": self.lobe,
			"reinforcing": self.reinforcing,
			"base_phase": self.base_phase,
			"confidence_band": self.confidence_band,
			"phase_trajectory": [e.to_dict() for e in self.phase_trajectory],
			"provenance": self.provenance
		}

	@staticmethod
	def from_dict(d):
		return Edge(
			d["edge_id"], d["source_node"], d["relation"], d["target_node"],
			d["lobe"], d["reinforcing"], d["base_phase"], d["confidence_band"],
			[PhaseTrajectoryEvent.from_dict(e) for e in d["phase_trajectory"]],
			d["provenance"]
		)

class Crystal:
	def __init__(self, crystal_id, crystal_label, domain, lobe, frozen, nodes, edges, version_history, stability_score, **kwargs):
		self.crystal_id = crystal_id
		self.crystal_label = crystal_label
		self.domain = domain
		self.lobe = lobe
		self.frozen = frozen
		self.nodes = nodes  # dict of node_id: Node
		self.edges = edges  # dict of edge_id: Edge
		self.version_history = version_history or []
		self.stability_score = stability_score
		self.extra = kwargs  # for optional fields

	def to_dict(self):
		d = {
			"crystal_id": self.crystal_id,
			"crystal_label": self.crystal_label,
			"domain": self.domain,
			"lobe": self.lobe,
			"frozen": self.frozen,
			"nodes": [n.to_dict() for n in self.nodes.values()],
			"edges": [e.to_dict() for e in self.edges.values()],
			"version_history": self.version_history,
			"stability_score": self.stability_score
		}
		d.update(self.extra)
		return d

	@staticmethod
	def from_dict(d):
		nodes = {n["node_id"]: Node.from_dict(n) for n in d["nodes"]}
		edges = {e["edge_id"]: Edge.from_dict(e) for e in d["edges"]}
		return Crystal(
			d["crystal_id"], d["crystal_label"], d["domain"], d["lobe"], d["frozen"],
			nodes, edges, d.get("version_history", []), d["stability_score"],
			**{k: v for k, v in d.items() if k not in {"crystal_id","crystal_label","domain","lobe","frozen","nodes","edges","version_history","stability_score"}}
		)

	def append_trajectory(self, edge_id, event):
		if edge_id in self.edges:
			self.edges[edge_id].phase_trajectory.append(event)

	def is_frozen(self):
		return self.frozen

	def get_node_labels(self):
		return [n.label for n in self.nodes.values()]

	def get_edge_phases(self):
		return [e.phase_trajectory[-1].phase for e in self.edges.values() if e.phase_trajectory]

def load_crystal_from_json(path):
	with open(path, 'r') as f:
		d = json.load(f)
	return Crystal.from_dict(d)

def save_crystal_to_json(crystal, path):
	with open(path, 'w') as f:
		json.dump(crystal.to_dict(), f, indent=2)

# Bank: a collection of crystals
class CrystalBank:
	def __init__(self, bank_id, bank_label, lobe, crystals=None, **kwargs):
		self.bank_id = bank_id
		self.bank_label = bank_label
		self.lobe = lobe
		self.crystals = crystals or {}  # dict of crystal_id: Crystal
		self.extra = kwargs

	def to_dict(self):
		d = {
			"bank_id": self.bank_id,
			"bank_label": self.bank_label,
			"lobe": self.lobe,
			"crystals": [c.to_dict() for c in self.crystals.values()]
		}
		d.update(self.extra)
		return d

	@staticmethod
	def from_dict(d):
		crystals = {c["crystal_id"]: Crystal.from_dict(c) for c in d["crystals"]}
		return CrystalBank(
			d["bank_id"], d["bank_label"], d["lobe"], crystals,
			**{k: v for k, v in d.items() if k not in {"bank_id","bank_label","lobe","crystals"}}
		)

def load_bank_from_json(path):
	with open(path, 'r') as f:
		d = json.load(f)
	return CrystalBank.from_dict(d)

def save_bank_to_json(bank, path):
	with open(path, 'w') as f:
		json.dump(bank.to_dict(), f, indent=2)
