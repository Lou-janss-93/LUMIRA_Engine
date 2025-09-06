#!/usr/bin/env python3
"""
Interactive LUMIRA Demo

An interactive demonstration of EFC + LUMIRA integration.
Users can input their own text and see how EFC and LUMIRA work together.
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lumira.engine import LumiraEngine
from lumira.types import TextSample
from efc.core import EFCEngine as OriginalEFC


def print_header():
    """Print the demo header."""
    print("=" * 60)
    print("🚀 INTERACTIVE LUMIRA DEMO")
    print("=" * 60)
    print("This interactive demo shows how LUMIRA extends EFC with:")
    print("1. 🧠 Semantics - Enhanced emotion detection")
    print("2. 🛡️ Safety - Risk assessment for self-harm/suicide")
    print("3. 📊 Signals - Overtime tracking and trend analysis")
    print("=" * 60)
    print()


def initialize_engines():
    """Initialize EFC and LUMIRA engines."""
    print("🔧 Initializing engines...")
    
    # Initialize EFC engine
    try:
        efc_engine = OriginalEFC()
        print("✅ EFC Engine loaded successfully")
    except ImportError as e:
        print(f"⚠️ EFC Engine not available: {e}")
        efc_engine = None
    
    # Initialize LUMIRA engine with EFC integration
    lumira_engine = LumiraEngine(
        base_engine=efc_engine,
        flags={
            "LUMIRA_ENABLED": True,
            "LUMIRA_SEMANTICS_ENABLED": True,
            "LUMIRA_SAFETY_ENABLED": True,
            "LUMIRA_SIGNALS_ENABLED": True
        }
    )
    print("✅ LUMIRA Engine loaded successfully")
    print()
    
    return efc_engine, lumira_engine


def analyze_text(text: str, efc_engine: Optional[OriginalEFC], lumira_engine: LumiraEngine):
    """Analyze text with both EFC and LUMIRA."""
    print(f"📝 Analyzing: '{text}'")
    print("-" * 50)
    
    # Create TextSample
    sample = TextSample(
        id=f"interactive_{datetime.now().strftime('%H%M%S')}",
        ts=datetime.now(),
        source="interactive_demo",
        text=text,
        meta={"interactive": True}
    )
    
    # Process with LUMIRA
    lumira_result = lumira_engine.process_sample(sample)
    
    # Process with EFC if available
    efc_result = None
    if efc_engine:
        try:
            efc_result = efc_engine.run_pipeline(text)
        except Exception as e:
            print(f"⚠️ EFC processing failed: {e}")
    
    # Display results
    print_results(efc_result, lumira_result)
    
    return lumira_result


def print_results(efc_result, lumira_result):
    """Print analysis results."""
    print("🔧 EFC + LUMIRA INTEGRATION RESULTS:")
    print()
    
    # EFC Results
    if efc_result:
        print("🔧 EFC CORE ANALYSIS:")
        print(f"  Sentiment: {efc_result.get('sentiment', {}).get('emotion', 'unknown')} (confidence: {efc_result.get('sentiment', {}).get('confidence', 0.0):.3f})")
        print(f"  Context Balance: {efc_result.get('context_balance', {}).get('balance', 'unknown')}")
        print(f"  Situation: {efc_result.get('situation', {}).get('situation', 'unknown')}")
        print(f"  Needs Status: {efc_result.get('needs', {}).get('status', 'unknown')}")
        print(f"  Core Value: {efc_result.get('calculation', {}).get('result', 0.0):.3f}")
        print()
    else:
        print("🔧 EFC CORE ANALYSIS: Not available")
        print()
    
    # LUMIRA Results
    print("🧠 LUMIRA SEMANTICS - Enhanced emotion detection:")
    if lumira_result.emotions:
        for emotion in lumira_result.emotions[:3]:
            print(f"  - {emotion.name}: {emotion.score:.3f}")
    else:
        print("  - No emotions detected")
    
    print("🛡️ LUMIRA SAFETY - Risk assessment:")
    if lumira_result.risks:
        for risk in lumira_result.risks:
            print(f"  - {risk.kind} ({risk.level}): {risk.confidence:.3f}")
            if hasattr(risk, 'excerpt') and risk.excerpt:
                print(f"    Excerpt: {risk.excerpt}")
    else:
        print("  - No risks detected")
    
    print("🔍 LUMIRA INTEGRITY - Incongruence detection:")
    if lumira_result.integrity:
        for signal in lumira_result.integrity:
            print(f"  - {signal.level}: {signal.reason}")
    else:
        print("  - No signals detected")
    
    print("📊 LUMIRA SIGNALS - Data stored for trend analysis")
    print()


def show_examples():
    """Show example texts."""
    examples = [
        "I'm so excited about the new project! This is going to be amazing!",
        "I feel really anxious about the presentation tomorrow.",
        "I hate myself sometimes. Nothing I do ever works out right.",
        "I promise I'll finish this by Friday, but I'm not sure I can deliver.",
        "I can't stop thinking about hurting myself. Maybe I should just disappear.",
        "I'm really proud of what we accomplished today!",
        "I feel so alone and isolated. Nobody understands me.",
        "I'm confident this will work out perfectly. I know exactly what to do."
    ]
    
    print("📋 EXAMPLE TEXTS TO TRY:")
    print("-" * 30)
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    print()


def show_menu():
    """Show the main menu."""
    print("🎯 INTERACTIVE MENU:")
    print("1. Analyze your own text")
    print("2. Try example texts")
    print("3. Show trend analysis")
    print("4. Show signal statistics")
    print("5. Exit")
    print()


def show_trend_analysis(lumira_engine: LumiraEngine):
    """Show trend analysis."""
    print("📊 TREND ANALYSIS")
    print("-" * 30)
    
    trends = lumira_engine.analyze_window(days=7)
    if trends:
        if trends.get("alert_detected"):
            alert = trends["alert"]
            print(f"🚨 DOWNHILL ALERT DETECTED!")
            print(f"Reason: {alert['reason']}")
            print(f"Severity: {alert['severity']}")
            print(f"Joy trend: {alert['joy_trend']:.3f}")
            print(f"Risk trend: {alert['risk_trend']:.3f}")
        else:
            print("✅ No downhill trends detected")
        print(f"Window: {trends['window_days']} days")
        print(f"Records analyzed: {trends['total_records']}")
    else:
        print("ℹ️ No trend data available (insufficient records)")
    print()


def show_signal_stats(lumira_engine: LumiraEngine):
    """Show signal statistics."""
    print("📈 SIGNAL STATISTICS")
    print("-" * 30)
    
    stats = lumira_engine.get_signal_stats()
    if stats.get("enabled"):
        print(f"Total records: {stats['total_records']}")
        print(f"By type: {stats['by_type']}")
        print(f"By sample: {stats['by_sample']}")
        if stats['date_range']['earliest']:
            print(f"Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
    else:
        print("Signal store not enabled")
    print()


def main():
    """Main interactive demo function."""
    print_header()
    
    # Initialize engines
    efc_engine, lumira_engine = initialize_engines()
    
    # Show examples
    show_examples()
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                text = input("\nEnter text to analyze: ").strip()
                if text:
                    analyze_text(text, efc_engine, lumira_engine)
                else:
                    print("Please enter some text to analyze.")
            
            elif choice == "2":
                show_examples()
                try:
                    example_num = int(input("Enter example number (1-8): ")) - 1
                    if 0 <= example_num < 8:
                        examples = [
                            "I'm so excited about the new project! This is going to be amazing!",
                            "I feel really anxious about the presentation tomorrow.",
                            "I hate myself sometimes. Nothing I do ever works out right.",
                            "I promise I'll finish this by Friday, but I'm not sure I can deliver.",
                            "I can't stop thinking about hurting myself. Maybe I should just disappear.",
                            "I'm really proud of what we accomplished today!",
                            "I feel so alone and isolated. Nobody understands me.",
                            "I'm confident this will work out perfectly. I know exactly what to do."
                        ]
                        analyze_text(examples[example_num], efc_engine, lumira_engine)
                    else:
                        print("Please enter a number between 1 and 8.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == "3":
                show_trend_analysis(lumira_engine)
            
            elif choice == "4":
                show_signal_stats(lumira_engine)
            
            elif choice == "5":
                print("\n🎉 Thank you for trying the Interactive LUMIRA Demo!")
                print("LUMIRA successfully demonstrated EFC + LUMIRA integration!")
                break
            
            else:
                print("Please enter a valid choice (1-5).")
            
            print("\n" + "=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
