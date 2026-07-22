from app.services.summarization.base import SummaryOutput
from app.services.summarization.service import enforce_summary_guardrails


def test_summary_length_guardrail() -> None:
    output = SummaryOutput(
        summary=" ".join(["word"] * 90),
        why_this_matters="This matters because communities need clear guidance and resilient planning over the coming weeks.",
        key_impact="Impacts expected in services",
        quality_flags=[],
    )
    result = enforce_summary_guardrails(output)
    assert len(result.summary.split()) <= 60
    assert "trimmed_for_length" in (result.quality_flags or [])

