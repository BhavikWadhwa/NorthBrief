import re

from app.core.config import get_settings
from app.services.summarization.base import SummaryOutput
from app.services.summarization.mock_provider import MockSummarizationProvider
from app.services.summarization.openai_provider import OpenAISummarizationProvider


def get_provider():
    settings = get_settings()
    if settings.summarization_provider.lower() == "openai":
        return OpenAISummarizationProvider()
    return MockSummarizationProvider()


def enforce_summary_guardrails(output: SummaryOutput) -> SummaryOutput:
    words = output.summary.split()
    if len(words) < 50:
        padding = (
            "The available metadata remains limited, so readers should review the original reporting for context, "
            "evidence, and any newly confirmed details."
        )
        output.summary = f"{output.summary.strip()} {padding}".strip()
        words = output.summary.split()
        output.quality_flags = (output.quality_flags or []) + ["expanded_for_min_length"]
    if len(words) > 60:
        output.summary = " ".join(words[:60]).strip()
        output.quality_flags = (output.quality_flags or []) + ["trimmed_for_length"]
    leading_sentence = output.summary.split(".")[0].lower()
    if re.match(r"^[a-z0-9\s\-:,]+$", leading_sentence) and len(leading_sentence.split()) <= 14:
        output.quality_flags = (output.quality_flags or []) + ["possible_title_echo"]
    if len(output.why_this_matters.split()) > 28:
        output.why_this_matters = " ".join(output.why_this_matters.split()[:28]).strip()
    return output
