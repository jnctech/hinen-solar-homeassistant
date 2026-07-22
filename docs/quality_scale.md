# Quality-scale roadmap

Progress toward the Home Assistant integration quality scale. This is a roadmap —
no tier is claimed in `manifest.json` until every rule in that tier is `done`.
(Kept as docs rather than `custom_components/hinen/quality_scale.yaml` so hassfest
doesn't require a premature `quality_scale` manifest claim.)

## Bronze
- ✅ appropriate-polling, common-modules, config-flow, config-flow-test-coverage,
  dependency-transparency, docs-high-level-description, docs-installation-instructions,
  entity-event-setup, entity-unique-id, test-before-configure, test-before-setup,
  unique-config-entry
- ✅ runtime-data — coordinator lives on `entry.runtime_data` via a typed `HinenConfigEntry`
- ✅ brands — self-hosted `brand/icon.png` + `icon@2x.png`. From HA 2026.3 custom
  integrations serve their own brand images locally, and `home-assistant/brands`
  no longer accepts custom-integration icons.
- ✅ docs-removal-instructions
- ⬜ **has-entity-name** — entities use explicit names; migrate to `has_entity_name` +
  translations. **Deferred on purpose:** this rewrites entity_ids and breaks existing
  history/dashboards, so it must be coordinated with the entity-naming work.
- ➖ action-setup, docs-actions — exempt (no service actions)

## Silver
- ✅ action-exceptions (control writes raise), config-entry-unloading, entity-unavailable,
  integration-owner, parallel-updates (0 for read-only platforms, 1 for the control
  platforms so writes serialise), reauthentication-flow, test-coverage (90%)
- ⬜ docs-configuration-parameters, docs-installation-parameters, log-when-unavailable

## Gold
- ✅ devices, entity-category, entity-device-class
- ⬜ diagnostics, dynamic-devices, entity-disabled-by-default, entity-translations,
  exception-translations, icon-translations, reconfiguration-flow, repair-issues,
  stale-devices, and the docs-* rules
- ➖ discovery, discovery-update-info — exempt (cloud-polling)

## Platinum
- ✅ inject-websession
- ⬜ async-dependency (would need a published API library), strict-typing
