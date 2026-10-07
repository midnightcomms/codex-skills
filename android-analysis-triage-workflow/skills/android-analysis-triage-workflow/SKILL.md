---
name: android-analysis-triage-workflow
description: Triage Android APKs or split APK sets for a user-supplied package name with static code, manifest, native-library, URL, and permission analysis, then produce an evidence-led analyst handoff. Use for APK reverse-engineering or security triage requests, not ordinary Android app development.
metadata:
  author: midnightcomms
  version: 0.1.0
---

# Android Analysis Triage Workflow

Use the parts of this workflow that answer the request. Keep the original binaries and tool logs as evidence, and identify the exact APK version and split set behind every conclusion. Do not treat a decompiler's reconstructed source as authoritative when bytecode or the manifest disagrees.

## Required starting input

Require the user to provide the Android package name (application ID) for the current case before acquiring or analyzing an APK. A quoted or unquoted name such as `com.example.app` satisfies this requirement. If it is missing or is only a placeholder, ask for the package name and wait; do not infer it from a file name, URL, or APK manifest. When the APK is available, compare its manifest package name and any split package names with the requested name. If they differ, stop and ask which package or artifact the user intends to analyze. Record both the requested and observed names in the handoff.

Example invocation: "Analyze this APK for package `com.example.app` using `$android-analysis-triage-workflow`."

## Tool preflight

This skill supplies instructions, not the executables. Before analysis, check the tools needed for the requested scope: an archive reader and hashing tool for every APK; Android SDK Build Tools and a manifest decoder for package/signature findings; JADX for DEX decompilation. Add `adb` for device acquisition, dex2jar + Fernflower for a second Java reconstruction, a bundle-version-compatible Hermes tool when Hermes is present, and radare2 for native-library analysis. See the [toolchain and fallback matrix](references/toolchain.md) for commands, setup boundaries, and what to mark unverified when a tool is missing. Record tool versions and source commits; do not silently skip a requested phase.

1. Establish the delivered file set, provenance, hashes, signature results, package/version, device configuration, and missing splits. Record what verification establishes and what it does not.
2. Inventory manifests, DEX files, resources, JavaScript bundles, and native libraries. Decompile relevant DEX and bundle code; retain logs, failures, and unresolved methods. Compare a second decompiler when a conclusion depends on incomplete output.
3. Reconstruct startup, routing, content requests, media, notifications, and other app-specific paths. Map every requested manifest permission to exact code or component evidence. Analyze native libraries against Java loads, JNI, and native dependencies. Inventory statically recoverable URL literals with their locations.
4. Review security controls against the current Android documentation and, when requested, the current OWASP MASVS text. Separate supported evidence, plausible gaps, and matters requiring runtime or server-side validation.
5. Produce a source-linked handoff with an APK-structure view, a high-level application flow, permission and native-library tables, URL inventory, uncertainty notes, and concrete next checks. Include workflow timing and token counts only when records are available.

Read [the triage procedure](references/triage-procedure.md) when performing acquisition, reconstruction, or code-to-permission/native mapping. Read [the public handoff guide](references/public-handoff.md) when writing a report or preparing any artifact for public sharing.

Static evidence establishes what is packaged and what paths are visible. It does not show that a path executed, a permission was granted, a URL was contacted, or a control passed end-to-end. If a task asks for a narrower answer, report the supported portion without implying that the full workflow was completed.
