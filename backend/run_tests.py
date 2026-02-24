#!/usr/bin/env python3
"""
Comprehensive test runner script for the backend.

This script:
- Checks if virtual environment exists
- Checks if dependencies are installed
- Runs pytest with proper configuration
- Generates coverage report
- Provides clear output about test results
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70 + "\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"✗ {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠ {message}")


def check_virtual_environment() -> bool:
    """Check if running in a virtual environment."""
    print_header("Checking Virtual Environment")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success(f"Running in virtual environment: {sys.prefix}")
        return True
    else:
        print_warning("Not running in a virtual environment")
        print("  It's recommended to use a virtual environment.")
        print("  To create one: python -m venv venv")
        print("  To activate:")
        print("    - Windows: venv\\Scripts\\activate")
        print("    - Unix/Mac: source venv/bin/activate")
        return False


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    print_header("Checking Dependencies")
    
    required_packages = [
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "fastapi",
        "sqlalchemy",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n" + "=" * 70)
        print_error("Missing dependencies detected!")
        print("\nTo install missing dependencies, run:")
        print("  pip install -r requirements.txt")
        print("=" * 70)
        return False
    
    return True


def run_tests() -> int:
    """Run pytest with coverage."""
    print_header("Running Tests")
    
    # Build pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--cov=src",  # Coverage for src directory
        "--cov-report=term-missing",  # Show missing lines in terminal
        "--cov-report=html",  # Generate HTML coverage report
        "--cov-report=xml",  # Generate XML coverage report (for CI)
    ]
    
    print(f"Running command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode
    except Exception as e:
        print_error(f"Failed to run tests: {e}")
        return 1


def print_coverage_info() -> None:
    """Print information about coverage reports."""
    print_header("Coverage Reports")
    
    html_report = Path(__file__).parent / "htmlcov" / "index.html"
    xml_report = Path(__file__).parent / "coverage.xml"
    
    if html_report.exists():
        print_success(f"HTML coverage report: {html_report}")
        print(f"  Open in browser: file://{html_report.absolute()}")
    
    if xml_report.exists():
        print_success(f"XML coverage report: {xml_report}")


def main() -> int:
    """Main entry point."""
    print("\n" + "=" * 70)
    print("  Backend Test Runner")
    print("=" * 70)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Check virtual environment (warning only, not blocking)
    check_virtual_environment()
    
    # Check dependencies (blocking)
    if not check_dependencies():
        return 1
    
    # Run tests
    exit_code = run_tests()
    
    # Print coverage info
    if exit_code == 0:
        print_coverage_info()
        print_header("Test Results")
        print_success("All tests passed!")
    else:
        print_header("Test Results")
        print_error("Some tests failed. Please review the output above.")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
