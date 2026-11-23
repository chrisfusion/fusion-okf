# Custom resources

## Concepts

* [CIBuild](cibuild.md) - forge's build request (build.fusion-platform.io/v1alpha1) that the forge operator turns into a ConfigMap plus builder Job.
* [GitWatcher](gitwatcher.md) - forge resource (build.fusion-platform.io/v1alpha1, short name gw) that polls a git repo and builds whenever the declared version changes.
* [WeaveApp](weaveapp.md) - Single-resource fast lane (weave.fusion-platform.io/v1alpha1, short name fa) that owns either a service or a set of job entrypoints, without templates, chains or runs.
* [WeaveChain](weavechain.md) - DAG of Job and Deploy steps (weave.fusion-platform.io/v1alpha1, short name fc) with failure, concurrency, shared-storage and auth settings.
* [WeaveJobTemplate](weavejobtemplate.md) - Reusable batch-job blueprint (weave.fusion-platform.io/v1alpha1, short name fjt) referenced by Job steps of a WeaveChain.
* [WeaveRun](weaverun.md) - One execution of a WeaveChain (weave.fusion-platform.io/v1alpha1, short name fr) with per-step status, overrides and deploy bookkeeping.
* [WeaveServiceTemplate](weaveservicetemplate.md) - Long-running service blueprint (weave.fusion-platform.io/v1alpha1, short name wst) used by Deploy steps; becomes a Deployment, Service and optional Ingress.
* [WeaveTrigger](weavetrigger.md) - Activation source for a WeaveChain (weave.fusion-platform.io/v1alpha1, short name ft) - OnDemand, Cron, Webhook, BatchCron or Kafka - that creates WeaveRuns.
* [WizardDefinition](wizarddefinition.md) - Instance-agnostic provisioning recipe (wizard.fusion-platform.io/v1alpha1, short name wdef) with typed parameters and an ordered subset of wizard steps.
* [WizardResource](wizardresource.md) - Ledger entry (wizard.fusion-platform.io/v1alpha1, short name wres) for one upstream object in forge, index or weave, ref-counted across wizard runs.
* [WizardRun](wizardrun.md) - One execution of a WizardDefinition (wizard.fusion-platform.io/v1alpha1, short name wrun) with parameters, definition snapshot, desired state and per-step status.
