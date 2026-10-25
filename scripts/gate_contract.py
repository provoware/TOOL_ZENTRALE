"""Technical gate completion and explicit, reviewable human decisions."""
from datetime import datetime
import json
import re

from completion_contract import digest, safe_file
from plan_contract import fingerprint, plan_fingerprint


def gate_states(route, actual, root):
    decisions = route.get('gate_decisions', {})
    if not isinstance(decisions, dict) or set(decisions) - set(route['gates']):
        raise ValueError('Unbekannte Gateentscheidung')
    states = {}
    previous = None
    for gate in route['gates']:
        decision = decisions.get(gate)
        states[gate] = 'OPEN'
        if decision is not None and (not isinstance(decision, dict) or not decision):
            raise ValueError(f'{gate}: ungültige Gateentscheidung')
        if decision:
            members = [sid for sid, step in route['steps'].items() if step['gate'] == gate]
            if not members or not all(actual[sid] for sid in members):
                raise ValueError(f'{gate}: Schritte nicht vollständig VERIFIED')
            if previous and states[previous] != 'APPROVED':
                raise ValueError(f'{gate}: Vorgängergate nicht freigegeben')
            if decision.get('state') not in {'CHECKED', 'APPROVED'}:
                raise ValueError(f'{gate}: unbekannter Gatezustand')
            # The exact verified member records are the technical gate evidence.
            evidence_hash = fingerprint({sid: route['evidence_by_step'][sid] for sid in members})
            if decision.get('evidence_sha256') != evidence_hash:
                raise ValueError(f'{gate}: Gatebeleg veraltet')
            if decision['state'] == 'APPROVED':
                name = decision.get('approval', '')
                if not isinstance(name, str) or not name.startswith('governance/approvals/'):
                    raise ValueError(f'{gate}: Freigabeakte fehlt')
                path = safe_file(root, name)
                if digest(path) != decision.get('approval_sha256'):
                    raise ValueError(f'{gate}: Freigabeakte verändert')
                approval = json.loads(path.read_text())
                if (approval.get('schema') != 'provoware-gate-approval/1'
                        or approval.get('approved_by') not in route['completion_policy']['approval_actors']
                        or approval.get('gate_id') != gate or approval.get('decision') != 'APPROVED'
                        or approval.get('plan_sha256') != plan_fingerprint(route)
                        or approval.get('evidence_sha256') != evidence_hash
                        or any(not isinstance(approval.get(k), str) or not approval[k].strip()
                               for k in ('approved_by', 'decided_at', 'decision_url'))):
                    raise ValueError(f'{gate}: dokumentierte Freigabe fehlt oder ist veraltet')
                stamp = datetime.fromisoformat(approval['decided_at'].replace('Z', '+00:00'))
                if stamp.tzinfo is None or not re.fullmatch(
                        r'https://github\.com/' + re.escape(route['repository'])
                        + r'/(pull|issues|discussions)/[0-9]+#[A-Za-z0-9_-]+', approval['decision_url']):
                    raise ValueError(f'{gate}: Freigabezeit oder Entscheidungsreferenz ungültig')
            states[gate] = decision['state']
        previous = gate
    return states


def enforce_gate_entry(route, actual, root):
    states = gate_states(route, actual, root)
    gates = list(route['gates'])
    for sid, step in route['steps'].items():
        pos = gates.index(step['gate'])
        active = actual[sid] or route.get('progress_overrides', {}).get(sid) in {'READY', 'PATCHED'}
        active = active or any(actual[sub['id']] or route.get('progress_overrides', {}).get(sub['id'])
                               in {'READY', 'PATCHED'} for sub in step.get('substeps', []))
        if active and pos and states[gates[pos - 1]] != 'APPROVED':
            raise ValueError(f'{sid}: Vorgängergate {gates[pos - 1]} nicht freigegeben')
    return states
