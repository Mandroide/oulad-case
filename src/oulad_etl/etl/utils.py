"""FK-aware helpers shared by the ETL layer."""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable, List, Dict

import sqlalchemy as sa


def topologically_sort_tables(engine: sa.engine.Engine, candidates: Iterable[str]) -> List[str]:
    """
    Return *candidates* sorted so that every parent table precedes its children.

    Uses information_schema through SQLAlchemy’s inspector; works for MySQL,
    PostgreSQL, and SQLite alike.
    """
    insp = sa.inspect(engine)

    # Build dependency graph: child -> {parents}
    graph: Dict[str, set[str]] = defaultdict(set)
    for tbl in candidates:
        for fk in insp.get_foreign_keys(tbl):
            parent = fk["referred_table"]
            if parent in candidates:
                graph[tbl].add(parent)

    # Kahn’s algorithm
    no_deps = [t for t in candidates if not graph[t]]
    ordered: List[str] = []

    while no_deps:
        n = no_deps.pop()
        ordered.append(n)
        for m in list(graph):
            if n in graph[m]:
                graph[m].remove(n)
                if not graph[m]:
                    no_deps.append(m)

    if len(ordered) != len(set(candidates)):
        cyclic = set(candidates) - set(ordered)
        raise RuntimeError(f"Foreign-key cycle detected: {cyclic}")

    return ordered
