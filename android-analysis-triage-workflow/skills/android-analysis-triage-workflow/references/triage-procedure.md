# Static APK triage procedure

Choose tools available in the environment; pin their versions or source commits in the evidence record. Consult the [Android API reference](https://developer.android.com/reference) for platform behavior that affects a finding. Use the current [OWASP MASVS](https://mas.owasp.org/MASVS/) control text when making a control-level assessment.

## Intake and provenance

- Prefer a supplied APK set or an app installed from a source the user authorized. If acquiring an installed app, enumerate its base and split paths with `adb shell pm path <package-id>` and copy each file. If using another Play delivery method, record its client/device profile and every returned split. Do not infer publisher identity from a certificate subject or a familiar package name.
- Save each original file read-only in the analysis copy. Record acquisition source and time, package/version, file size, SHA-256, ZIP integrity, and any delivery digest. Verify signatures on every APK, including splits, with `apksigner verify --verbose --print-certs` or an equivalent tool. Check that package/version and signing certificate agree across the set.
- Inventory base and configuration splits by ABI, screen density, and language. A base APK alone may lack native libraries or device-specific resources. Report missing pieces before drawing conclusions about the complete installation.

## Unpack and reconstruct

- Decode the manifest and resources; record requested permissions, components, exported entry points, intent filters, SDK levels, network policy, and backup rules. Keep the original binary manifest as the authority when a decoded representation is ambiguous.
- Enumerate all DEX files. Use a direct DEX decompiler such as JADX for broad coverage. If comparison is useful, convert DEX to class archives and run Fernflower. Preserve the input archives, command lines, logs, failed class lists, and counts of recovered versus unresolved classes. Compare *behaviorally important methods* in both outputs and return to smali/DEX when they conflict. File counts alone are not a quality score.
- Identify embedded JavaScript or Hermes bytecode. Decompile or disassemble with a compatible tool; label the result reconstructed pseudo-source. Trace startup, routes, API client configuration, cache, deep links, push handling, media, and app-specific features from the bundle and Java bridge together.
- Draw two distinct views when helpful: the delivered APK/split structure and a high-level behavior flow. Link each nontrivial flow branch to manifest, Java, smali, bundle, or native evidence. Arrows are reconstructed paths unless runtime traces exist.

## Permissions, native code, and URLs

- Audit **every** manifest permission. For each row record its declaration, code file and method, trigger or component, apparent purpose, and one of: supported app/component use, conditional SDK/device path, or no matching operation found. Distinguish permission checks, actual protected API calls, manifest-only declarations, and transitive SDK code. A missing static match is not proof of non-use.
- Extract `.so` files for every delivered ABI. For each library record hash, ABI, hardening flags, imports, exports, dependencies, JNI symbols, and notable strings. Radare2's `rabin2` JSON modes (`-Ij`, `-ij`, `-Ej`, `-lj`, `-zj`) provide a reproducible baseline; use `r2` cross-references for specific claims. Map `System.loadLibrary`, SoLoader registrations, native method declarations, `JNI_OnLoad`, and dependency edges to the decompiled classes. Label direct matches separately from inferred relationships and unmatched libraries. An import or string is not evidence of reachable app behavior.
- Scan manifest/resources, decoded Java, reconstructed bundle code, and APK entries for HTTP(S)/WS(S) URL-like literals. Save a complete deduplicated inventory with original string, source location, and evidence class. Separate first-party API bases and relative paths from SDK endpoints, fonts, documentation links, placeholders, and DEX-only candidates. Do not claim that a literal was contacted; runtime-composed and server-provided URLs may be absent.

## Security assessment

- For each observation, state the exact artifact and location, the narrowest supported interpretation, and the test needed to resolve uncertainty. Classify a control as supported in part, potential gap, confirmed gap, or not assessed only when the evidence fits that label.
- Treat backup scope, exported components, network pinning, foreground-service types, runtime permission prompts, and third-party SDK defaults as separate questions. Static configuration can support or undermine a control, but cannot establish full runtime compliance.
- Do not execute an untrusted APK just to complete a narrow static request. For a full triage, follow the gated [isolated five-minute dynamic run](dynamic-run.md) and record the tested version, split set, actions, logcat, network evidence, and granted permissions. If a gate fails, keep the static assessment and mark dynamic coverage incomplete.
