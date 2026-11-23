---
type: Playbook
title: Local DNS for *.fusion.local
description: A host-side dnsmasq on 127.0.0.1:5353 resolves the *.fusion.local wildcard to the minikube IP via systemd-resolved, self-healing every 60s; only dev.fusion.local stays in /etc/hosts.
tags: [operations, minikube, dns, spectra, fleet]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Setup

- `/etc/dnsmasq-fusion.conf`: `address=/fusion.local/<minikube-ip>`, listening on `127.0.0.1:5353` (so it doesn't collide with the systemd-resolved stub). Runs as `dnsmasq-fusion.service`.[^spectra]
- `/etc/systemd/resolved.conf.d/fusion-local.conf`: `Domains=~fusion.local` routes only that domain to dnsmasq.
- `fusion-dns-sync.timer` (60s) rewrites the config when `minikube ip` changes, e.g. after `minikube delete && start`.

# Rules

- **Only** `dev.fusion.local` → `127.0.0.1` (Vite dev server) belongs in `/etc/hosts`. Any other `*.fusion.local` entry there silently shadows DNS (`files` comes before `dns` in nsswitch).[^spectra]
- Host names: `<service>.fusion.local` for the manual `fusion` namespace, `<service>-<instance>.fusion.local` for Flux instances (`spectra-a`, `bff-b`, ...).[^fleet]
- A spectra instance with its own host needs three matching bff overrides, otherwise login loops: `config.oidcBypassBaseUrl`, `config.corsOrigins`, `config.postLoginRedirectUrl`. Restart the bff afterwards, because env vars are read at startup.[^fleet]

[^spectra]: fusion-spectra CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
