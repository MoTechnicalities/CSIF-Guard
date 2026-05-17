"""
PhaseGraph and multi-path conflict detection for CSIF-Guard
Implements: PhaseGraph, build_merged_phase_graph, pairwise_conflict, max_multipath_phase_conflict
"""
from core.math import wrap_pi, phase_distance, compose_path_phase

# PhaseEdge: source, target, phase, sigma, edge_id
class PhaseEdge:
	def __init__(self, source, target, phase, sigma, edge_id):
		self.source = source
		self.target = target
		self.phase = phase
		self.sigma = sigma
		self.edge_id = edge_id

class PhaseGraph:
	def __init__(self):
		self.nodes = set()
		self.edges = []  # list of PhaseEdge

	def add_edge(self, source, target, phase, sigma, edge_id):
		self.nodes.add(source)
		self.nodes.add(target)
		self.edges.append(PhaseEdge(source, target, phase, sigma, edge_id))

	def find_edges(self, source, target):
		return [e for e in self.edges if e.source == source and e.target == target]

def build_phase_graph(crystal):
	graph = PhaseGraph()
	for edge in crystal.edges.values():
		source_label = crystal.nodes[edge.source_node].label
		target_label = crystal.nodes[edge.target_node].label
		phase = edge.phase_trajectory[-1].phase if edge.phase_trajectory else edge.base_phase
		sigma = edge.phase_trajectory[-1].confidence_band if edge.phase_trajectory else edge.confidence_band
		graph.add_edge(source_label, target_label, phase, sigma, edge.edge_id)
	return graph

def build_merged_phase_graph(crystal_a, crystal_b):
	graph_a = build_phase_graph(crystal_a)
	graph_b = build_phase_graph(crystal_b)
	shared_labels = graph_a.nodes & graph_b.nodes
	merged = PhaseGraph()
	merged.nodes = graph_a.nodes | graph_b.nodes
	merged.edges = graph_a.edges + graph_b.edges
	# Bridge edges: zero-phase self-loops on shared nodes
	for label in shared_labels:
		merged.add_edge(label, label, 0.0, 0.0, None)
	return merged, shared_labels

def all_simple_paths(graph, source, target, max_depth=10):
	# DFS for all simple paths (no repeated nodes), preserving edge identity/direction.
	paths = []
	# Stack entries: (current_node, node_path, step_path)
	# step_path entries are (PhaseEdge, direction_sign) with +1 native, -1 reverse traversal.
	stack = [(source, [source], [])]
	while stack:
		current, node_path, step_path = stack.pop()
		if current == target and len(node_path) > 1:
			paths.append({"nodes": node_path, "steps": step_path})
		if len(node_path) >= max_depth:
			continue
		for e in graph.edges:
			next_node = None
			direction_sign = None
			if e.source == current:
				next_node = e.target
				direction_sign = 1
			elif e.target == current:
				next_node = e.source
				direction_sign = -1
			if next_node is not None and next_node not in node_path:
				stack.append((next_node, node_path + [next_node], step_path + [(e, direction_sign)]))
	return paths

def path_phase(path_record):
	phases = []
	for edge, direction_sign in path_record["steps"]:
		signed_phase = edge.phase if direction_sign == 1 else wrap_pi(-edge.phase)
		phases.append(signed_phase)
	return compose_path_phase(phases)

class ConflictPathTrace:
	def __init__(self, source, target, path_a, path_b, phase_a, phase_b, residual):
		self.source = source
		self.target = target
		self.path_a = path_a
		self.path_b = path_b
		self.phase_a = phase_a
		self.phase_b = phase_b
		self.residual = residual

	def to_dict(self):
		return {
			"source": self.source,
			"target": self.target,
			"path_a": self.path_a,
			"path_b": self.path_b,
			"phase_a": self.phase_a,
			"phase_b": self.phase_b,
			"residual": self.residual
		}

def pairwise_conflict(graph, source, target):
	paths = all_simple_paths(graph, source, target)
	if len(paths) < 2:
		return 0.0, []
	max_residual = 0.0
	traces = []
	for i in range(len(paths)):
		for j in range(i+1, len(paths)):
			phase_i = path_phase(paths[i])
			phase_j = path_phase(paths[j])
			residual = phase_distance(phase_i, phase_j)
			traces.append(ConflictPathTrace(
				source, target, paths[i]["nodes"], paths[j]["nodes"], phase_i, phase_j, residual
			))
			if residual > max_residual:
				max_residual = residual
	return max_residual, traces

def max_multipath_phase_conflict(graph):
	global_max = 0.0
	all_traces = []
	nodes = list(graph.nodes)
	for i in range(len(nodes)):
		for j in range(len(nodes)):
			if i == j:
				continue
			score, traces = pairwise_conflict(graph, nodes[i], nodes[j])
			all_traces.extend(traces)
			if score > global_max:
				global_max = score
	return global_max, all_traces
