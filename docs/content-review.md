# Portfolio and CV consistency review

Reviewed on 21 October 2026 against the downloadable PDF, the shared project records and the linked workflow evidence.

## Confirmed consistent

- The PDF and site agree on 12+ years, the 84% release test-scope automation figure, four QA engineers led, employment dates, role transitions, education, languages and European work-authorisation wording.
- The 84% explanation on the site now explicitly says that all multi-user performance and upgrade suites were automated and ready to run. It describes automation coverage, not product quality.
- The Enterprise case study and home card use the verified 21 October 2026 nightly workflow run. They report each environment's test executions separately and link to that run.

## Needs a decision before changing the PDF

- The PDF's portfolio section says the Enterprise project has 169 automated tests, including 57 API and 53 UI tests. The current nightly run records 233 executions in Chrome and 174 each in Firefox, Edge and Selenium Grid. The workflow logs report execution counts by job; they do not provide a directly comparable project-wide inventory with the same grouping as the PDF. The PDF figure is therefore left unchanged pending confirmation of whether it describes unique tests, methods or a previous suite version.
- The PDF lists five older portfolio examples, while the site now features six different projects. These are selections rather than contradictory claims, but the PDF could be refreshed to use the current featured set in a later content pass.

## External link check

- All 25 project repositories are public, and all 22 configured workflow files resolve in their repositories.
- The Quality Intelligence live dashboard smoke workflow passed on 21 October 2026, but the verifier could not fetch the Render URL directly. Keep the link tied to the dated smoke evidence.
- LinkedIn rejected the direct fetch with status 999, so that destination could not be independently checked in this pass. The address matches the profile link in the CV.
- A scheduled metric refresh was not added: the projects use different report formats and test-count units, so a single automated parser could mix unique tests with per-browser executions. Evidence stays dated in the shared data, and the build has no external-service dependency. Records older than 30 days are labelled for rechecking when the site is rebuilt.

No replacement Enterprise total has been inferred from the per-environment run counts.
