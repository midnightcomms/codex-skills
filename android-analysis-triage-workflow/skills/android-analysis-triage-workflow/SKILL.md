---
name: android-analysis-triage-workflow
description: Triage Android APKs or split APK sets for a user-supplied package name with static and isolated dynamic analysis, then produce an evidence-led analyst handoff. Use for APK reverse-engineering or security triage requests, not ordinary Android app development.
metadata:
  author: midnightcomms
  version: 0.3.0
---

# Android Analysis Triage Workflow

Use the parts of this workflow that answer the request. A full triage includes the controlled five-minute dynamic run below for every accepted application; a narrower static request need not start a device. Keep the original binaries and tool logs as evidence, and identify the exact APK version and split set behind every conclusion. Do not treat a decompiler's reconstructed source as authoritative when bytecode or the manifest disagrees.

## Required starting input

Require the user to provide the Android package name (application ID) for the current case before acquiring or analyzing an APK. A quoted or unquoted name such as `com.example.app` satisfies this requirement. If it is missing or is only a placeholder, ask for the package name and wait; do not infer it from a file name, URL, or APK manifest. When the APK is available, compare its manifest package name and any split package names with the requested name. If they differ, stop and ask which package or artifact the user intends to analyze. Record both the requested and observed names in the handoff.

Example invocation: "Analyze this APK for package `com.example.app` using `$android-analysis-triage-workflow`."

## Tool preflight

This skill supplies instructions, not the executables or an isolation environment. Before analysis, check the tools needed for the requested scope: an archive reader and hashing tool for every APK; Android SDK Build Tools and a manifest decoder for package/signature findings; JADX for DEX decompilation. Add `adb` for device acquisition, dex2jar + Fernflower for a second Java reconstruction, a compatible Hermes tool when Hermes is present, and radare2 for native-library analysis. A full triage also needs a disposable VM, Google Android SDK image/emulator tools, guest-side Docker, Tor, Privoxy, and enforceable guest network controls. See the [toolchain and fallback matrix](references/toolchain.md). Record tool versions and source commits; do not silently skip a requested phase.

1. Establish the delivered file set, provenance, hashes, signature results, package/version, device configuration, and missing splits. Record what verification establishes and what it does not.
2. Inventory manifests, DEX files, resources, JavaScript bundles, and native libraries. Decompile relevant DEX and bundle code; retain logs, failures, and unresolved methods. Compare a second decompiler when a conclusion depends on incomplete output.
3. Reconstruct startup, routing, content requests, media, notifications, and other app-specific paths. Map every requested manifest permission to exact code or component evidence. Analyze native libraries against Java loads, JNI, and native dependencies. Inventory statically recoverable URL literals with their locations.
4. For a full triage, read the [dynamic run procedure](references/dynamic-run.md). Select the latest stable Google system-image revision for the manifest target API level that can run the delivered APK set; record the exact SDK package, revision, image hashes, and compatibility decision. Boot a fresh Android emulator **inside a disposable analysis VM** with Android egress denied from the outset. Verify boot and runtime API/build before changing network access.
5. Only after boot verification, start a pinned Tor-plus-Privoxy Docker gateway inside that VM. Enforce and test fail-closed Android egress through the gateway, including DNS, IPv6, and non-TCP paths. Do not rely on an Android HTTP proxy setting alone. If the isolation or routing checks fail, do not install the APK; record the dynamic phase as blocked.
6. Capture a complete, read-only baseline of the AVD's writable files immediately before installation. Install the complete matched APK/split set, launch the app, and observe it for 300 seconds from confirmed launch. Capture a matching final snapshot, logcat/crash/ANR evidence, gateway logs, network-denial evidence, timestamps, and hashes. If it crashes or never launches, record actual observed duration instead of claiming a completed five-minute run. Use the [filesystem and VirusTotal procedure](references/filesystem-and-virustotal.md) to list and hash every created, modified, or deleted file in the captured scope; clearly label inaccessible paths and background Android changes.
7. Query existing VirusTotal reports for the APK SHA-256 and every distinct SHA-256 of a newly created regular file. Use the connected VirusTotal plugin's `get_file_report` lookup only; do not submit files or start scans. Record each lookup result, including missing and quota-limited results, in the handoff. If the plugin is unavailable, label this enrichment incomplete without inventing results.
8. Review security controls against current Android documentation and, when requested, OWASP MASVS. Produce a source-linked handoff with APK structure, application flow, permission/native-library tables, URL inventory, a dynamic-run section with log links and image identity, the complete file-change inventory and VirusTotal results, uncertainty notes, and concrete next checks. Include workflow timing and token counts only when records are available.

Read [the triage procedure](references/triage-procedure.md) when performing acquisition, reconstruction, or code-to-permission/native mapping. Read [the public handoff guide](references/public-handoff.md) when writing a report or preparing any artifact for public sharing.

Static evidence establishes what is packaged and what paths are visible. Runtime evidence applies only to the recorded image, installation, actions, and observation window. If a full dynamic run cannot be completed, state the exact gate that failed; do not imply that the full workflow was completed. A VM and Docker reduce exposure but cannot prove that a guest has zero interaction with its host.
