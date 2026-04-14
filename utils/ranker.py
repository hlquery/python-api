"""hlquery Python Client - Ranking Utilities"""

import math
from typing import Dict, Optional

DEFAULT_WEIGHTS = {
    'popularity_log': 1.15,
    'hit_log': 0.95,
    'popularity_sqrt': 0.25,
    'hit_log_sqrt': 0.15,
}


def compute_rank_signal(popularity: float, hit_log: float, weights: Optional[Dict[str, float]] = None) -> float:
    w = DEFAULT_WEIGHTS.copy()
    if weights:
        for key, value in weights.items():
            if key in w and isinstance(value, (int, float)):
                w[key] = float(value)

    return (
        math.log(popularity + 1) * w['popularity_log']
        + math.log(hit_log + 1) * w['hit_log']
        + math.sqrt(popularity) * w['popularity_sqrt']
        + math.sqrt(hit_log) * w['hit_log_sqrt']
    )


def attach_rank_sort(params: Dict[str, object], field: str = 'rank_signal', direction: str = 'desc') -> None:
    if not isinstance(params, dict):
        return

    direction = direction.lower()
    if direction not in ('asc', 'desc'):
        direction = 'desc'

    sort_instruction = f"{field}:{direction}"

    existing = params.get('sort_by')
    if isinstance(existing, str) and existing.strip():
        params['sort_by'] = f"{existing},{sort_instruction}"
    else:
        params['sort_by'] = sort_instruction
