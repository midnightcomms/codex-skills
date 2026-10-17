# Codex skills

This repository contains the **Android Analysis Triage Workflow** plugin, version `0.2.0`, by `midnightcomms`. The plugin source is in [`android-analysis-triage-workflow/`](android-analysis-triage-workflow/), with a Codex marketplace descriptor in [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). A ready-to-share archive is available as [`android-analysis-triage-workflow-0.2.0.zip`](android-analysis-triage-workflow-0.2.0.zip).

To add the Git-backed marketplace and install the plugin with Codex CLI:

```bash
codex plugin marketplace add midnightcomms/codex-skills --ref main
codex plugin add android-analysis-triage-workflow@midnightcomms-codex-skills
```

Provide the Android package name when invoking the skill:

> Analyze this APK for package `com.example.app` using `$android-analysis-triage-workflow`.

The workflow checks the package name against the APK manifest, then guides evidence-led static analysis of code, permissions, native libraries, and URL literals. A full triage also selects the latest stable Google system image for the manifest target API, boots Android inside a disposable analysis VM with app egress blocked, starts a Tor/Privoxy Docker gateway after boot verification, checks that traffic fails closed, and observes the app for five minutes. The handoff includes image hashes and linked runtime logs.

The skill does not bundle the command-line tools or a VM. See the [toolchain and fallback matrix](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/toolchain.md) and [isolated dynamic runbook](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/dynamic-run.md) before use. If isolation or routing cannot be verified, the skill records the dynamic phase as blocked and does not install the app.
