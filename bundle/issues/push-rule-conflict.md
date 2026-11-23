---
type: Known Issue
title: Conflicting git push rules between spectra and fleet
description: fusion-spectra's CLAUDE.md says push to origin only, while fusion-fleet's says push to gitea freely and never to origin without confirmation.
resource: repo://fusion-fleet/CLAUDE.md
tags: [spectra, fleet, git, deployment]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Conflict

- [fusion-spectra](/services/fusion-spectra.md): remotes `origin` (GitHub) and `gitea` (local Gitea on minikube) - "push to `origin` only unless asked".[^spectra]
- [fusion-fleet](/services/fusion-fleet.md): every project repo has a `gitea` remote ("safe to push freely") and `origin` ("never push there without explicit per-push confirmation"). Flux only watches `gitea`, so `git push gitea main` is the deploy step.[^fleet]

The two rules point in opposite directions. An agent working in spectra would push to GitHub, which deploys nothing, and would skip the Gitea push that does deploy.

# Resolution

Until the CLAUDE.md files agree, the stricter rule wins: ask before any push, whichever remote. The fleet rule describes how deployment actually works.

[^spectra]: fusion-spectra CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
