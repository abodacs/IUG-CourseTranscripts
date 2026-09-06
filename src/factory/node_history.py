"""CF-05: teaching-node split/merge history.

Node IDs are identities that outlive revisions. When one node splits into
several, or several merge into one, the history records the event; old
references keep resolving through `descendants()`. Identity is never a
paragraph ordinal or a content hash, so history — not location — defines
what a node is.
"""
from src.factory.evidence import AppendOnlyJsonLog, EvidencePolicyError


class NodeHistoryError(EvidencePolicyError):
    """A split/merge event is invalid (unknown source IDs, colliding target
    IDs, or a cycle)."""


class NodeHistory(AppendOnlyJsonLog):
    PREFIX = "n"

    def split(self, source_id, new_ids, reason, revision):
        new_ids = list(new_ids)
        if not source_id or len(set(new_ids)) != len(new_ids) or not new_ids:
            raise NodeHistoryError("a split needs a source and distinct target IDs")
        if source_id in new_ids:
            raise NodeHistoryError(f"{source_id}: a split target cannot be its own source")
        for target in new_ids:
            self._require_never_seen(target)
        self._require_live(source_id)
        record = {
            "kind": "split",
            "event_id": self._next_id(),
            "source_id": source_id,
            "new_ids": new_ids,
            "reason": reason,
            "revision": revision,
            "created_at": _now(),
        }
        self.records.append(record)
        self._save()
        return record

    def merge(self, source_ids, new_id, reason, revision):
        source_ids = list(source_ids)
        if len(source_ids) < 2 or len(set(source_ids)) != len(source_ids):
            raise NodeHistoryError("a merge needs at least two distinct source IDs")
        if new_id in source_ids:
            raise NodeHistoryError(f"{new_id}: a merge target cannot be one of its sources")
        self._require_never_seen(new_id)
        for source_id in source_ids:
            self._require_live(source_id)
        record = {
            "kind": "merge",
            "event_id": self._next_id(),
            "source_ids": source_ids,
            "new_id": new_id,
            "reason": reason,
            "revision": revision,
            "created_at": _now(),
        }
        self.records.append(record)
        self._save()
        return record

    def consumed_ids(self):
        """IDs split or merged away: referencing them as live nodes is stale."""
        consumed = set()
        for record in self.records:
            if record["kind"] == "split":
                consumed.add(record["source_id"])
            elif record["kind"] == "merge":
                consumed.update(record["source_ids"])
        return consumed

    def _require_live(self, node_id):
        if node_id in self.consumed_ids():
            raise NodeHistoryError(f"{node_id}: was already consumed by an earlier split/merge")

    def _require_never_seen(self, node_id):
        for record in self.records:
            seen = set(record.get("new_ids", [])) | {record.get("new_id")} | {record.get("source_id")} | set(record.get("source_ids", []))
            if node_id in seen:
                raise NodeHistoryError(f"{node_id}: node IDs are identities and are never reused")

    def descendants(self, node_id):
        """All live IDs an old reference resolves to today."""
        current = {node_id}
        while True:
            expanded = False
            for record in self.records:
                if record["kind"] == "split" and record["source_id"] in current:
                    current.discard(record["source_id"])
                    current.update(record["new_ids"])
                    expanded = True
                elif record["kind"] == "merge" and record["source_ids"] and record["source_ids"][0] in current:
                    for source_id in record["source_ids"]:
                        current.discard(source_id)
                    current.add(record["new_id"])
                    expanded = True
            if not expanded:
                return sorted(current)


def _now():
    import datetime

    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def validate_lesson_nodes(document, history):
    """A lesson may use fresh IDs or unconsumed historical IDs — but never an
    ID that was split or merged away (that reference is stale)."""
    consumed = history.consumed_ids()
    for node in document["nodes"]:
        if node["node_id"] in consumed:
            raise NodeHistoryError(
                f"{node['node_id']}: stale node ID (split/merged away); "
                f"resolves to {history.descendants(node['node_id'])}"
            )
    return True
