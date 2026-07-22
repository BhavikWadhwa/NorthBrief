from dataclasses import dataclass


@dataclass
class SummaryOutput:
    summary: str
    why_this_matters: str
    key_impact: str | None = None
    quality_flags: list[str] | None = None


class SummarizationProvider:
    provider_name = "base"

    def summarize(self, title: str, snippet: str | None, source_name: str) -> SummaryOutput:
        raise NotImplementedError

