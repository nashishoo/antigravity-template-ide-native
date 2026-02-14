# Documentation Reorganization Script for v2.0-alpha
# Run this before pushing to GitHub

Write-Host "Creating new directory structure..."
New-Item -ItemType Directory -Force -Path docs/v2
New-Item -ItemType Directory -Force -Path docs/es/v2
New-Item -ItemType Directory -Force -Path scripts

Write-Host "Moving v2 English docs..."
if (Test-Path README_V2_STATUS.md) { Move-Item README_V2_STATUS.md docs/v2/STATUS.md }
if (Test-Path CHANGELOG_v2.0-alpha.1.md) { Move-Item CHANGELOG_v2.0-alpha.1.md docs/v2/CHANGELOG.md }
if (Test-Path RELEASE_NOTES_v2.0-alpha.1.md) { Move-Item RELEASE_NOTES_v2.0-alpha.1.md docs/v2/RELEASE_NOTES.md }
if (Test-Path MIGRATION_GUIDE_v1_to_v2-alpha.md) { Move-Item MIGRATION_GUIDE_v1_to_v2-alpha.md docs/v2/MIGRATION_GUIDE.md }
if (Test-Path CONTRIBUTING_v2.md) { Move-Item CONTRIBUTING_v2.md docs/v2/CONTRIBUTING.md }

Write-Host "Moving v2 Spanish docs..."
if (Test-Path README_V2_STATUS_ES.md) { Move-Item README_V2_STATUS_ES.md docs/es/v2/STATUS.md }
if (Test-Path CHANGELOG_v2.0-alpha.1_ES.md) { Move-Item CHANGELOG_v2.0-alpha.1_ES.md docs/es/v2/CHANGELOG.md }
if (Test-Path RELEASE_NOTES_v2.0-alpha.1_ES.md) { Move-Item RELEASE_NOTES_v2.0-alpha.1_ES.md docs/es/v2/RELEASE_NOTES.md }
if (Test-Path MIGRATION_GUIDE_v1_to_v2-alpha_ES.md) { Move-Item MIGRATION_GUIDE_v1_to_v2-alpha_ES.md docs/es/v2/MIGRATION_GUIDE.md }
if (Test-Path CONTRIBUTING_v2_ES.md) { Move-Item CONTRIBUTING_v2_ES.md docs/es/v2/CONTRIBUTING.md }

if (Test-Path scripts/reorganize_docs.sh) { Remove-Item scripts/reorganize_docs.sh }

Write-Host "✅ Reorganization complete!"
Write-Host "Files moved to docs/v2/ and docs/es/v2/"
Write-Host "Root directory is now clean."
