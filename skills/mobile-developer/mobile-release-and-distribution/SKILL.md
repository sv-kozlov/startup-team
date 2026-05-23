---
name: mobile-release-and-distribution
description: Use when preparing a mobile release — configuring app signing, build variants, staged rollout, feature flags, submitting to App Store or Google Play, managing TestFlight or internal tracks, defining a hotfix process, or coordinating store review timelines. Covers the release train model and rollback strategy.
family: method
profile_level: Senior+
---

# Mobile Release and Distribution

## Purpose

Ship mobile releases predictably, safely, and recoverably. Release is a pipeline: signing → build → internal test → staged rollout → full production → post-launch monitoring. Feature flags decouple code shipping from feature visibility. Staged rollout limits the blast radius of regressions. Rollback has a defined path before the first release.

## Use When

- Preparing a release candidate: signing, build variants, and release notes.
- Configuring staged rollout in Google Play (1% → 5% → 25% → 100%) or App Store phased release.
- Setting up TestFlight (iOS) or internal/closed testing track (Google Play).
- Defining or activating feature flags for a risky feature.
- Coordinating App Store review submission timing (24–72 h review window).
- Defining the hotfix process (expedited review, rollback, emergency release).
- Planning the release train calendar for a team with multiple feature streams.

## Do Not Use When

- The task is about CI/CD pipeline infrastructure ownership → handoff to `devops-sre`.
- The task is about crash analytics after the release → `mobile-observability`.
- The task is about QA strategy for the release → handoff to `qa-engineer`.
- The task is about app performance profiling → `mobile-performance-and-resources`.

## Inputs

- Current build configuration: Gradle build types / Xcode configurations.
- Signing certificates and provisioning profiles (Android: keystore; iOS: distribution certificate + provisioning profile).
- Feature flags system in use: Firebase Remote Config, LaunchDarkly, in-house.
- Release calendar and store account access.

## Workflow

1. **Version and changelog**: bump versionCode/CFBundleVersion monotonically. Update versionName/CFBundleShortVersionString using semantic versioning. Write release notes per locale.
2. **Build signing**: Android — sign AAB with a release keystore (never commit the keystore; use CI secrets). iOS — use Xcode automatic signing or Fastlane `match` for team-managed certificates.
3. **Build variants**: Android — release, debug, staging build types with separate applicationId suffixes. iOS — schemes per environment (dev / staging / prod) with different Bundle IDs.
4. **Internal testing**: distribute to internal track (Google Play) or TestFlight internal group before any external exposure. Gate on crash-free rate > 99.5% and no P1 issues in 24 h.
5. **Staged rollout**: Google Play — set rollout percentage; monitor crash-free rate and ANR rate in Play Console. App Store — use phased release (7-day, up to 100%). If crash-free rate drops > 0.5 pp relative, pause rollout.
6. **Feature flags**: wrap risky features in a flag evaluated at runtime. Default value must be safe (feature off). Validate that the flag evaluation happens before the feature code path executes.
7. **Store review**: submit 3–5 business days before the desired release date. For iOS emergency, use the expedited review request (one per 90 days). For Android, expedited review is not available — plan accordingly.
8. **Hotfix**: branch from the release tag; fix the regression; bump build number; fast-track internal → full production without staged rollout for critical safety fixes.

## Outputs

- Signed AAB / IPA ready for upload.
- Store listing update (release notes, screenshots if changed).
- Staged rollout configuration with monitoring thresholds.
- Feature flag configuration with rollback value.
- Release checklist (signed off by mobile developer and QA).

## Named Patterns

### Good — Fastlane match for iOS certificate management
```ruby
# Fastfile
lane :beta do
  match(type: "appstore", readonly: true)
  build_app(scheme: "MyApp-Prod", configuration: "Release")
  upload_to_testflight(skip_waiting_for_build_processing: true)
end
```
Certificates stored in a private git repo; rotated in one place; all team members use the same signing identity.

### Bad — Developer certificate committed to the repo
```
# Committed: MyApp.p12, MyApp.mobileprovision
# Password in README: "use 'dev123' to import"
```
Certificate exposed; password in plaintext; rotation requires manual steps on every machine.

### Good — Feature flag checked before code path
```kotlin
// Android: flag checked at the entry point of the feature, not deep inside
@Composable
fun NavHost(remoteConfig: RemoteConfigService) {
    val isNewCheckoutEnabled by remoteConfig.getBooleanAsState("new_checkout", default = false)
    if (isNewCheckoutEnabled) NewCheckoutScreen() else LegacyCheckoutScreen()
}
```

### Bad — Feature flag checked inside business logic
```kotlin
class CheckoutViewModel(private val remoteConfig: RemoteConfigService) : ViewModel() {
    fun calculateTotal(): Money {
        return if (remoteConfig.getBoolean("new_checkout")) { // flag in domain logic
            newPricingEngine.calculate()
        } else { legacyPricingEngine.calculate() }
    }
}
```
Flag in domain logic makes both code paths entangled; harder to remove when fully rolled out.

### Good — Staged rollout pause criterion
```
Release Day 1:  1% → watch crash-free, ANR rate, ratings for 4 h
Release Day 2:  5% → watch for 24 h
Release Day 4: 25% → watch for 24 h
Release Day 6: 100%

Pause trigger: crash-free rate drops by > 0.5 pp vs previous version baseline
```

### Bad — Full rollout on day 1
Deploying 100% immediately: a regression in edge cases (specific device/OS) reaches all users before crash analytics surface the issue.

## Boundaries

- Owns release preparation, signing, store submission, staged rollout configuration, and feature flag coordination.
- Does not own CI/CD pipeline infrastructure (Bitrise, Fastlane runner, GitHub Actions setup) → `devops-sre`.
- Does not own QA test strategy or release sign-off → `qa-engineer`.
- Does not own post-release crash analysis → `mobile-observability`.

## Sources

### Priority 1 — Platform canon
- App Store Review Guidelines — https://developer.apple.com/app-store/review/guidelines/
- App Store phased release — https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/
- Google Play staged rollouts — https://support.google.com/googleplay/android-developer/answer/6346149
- Google Play internal testing — https://support.google.com/googleplay/android-developer/answer/9845334
- Android app signing — https://developer.android.com/studio/publish/app-signing

### Priority 2 — Tools and standards
- Fastlane — https://fastlane.tools/
- Firebase Remote Config — https://firebase.google.com/docs/remote-config
- The Twelve-Factor App (config) — https://12factor.net/config

### Priority 3 — Community
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- CI/CD pipeline infrastructure → `devops-sre`.
- QA test strategy and release sign-off → `qa-engineer`.
- Post-release crash analysis → `mobile-observability`.
- Product decision on rollout pace → `product-manager` / `product-owner`.
