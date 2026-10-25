"""Canonical plan identity without mutable completion administration."""
import copy
import hashlib
import json


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def plan_fingerprint(route):
    plan = copy.deepcopy(route)
    for key in ('progress_overrides', 'evidence_by_step', 'gate_decisions', 'plan_status'):
        plan.pop(key, None)
    for entry in plan.get('iteration_queue', []):
        entry.pop('status', None)
    return fingerprint(plan)
