# LUMIRA — Layered Unit for Monitoring Integrity & Response Analysis

Lumira is an offline-first guardian engine with three layers:
1) **Semantics** — 12-emotions compatible + incongruence checks
2) **Safety** — rule-based self-harm/suicide/self-hate signal detection (non-clinical)
3) **Signals** — overtime trend tracking (JSONL) + 7d downhill alert

## Quick start

### Windows PowerShell
```powershell
# Automated Demo
.\run_lumira_demo.ps1

# Interactive Demo (try your own text)
.\run_interactive_lumira_demo.ps1
```

### Or Python module
```bash
# Automated Demo
python -m lumira demo --data demo_data.json

# Interactive Demo
python interactive_lumira_demo.py
```

## Data & Privacy

- **Offline**, no network calls.
- **JSONL signal store** in `.lumira/`. No PII required.
- **Feature flags** default OFF. Enable via `.env`.

## Safety Disclaimer

Lumira is **not a medical device** and provides non-diagnostic heuristics only.
If you or someone is at risk, seek professional help and local emergency resources.

## Installation

```bash
# Clone repository
git clone https://github.com/louisjanssens/lumira.git
cd lumira

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install lumira
```

## Configuration

Create a `.env` file in your project root:

```bash
# Copy example
cp .env.example .env

# Edit with your preferences
nano .env
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LUMIRA_ENABLED` | `false` | Enable LUMIRA engine |
| `LUMIRA_SEMANTICS_ENABLED` | `false` | Enable semantic analysis |
| `LUMIRA_SAFETY_ENABLED` | `false` | Enable safety detection |
| `LUMIRA_SIGNALS_ENABLED` | `false` | Enable signal storage |
| `LUMIRA_DB_PATH` | `.lumira/signals.jsonl` | Signal store path |

## Usage

### Basic Usage

```python
from lumira import LumiraEngine, TextSample
from datetime import datetime

# Initialize engine
engine = LumiraEngine()

# Create text sample
sample = TextSample(
    id="sample_1",
    ts=datetime.now(),
    source="user_input",
    text="I'm feeling happy but also a bit worried about the future",
    meta={"user_id": "123"}
)

# Process sample
report = engine.process_sample(sample)

# Check results
print(f"Emotions: {[e.name for e in report.emotions]}")
print(f"Risks: {[r.kind for r in report.risks]}")
```

### CLI Usage

```bash
# Run demo
lumira demo --data demo_data.json

# Help
lumira --help
lumira demo --help
```

### PowerShell Demo

```powershell
# Set environment variables and run demo
.\run_lumira_demo.ps1
```

### Generate a report

```powershell
# Generate analysis report
.\run_lumira_report.ps1
```

Or manually:

```bash
# Generate report with custom settings
lumira report --window 7 --store .lumira/signals.jsonl --outdir reports
```

**Note**: Reports are local files; delete anytime.

### Export a clean LUMIRA bundle

```bash
# Create clean LUMIRA bundle
python scripts/package_lumira.py
# outputs:
#  dist/LUMIRA_Engine/
#  dist/LUMIRA_Engine.zip

# Include tests in bundle
python scripts/package_lumira.py --include-tests

# Custom output directory
python scripts/package_lumira.py --output-dir custom_dist

# Via CLI
lumira package
lumira package --include-tests
```

## Architecture

### Semantics Layer
- **12-emotion lexicon** (joy, sadness, anger, fear, surprise, disgust, trust, anticipation, shame, pride, love, contempt)
- **Incongruence detection** (future-tense + negation patterns)
- **Multilingual support** (English + Dutch)

### Safety Layer
- **Rule-based detection** for self-harm, suicide intent, self-hate
- **Non-clinical heuristics** only
- **Escalation signals** for high-risk content
- **Safe excerpts** (max 160 characters)

### Signals Layer
- **JSONL storage** for overtime tracking
- **Trend analysis** with moving averages
- **Downhill alerts** (joy decreasing + risk increasing)
- **No external dependencies**

## API Reference

### Core Classes

#### `LumiraEngine`
Main orchestration engine.

```python
engine = LumiraEngine(
    base_engine=None,           # Optional EFC engine for compatibility
    store_path=None,            # Optional signal store path
    flags=None                  # Optional feature flags dict
)
```

#### `TextSample`
Input text sample for analysis.

```python
sample = TextSample(
    id: str,                    # Unique identifier
    ts: datetime,               # Timestamp
    source: str,                # Source identifier
    text: str,                  # Text content
    meta: Dict[str, Any]        # Metadata
)
```

#### `AnalysisReport`
Complete analysis results.

```python
report = AnalysisReport(
    sample_id: str,             # Sample identifier
    emotions: List[EmotionScore], # Emotion scores
    integrity: List[IntegritySignal], # Integrity signals
    risks: List[RiskFlag]       # Risk flags
)
```

### Methods

#### `process_sample(sample: TextSample) -> AnalysisReport`
Process a text sample through all enabled layers.

#### `analyze_window(days: int = 7) -> Optional[Dict[str, Any]]`
Analyze trends over a time window.

#### `get_signal_stats() -> Dict[str, Any]`
Get statistics about stored signals.

## Migration from EFC

LUMIRA is a complete rewrite of the EFC (Emotional Framework Computing) engine.

### Backward Compatibility
- EFC imports still work (with deprecation warnings)
- Existing EFC engines can be wrapped using `integrate_with_existing_efc()`
- All existing demos remain functional

### Migration Steps
1. Update imports:
   ```python
   # Old
   from efc import EFCEngine
   
   # New
   from lumira import LumiraEngine
   ```

2. Enable features via environment variables:
   ```bash
   export LUMIRA_ENABLED=true
   export LUMIRA_SEMANTICS_ENABLED=true
   export LUMIRA_SAFETY_ENABLED=true
   export LUMIRA_SIGNALS_ENABLED=true
   ```

See [CHANGELOG.md](CHANGELOG.md) for detailed migration notes.

## Development

### Setup
```bash
# Clone repository
git clone https://github.com/louisjanssens/lumira.git
cd lumira

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=lumira --cov-report=html
```

### Code Quality
```bash
# Format code
black lumira/

# Lint code
ruff lumira/

# Type checking
mypy lumira/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [GitHub Wiki](https://github.com/louisjanssens/lumira/wiki)
- **Issues**: [GitHub Issues](https://github.com/louisjanssens/lumira/issues)
- **Discussions**: [GitHub Discussions](https://github.com/louisjanssens/lumira/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and migration notes.
