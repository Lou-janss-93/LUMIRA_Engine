# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-17

### Added
- **LUMIRA Engine**: Complete rewrite from EFC to LUMIRA architecture
- **Semantic Pipeline**: 12-emotion lexicon with incongruence detection
- **Safety Detector**: Rule-based safety detection for self-harm and suicide intent
- **Signal Store**: Lightweight JSONL-based signal storage and analytics
- **CLI Interface**: Command-line interface with `lumira demo` command
- **PowerShell Demo**: Complete demo script with environment variable setup
- **Backward Compatibility**: EFC compatibility shim with deprecation warnings
- **Feature Flags**: Environment variable-driven module enablement
- **Trend Analysis**: Downhill alert detection for risk/emotion patterns

### Changed
- **Package Name**: `efc-engine` → `lumira`
- **Version**: `2.0.0` → `0.1.0` (fresh start)
- **Description**: Updated to reflect LUMIRA acronym
- **Python Support**: Minimum version raised to 3.10
- **Architecture**: Modular design with separate semantics, safety, and signals modules

### Migration Notes

#### From EFC to LUMIRA

**Breaking Changes:**
- Package name changed from `efc-engine` to `lumira`
- Import paths changed from `efc.*` to `lumira.*`
- Engine class renamed from `EFCEngine` to `LumiraEngine`

**Backward Compatibility:**
- EFC imports still work but show deprecation warnings
- Existing EFC engines can be wrapped using `integrate_with_existing_efc()`
- All existing demos remain functional during transition

**Migration Steps:**
1. Update imports:
   ```python
   # Old
   from efc import EFCEngine
   
   # New
   from lumira import LumiraEngine
   ```

2. Update engine initialization:
   ```python
   # Old
   engine = EFCEngine()
   
   # New
   engine = LumiraEngine()
   ```

3. Enable features via environment variables:
   ```bash
   export LUMIRA_ENABLED=true
   export LUMIRA_SEMANTICS_ENABLED=true
   export LUMIRA_SAFETY_ENABLED=true
   export LUMIRA_SIGNALS_ENABLED=true
   ```

**New Features:**
- Semantic analysis with 12-emotion lexicon
- Safety detection for content filtering
- Signal storage and trend analysis
- CLI interface for easy testing
- PowerShell demo script

### Technical Details

**New Modules:**
- `lumira.semantics`: Emotion classification and incongruence detection
- `lumira.safety`: Rule-based safety and risk assessment
- `lumira.signals`: Signal storage and analytics
- `lumira.engine`: Main orchestration engine
- `lumira.cli`: Command-line interface

**Data Types:**
- `TextSample`: Input text with metadata
- `EmotionScore`: Emotion classification results
- `RiskFlag`: Safety risk assessment
- `IntegritySignal`: Content integrity signals
- `AnalysisReport`: Complete analysis results

**Storage:**
- JSONL format for signal storage
- No external database dependencies
- Optional SQLite support planned

### Deprecated
- EFC package (will be removed in future version)
- Old import paths (use new lumira.* imports)
- Legacy engine classes (use LumiraEngine)

### Security
- Non-clinical safety detection (not for medical use)
- Offline-first design (no external network calls by default)
- Safe content filtering with appropriate disclaimers

---

## [Legacy EFC Versions]

### [2.0.0] - Previous EFC Version
- Last version of the EFC (Emotional Framework Computing) engine
- Maintained for backward compatibility
- Will be deprecated in future releases

---

For more information, see the [README.md](README.md) and [Migration Guide](docs/MIGRATION.md).