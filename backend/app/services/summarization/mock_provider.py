from app.services.summarization.base import SummarizationProvider, SummaryOutput


class MockSummarizationProvider(SummarizationProvider):
    provider_name = "mock"

    @staticmethod
    def _without_title_echo(title: str, snippet: str) -> str:
        title_words = {word.lower() for word in title.split() if len(word) > 3}
        filtered = [word for word in snippet.split() if word.lower().strip(".,") not in title_words]
        text = " ".join(filtered).strip()
        return text or snippet

    def summarize(self, title: str, snippet: str | None, source_name: str) -> SummaryOutput:
        context = (snippet or "").strip()
        if not context:
            return SummaryOutput(
                summary=(
                    "Available source metadata is limited, so this briefing remains cautious while details are still "
                    "being verified by the publisher and relevant institutions. Expect additional context as official "
                    "updates and follow-up reporting are released."
                ),
                why_this_matters="This item may still influence local or national priorities as more facts are confirmed.",
                key_impact=None,
                quality_flags=["limited_source_context"],
            )
        cleaned_context = self._without_title_echo(title, context)
        summary = (
            "According to available source metadata, this development adds new context for people tracking the story "
            f"in Canada. {cleaned_context} Readers should use the original report for full nuance, direct quotes, and "
            "continuing updates as details evolve."
        )
        trimmed = " ".join(summary.split()[:60]).strip()
        why = "This matters because it could affect policy, costs, or day-to-day decisions for people in Canada."
        impact = "Watch for updates from official agencies or local authorities."
        return SummaryOutput(summary=trimmed, why_this_matters=why, key_impact=impact, quality_flags=[])
