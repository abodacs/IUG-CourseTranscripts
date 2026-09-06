"""CF-04: guarded dispatch wiring the ledger to a provider adapter.

The guard enforces the ordering the plan requires: reserve -> commit
`dispatched` -> external call -> persist output -> commit usage with success.
Every deviation lands in a durable state (`reserved`, `dispatched`,
`outcome_unknown`) instead of a lost reservation or a silent success.
"""
from src.factory.ledger import LedgerPolicyError


class ProviderUnavailable(RuntimeError):
    """The provider refused/failed before any work could happen."""


class ResponseLost(RuntimeError):
    """The provider may have done work; the response never arrived."""


class PersistenceFailed(RuntimeError):
    """The provider response arrived but persisting it failed. The response
    is carried so the caller can retry persistence without a re-dispatch."""

    def __init__(self, attempt_id, response, usage):
        super().__init__(f"{attempt_id}: output persistence failed")
        self.attempt_id = attempt_id
        self.response = response
        self.usage = usage


def guarded_dispatch(ledger, provider, *, unit_id, model, reserved_in, reserved_out,
                     run_id="pilot", persist_output=None):
    """Run one bounded attempt. Raises what the fault surface raises; the
    ledger state always shows the truth of how far it got."""
    attempt_id = ledger.reserve(unit_id, model, reserved_in, reserved_out, run_id)
    ledger.mark_dispatched(attempt_id)
    try:
        response = provider.call(model, reserved_in, reserved_out)
    except ProviderUnavailable:
        ledger.fail_confirmed(attempt_id)
        ledger.count_event(unit_id, "transient_retry")
        raise
    except ResponseLost:
        ledger.mark_unknown(attempt_id)
        raise
    usage = provider.usage(response)
    if persist_output is not None:
        try:
            output_ref = persist_output(response)
        except Exception as error:
            raise PersistenceFailed(attempt_id, response, usage) from error
    else:
        output_ref = None
    ledger.complete(attempt_id, usage["in"], usage["out"], output_ref)
    return attempt_id, response, usage
