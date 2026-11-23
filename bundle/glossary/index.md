# Glossary

## Concepts

* [Blueprint](blueprint.md) - spectra's UI name for weave templates - Step Blueprints are job/service templates, Run Blueprints are chains; Deploy steps are shown as Service.
* [Build type](build-type.md) - forge's three build flavours - requirements build, git build and app build - which differ in input, API and artifact prefix.
* [Code source](code-source.md) - weave's codeSource mechanism - load an index artifact by tag into a pod via the code-loader init container and follow tag moves with rolling restarts.
* [Deploy step](deploy-step.md) - A WeaveChain step with stepKind Deploy that creates or rolling-updates a long-lived Deployment, Service and Ingress owned by the chain.
* [Ledger](ledger.md) - fusion-wizard's ref-counted record of every upstream object it touches, which makes provisioning idempotent and rollback exact.
* [Owner group](owner-group.md) - Team that owns platform resources; resolved by the BFF at login and forwarded as X-User-Groups, with service-side enforcement planned.
* [Showroom](showroom.md) - Optional demo tour shipped in the fusion-weave chart - Tier 1 self-contained chains, Tier 2 real code-source apps built from fusion-testcases.
* [Simple and Expert mode](simple-expert-mode.md) - spectra's two audiences - common users see wizards and runs, experts with the ui:expert permission see the full Weave, Forge and Index UI.
* [venvpack](venvpack.md) - A packed Python virtual environment (.tar.gz with top-level venv/) produced by forge, stored in index and unpacked by the runner.
* [weave vs flux](weave-vs-flux.md) - fusion-weave is the job scheduler, developed in the local directory fusion-flux; "Flux" alone means the FluxCD GitOps tool used by fusion-fleet.
