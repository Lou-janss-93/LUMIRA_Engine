"""
LUMIRA CLI

Command-line interface for the LUMIRA framework.
"""

import json
import argparse
import sys
import os
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from .engine import LumiraEngine
from .types import TextSample
from .reporting import make_summary, render_markdown, render_json
import subprocess
import sys


def load_demo_data(data_path: str) -> List[Dict[str, Any]]:
    """
    Load demo data from JSON file.
    
    Args:
        data_path: Path to demo data file
        
    Returns:
        List of demo samples
    """
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'samples' in data:
            return data['samples']
        else:
            print(f"Error: Invalid data format in {data_path}")
            return []
            
    except FileNotFoundError:
        print(f"Error: Demo data file not found: {data_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {data_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading demo data: {e}")
        return []


def create_text_sample(sample_data: Any, index: int) -> TextSample:
    """
    Create TextSample from demo data.
    
    Args:
        sample_data: Sample data (string or dictionary)
        index: Sample index
        
    Returns:
        TextSample object
    """
    if isinstance(sample_data, str):
        # Simple string format
        return TextSample(
            id=f'demo_{index+1:03d}',
            ts=datetime(2024, 1, 15 + index//2, 9 + index%2 * 10, 30 * (index%2)),
            source='demo',
            text=sample_data,
            meta={'demo': True}
        )
    else:
        # Dictionary format
        return TextSample(
            id=sample_data.get('id', f'demo_{index+1:03d}'),
            ts=datetime.fromisoformat(sample_data.get('timestamp', datetime.now().isoformat())),
            source=sample_data.get('source', 'demo'),
            text=sample_data.get('text', ''),
            meta=sample_data.get('meta', {})
        )


def print_analysis_report(report, sample_id: str, day: str):
    """
    Print analysis report in a formatted way.
    
    Args:
        report: AnalysisReport object
        sample_id: Sample identifier
        day: Day identifier
    """
    print(f"\n--- Sample {sample_id} ({day}) ---")
    print(f"Text: {report.sample_id}")
    print()
    
    # Print emotions with explanation
    if report.emotions:
        print("🧠 SEMANTICS - Emotions detected:")
        for emotion in report.emotions[:3]:  # Top 3 emotions
            print(f"  - {emotion.name}: {emotion.score:.3f}")
    else:
        print("🧠 SEMANTICS - No emotions detected")
    
    # Print risks with explanation
    if report.risks:
        print("🛡️ SAFETY - Risks detected:")
        for risk in report.risks:
            print(f"  - {risk.kind} ({risk.level}): {risk.confidence:.3f}")
            if hasattr(risk, 'excerpt') and risk.excerpt:
                print(f"    Excerpt: {risk.excerpt}")
    else:
        print("🛡️ SAFETY - No risks detected")
    
    # Print integrity signals with explanation
    if report.integrity:
        print("🔍 INTEGRITY - Signals detected:")
        for signal in report.integrity:
            print(f"  - {signal.level}: {signal.reason}")
    else:
        print("🔍 INTEGRITY - No signals detected")


def print_integrated_analysis_report(report, sample_id: str, day: str, text: str, efc_result=None):
    """
    Print integrated analysis report showing EFC + LUMIRA results.
    
    Args:
        report: AnalysisReport object
        sample_id: Sample identifier
        day: Day identifier
        text: Original text sample
        efc_result: EFC pipeline result (optional)
    """
    print(f"\n--- Sample {sample_id} ({day}) ---")
    print(f"Text: {text}")
    print()
    
    # Show EFC + LUMIRA integration
    print("🔧 EFC + LUMIRA INTEGRATION:")
    print("  EFC Core: Original emotional framework computing")
    print("  LUMIRA Extensions: Semantics + Safety + Signals")
    print()
    
    # Show EFC results if available
    if efc_result:
        print("🔧 EFC CORE ANALYSIS:")
        print(f"  Sentiment: {efc_result.get('sentiment', {}).get('emotion', 'unknown')} (confidence: {efc_result.get('sentiment', {}).get('confidence', 0.0):.3f})")
        print(f"  Context Balance: {efc_result.get('context_balance', {}).get('balance', 'unknown')}")
        print(f"  Situation: {efc_result.get('situation', {}).get('situation', 'unknown')}")
        print(f"  Needs Status: {efc_result.get('needs', {}).get('status', 'unknown')}")
        print(f"  Core Value: {efc_result.get('calculation', {}).get('result', 0.0):.3f}")
        print()
    
    # Print emotions with explanation
    if report.emotions:
        print("🧠 LUMIRA SEMANTICS - Enhanced emotion detection:")
        for emotion in report.emotions[:3]:  # Top 3 emotions
            print(f"  - {emotion.name}: {emotion.score:.3f}")
    else:
        print("🧠 LUMIRA SEMANTICS - No emotions detected")
    
    # Print risks with explanation
    if report.risks:
        print("🛡️ LUMIRA SAFETY - Risk assessment:")
        for risk in report.risks:
            print(f"  - {risk.kind} ({risk.level}): {risk.confidence:.3f}")
            if hasattr(risk, 'excerpt') and risk.excerpt:
                print(f"    Excerpt: {risk.excerpt}")
    else:
        print("🛡️ LUMIRA SAFETY - No risks detected")
    
    # Print integrity signals with explanation
    if report.integrity:
        print("🔍 LUMIRA INTEGRITY - Incongruence detection:")
        for signal in report.integrity:
            print(f"  - {signal.level}: {signal.reason}")
    else:
        print("🔍 LUMIRA INTEGRITY - No signals detected")
    
    print("  📊 LUMIRA SIGNALS - Data stored for trend analysis")


def group_samples_by_day(samples: List[TextSample]) -> Dict[str, List[TextSample]]:
    """
    Group samples by day.
    
    Args:
        samples: List of TextSample objects
        
    Returns:
        Dictionary with day as key and samples as value
    """
    daily_samples = {}
    
    for sample in samples:
        day_key = sample.ts.date().isoformat()
        if day_key not in daily_samples:
            daily_samples[day_key] = []
        daily_samples[day_key].append(sample)
    
    return daily_samples


def run_demo(data_path: str):
    """
    Run the LUMIRA demo showing EFC + LUMIRA integration.
    
    Args:
        data_path: Path to demo data file
    """
    print("🚀 LUMIRA Demo Starting...")
    print("=" * 50)
    print("This demo shows how LUMIRA extends the EFC engine with:")
    print("1. 🧠 Semantics - Emotion detection and incongruence analysis")
    print("2. 🛡️ Safety - Risk detection for self-harm and suicide ideation")
    print("3. 📊 Signals - Overtime tracking and trend analysis")
    print("=" * 50)
    
    # Load demo data
    print(f"Loading demo data from: {data_path}")
    demo_data = load_demo_data(data_path)
    
    if not demo_data:
        print("No demo data loaded. Exiting.")
        return
    
    print(f"Loaded {len(demo_data)} samples")
    
    # Initialize EFC engine first
    print("\n🔧 Initializing EFC Engine...")
    try:
        from efc.core import EFCEngine as OriginalEFC
        efc_engine = OriginalEFC()
        print("✅ EFC Engine loaded successfully")
    except ImportError:
        print("⚠️ EFC Engine not available, using LUMIRA standalone")
        efc_engine = None
    
    # Initialize LUMIRA engine with EFC integration
    print("\n🔧 Initializing LUMIRA Engine (extending EFC)...")
    engine = LumiraEngine(
        base_engine=efc_engine,  # Pass EFC engine for integration
        flags={
            "LUMIRA_ENABLED": True,
            "LUMIRA_SEMANTICS_ENABLED": True,
            "LUMIRA_SAFETY_ENABLED": True,
            "LUMIRA_SIGNALS_ENABLED": True
        }
    )
    
    # Check module status
    status = engine.get_module_status()
    print(f"Module status: {status}")
    
    # Convert demo data to TextSample objects
    samples = []
    for i, sample_data in enumerate(demo_data):
        sample = create_text_sample(sample_data, i)
        samples.append(sample)
    
    # Group samples by day
    daily_samples = group_samples_by_day(samples)
    
    print(f"\nProcessing {len(samples)} samples across {len(daily_samples)} days...")
    print("=" * 50)
    
    # Process each day
    for day, day_samples in sorted(daily_samples.items()):
        print(f"\n📅 Day: {day}")
        print("-" * 30)
        
        for sample in day_samples:
            # Process sample with EFC + LUMIRA
            report = engine.process_sample(sample)
            
            # Get EFC results if available
            efc_result = None
            if hasattr(engine, 'base_engine') and engine.base_engine:
                try:
                    efc_result = engine.base_engine.run_pipeline(sample.text)
                except Exception as e:
                    print(f"  ⚠️ EFC processing failed: {e}")
            
            # Print results showing EFC + LUMIRA integration
            print_integrated_analysis_report(report, sample.id, day, sample.text, efc_result)
    
    # Analyze trends
    print("\n" + "=" * 50)
    print("📊 SIGNALS - Trend Analysis")
    print("=" * 50)
    
    trends = engine.analyze_window(days=7)
    if trends:
        if trends.get("alert_detected"):
            alert = trends["alert"]
            print(f"🚨 DOWNHILL ALERT DETECTED!")
            print(f"Reason: {alert['reason']}")
            print(f"Severity: {alert['severity']}")
            print(f"Joy trend: {alert['joy_trend']:.3f}")
            print(f"Risk trend: {alert['risk_trend']:.3f}")
            print(f"Window: {trends['window_days']} days")
            print(f"Records analyzed: {trends['total_records']}")
        else:
            print("✅ No downhill trends detected")
            print(f"Window: {trends['window_days']} days")
            print(f"Records analyzed: {trends['total_records']}")
    else:
        print("ℹ️ No trend data available (insufficient records)")
    
    # Print signal store stats
    print("\n" + "=" * 50)
    print("📈 Signal Store Statistics")
    print("=" * 50)
    
    stats = engine.get_signal_stats()
    if stats.get("enabled"):
        print(f"Total records: {stats['total_records']}")
        print(f"By type: {stats['by_type']}")
        print(f"By sample: {stats['by_sample']}")
        if stats['date_range']['earliest']:
            print(f"Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
    else:
        print("Signal store not enabled")
    
    print("\n🎉 Demo completed!")
    print("=" * 50)
    print("LUMIRA successfully extended EFC with:")
    print("• EFC Core: Original emotional framework computing")
    print("• LUMIRA Semantics: Enhanced emotion detection and incongruence analysis")
    print("• LUMIRA Safety: Risk assessment for self-harm and suicide ideation")
    print("• LUMIRA Signals: Overtime tracking and trend analysis")
    print("=" * 50)


def run_report(store_path: str, window_days: int, outdir: str):
    """
    Run the LUMIRA report generation.
    
    Args:
        store_path: Path to the signal store
        window_days: Number of days to analyze
        outdir: Output directory for reports
    """
    print("📊 LUMIRA Report Generation Starting...")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs(outdir, exist_ok=True)
    print(f"Output directory: {outdir}")
    
    # Generate summary
    print(f"Analyzing signal store: {store_path}")
    print(f"Window: {window_days} days")
    
    try:
        summary = make_summary(store_path, window_days)
        print("✅ Analysis completed")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate JSON report
    json_content = render_json(summary)
    json_path = os.path.join(outdir, f"lumira_report_{timestamp}.json")
    
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_content)
        print(f"✅ JSON report written: {json_path}")
    except Exception as e:
        print(f"❌ Error writing JSON report: {e}")
        return
    
    # Generate Markdown report
    markdown_content = render_markdown(summary)
    md_path = os.path.join(outdir, f"lumira_report_{timestamp}.md")
    
    try:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Markdown report written: {md_path}")
    except Exception as e:
        print(f"❌ Error writing Markdown report: {e}")
        return
    
    # Print summary
    print("\n" + "=" * 50)
    print("📈 Report Summary")
    print("=" * 50)
    print(f"Window: {summary.window_days} days")
    print(f"From: {summary.from_ts}")
    print(f"To: {summary.to_ts}")
    print(f"Records: emotions={summary.counts.get('emotions', 0)}, risks={summary.counts.get('risks', 0)}, integrity={summary.counts.get('integrity', 0)}")
    print(f"Avg joy: {summary.joy_avg:.3f}")
    print(f"Top emotions: {[f'{name}({avg:.3f})' for name, avg in summary.top_emotions[:3]]}")
    
    if summary.alert:
        print(f"🚨 Alert: {summary.alert.get('reason')}")
    else:
        print("✅ No alerts detected")
    
    print(f"\n📁 Reports generated:")
    print(f"  - JSON: {json_path}")
    print(f"  - Markdown: {md_path}")
    print("\n🎉 Report generation completed!")


def run_package(include_tests: bool = False, output_dir: str = "dist"):
    """
    Run the LUMIRA packaging.
    
    Args:
        include_tests: Whether to include tests in the bundle
        output_dir: Output directory for the bundle
    """
    print("📦 LUMIRA Packaging Starting...")
    print("=" * 50)
    
    # Get the path to the package script
    script_path = Path(__file__).parent.parent / "scripts" / "package_lumira.py"
    
    if not script_path.exists():
        print(f"❌ Package script not found: {script_path}")
        return
    
    # Build command
    cmd = [sys.executable, str(script_path)]
    
    if include_tests:
        cmd.append("--include-tests")
    
    if output_dir != "dist":
        cmd.extend(["--output-dir", output_dir])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Run the package script
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        print("✅ Packaging completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Packaging failed with exit code {e.returncode}")
        if e.stdout:
            print("Output:")
            print(e.stdout)
        if e.stderr:
            print("Errors:")
            print(e.stderr)
    except Exception as e:
        print(f"❌ Error running package script: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LUMIRA - Lightweight Unified Modular Intelligence & Reasoning Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m lumira demo --data demo_data.json
  python -m lumira demo --data /path/to/data.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run LUMIRA demo')
    demo_parser.add_argument(
        '--data',
        type=str,
        default='demo_data.json',
        help='Path to demo data JSON file (default: demo_data.json)'
    )
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate LUMIRA analysis report')
    report_parser.add_argument(
        '--window',
        type=int,
        default=7,
        help='Analysis window in days (default: 7)'
    )
    report_parser.add_argument(
        '--store',
        type=str,
        default='.lumira/signals.jsonl',
        help='Path to signal store (default: .lumira/signals.jsonl)'
    )
    report_parser.add_argument(
        '--outdir',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports)'
    )
    
    # Package command
    package_parser = subparsers.add_parser('package', help='Package LUMIRA engine into clean bundle')
    package_parser.add_argument(
        '--include-tests',
        action='store_true',
        help='Include tests directory in the bundle'
    )
    package_parser.add_argument(
        '--output-dir',
        type=str,
        default='dist',
        help='Output directory for the bundle (default: dist)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'demo':
        run_demo(args.data)
    elif args.command == 'report':
        run_report(args.store, args.window, args.outdir)
    elif args.command == 'package':
        run_package(args.include_tests, args.output_dir)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()


if __name__ == '__main__':
    main()
