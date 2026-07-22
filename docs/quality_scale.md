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
- ⬜ **has-entity-name** — entities use explicit names; migrate to `has_entity_name` + translations
- ⬜ **runtime-data** — coordinator in `hass.data`; migrate to `entry.runtime_data`
- ⬜ **brands** — submit logo to `home-assistant/brands`
- ⬜ docs-removal-instructions
- ➖ action-setup, docs-actions — exempt (no service actions)

## Silver
- ✅ action-exceptions (control writes raise), config-entry-unloading, entity-unavailable,
  integration-owner, reauthentication-flow, test-coverage (90%)
- ⬜ docs-configuration-parameters, docs-installation-parameters, log-when-unavailable,
  parallel-updates

## Gold
- ✅ devices, entity-category, entity-device-class
- ⬜ diagnostics, dynamic-devices, entity-disabled-by-default, entity-translations,
  exception-translations, icon-translations, reconfiguration-flow, repair-issues,
  stale-devices, and the docs-* rules
- ➖ discovery, discovery-update-info — exempt (cloud-polling)

## Platinum
- ✅ inject-websession
- ⬜ async-dependency (would need a published API library), strict-typing
