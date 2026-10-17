# Codex skills

This repository contains the **Android Analysis Triage Workflow** plugin, version `0.3.0`, by `midnightcomms`. The plugin source is in [`android-analysis-triage-workflow/`](android-analysis-triage-workflow/), with a Codex marketplace descriptor in [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). A ready-to-share archive is available as [`android-analysis-triage-workflow-0.3.0.zip`](android-analysis-triage-workflow-0.3.0.zip).

Keep only the ZIP for the version declared in `android-analysis-triage-workflow/plugin.json`. After updating the plugin source and its matching skill version, run `python3 scripts/package_latest_plugin.py`; it rebuilds the current archive and removes older versioned ZIPs. Commit the ZIP addition and deletions with the source changes. The GitHub workflow runs `python3 scripts/package_latest_plugin.py --check` on pushes and pull requests to reject stale or mismatched archives.

To add the Git-backed marketplace and install the plugin with Codex CLI:

```bash
codex plugin marketplace add midnightcomms/codex-skills --ref main
codex plugin add android-analysis-triage-workflow@midnightcomms-codex-skills
```

Provide the Android package name when invoking the skill:

> Analyze this APK for package `com.example.app` using `$android-analysis-triage-workflow`.

The workflow checks the package name against the APK manifest, then guides evidence-led static analysis of code, permissions, native libraries, and URL literals. A full triage also selects the latest stable Google system image for the manifest target API, boots Android inside a disposable analysis VM with app egress blocked, starts a Tor/Privoxy Docker gateway after boot verification, checks that traffic fails closed, and observes the app for five minutes. It snapshots writable Android files before installation and after observation, hashes and lists created, modified, or deleted files, and looks up the APK and created-file hashes in VirusTotal. The handoff includes image hashes, runtime logs, the full file-change inventory, and VirusTotal results.

The skill does not bundle the command-line tools or a VM. VirusTotal enrichment requires the separately connected VirusTotal plugin and uses existing-report lookups only; it never uploads files for this step. See the [toolchain and fallback matrix](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/toolchain.md), [isolated dynamic runbook](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/dynamic-run.md), and [file-change/lookup procedure](android-analysis-triage-workflow/skills/android-analysis-triage-workflow/references/filesystem-and-virustotal.md) before use. If isolation or routing cannot be verified, the skill records the dynamic phase as blocked and does not install the app.
