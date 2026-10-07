# Codex skills

This repository contains the **Android Analysis Triage Workflow** plugin, version `0.1.0`, by `midnightcomms`. The plugin source is in [`android-analysis-triage-workflow/`](android-analysis-triage-workflow/), with a Codex marketplace descriptor in [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). A ready-to-share archive is available as [`android-analysis-triage-workflow-0.1.0.zip`](android-analysis-triage-workflow-0.1.0.zip).

To add the Git-backed marketplace and install the plugin with Codex CLI:

```bash
codex plugin marketplace add midnightcomms/codex-skills --ref main
codex plugin add android-analysis-triage-workflow@midnightcomms-codex-skills
```

Provide the Android package name when invoking the skill:

> Analyze this APK for package `com.example.app` using `$android-analysis-triage-workflow`.

The workflow checks the package name against the APK manifest, then guides evidence-led static analysis of code, permissions, native libraries, and URL literals. It does not bundle the command-line tools; see the [toolchain and fallback matrix](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/toolchain.md) before use.
