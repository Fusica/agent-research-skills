# Publication Relevance Policy

Current user preference: keep literature discovery unrestricted.

## Rule

Do not exclude papers by publisher, journal, conference, venue category, DOI prefix,
domain, preprint status, or perceived source quality. Do not rank papers by venue
prestige or source label.

The only default selection criterion is topical relevance to the user's current
query, stable kernel, or bounded research question.

## How To Use Search Results

- Keep all records returned by Semantic Scholar, arXiv, OpenAlex, CrossRef,
  OpenReview, Google Scholar manual checks, venue pages, and web search.
- Label source type when useful, but do not remove records because of source type.
- Sort or cluster by semantic relevance, method similarity, dataset/task match,
  and direct usefulness for the current research question.
- Show uncertainty explicitly when a source is a preprint, short paper, survey,
  weakly related work, or has missing metadata.
- Let the user decide later whether to cite, ignore, or downgrade a paper.

## Compatibility Script

`filter_publications.py` is retained only because existing skills and scripts call
it. It now passes all records through and removes stale source-ranking metadata.
