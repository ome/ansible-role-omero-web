# Changes in Version 2

## Removed variables
- `omero_web_upgrade`: This variable is now an internal variable.
  Upgrades are automatically executed depending on the value of `omero_web_release` which can be set to `present`, `latest` or a fixed version.
