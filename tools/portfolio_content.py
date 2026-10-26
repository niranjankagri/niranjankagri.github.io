"""Editorial summaries; results and evidence always come from the project catalogue."""
HOME_PROJECT_IDS = (
    'enterprise-test-automation-framework',
    'automation-coverage-quality-intelligence',
    'ai-assisted-test-automation',
)
FLAGSHIP_STORIES = {
    'enterprise-test-automation-framework': {
        'problem': 'Verify the same demo-shop business flows across UI, API and database layers.',
        'decision': 'Separate business assertions from browser, HTTP and SQL access; isolate test data and retain failure evidence.',
        'limitation': 'Repository demo application; these results do not establish production customer impact.',
    },
    'automation-coverage-quality-intelligence': {
        'problem': 'Results spread across repositories make release readiness difficult to inspect.',
        'decision': 'Normalize existing result files, retain execution context, and keep collected CI evidence separate from the synthetic requirement catalogue.',
        'limitation': 'Execution evidence and sample requirement coverage have different sources; a pass rate alone cannot establish release readiness.',
    },
    'ai-assisted-test-automation': {
        'problem': 'Generated tests need validation and accountable review before they can become trusted checks.',
        'decision': 'Gate drafts through rules, compilation and repeated execution, then require a named human reviewer. Label hand-written samples separately from live model outputs.',
        'limitation': 'Sample and replay evidence does not establish live Claude generation quality or triage accuracy.',
    },
}
