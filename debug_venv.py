#!/usr/bin/env python3
"""
Virtual Environment Diagnostic Script
This script identifies common issues with virtual environment setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Fix for Windows console encoding issues
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def log_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_python_installations():
    """Check available Python installations"""
    log_section("Python Installations Check")

    try:
        # Check which python is being used
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"Current Python: {result.stdout.strip()}")

        # Check all python installations in PATH
        if platform.system() == "Windows":
            result = subprocess.run(["where", "python"], capture_output=True, text=True)
        else:
            result = subprocess.run(["which", "-a", "python3", "python"], capture_output=True, text=True)

        print(f"Python installations found:\n{result.stdout}")

        # Check if venv module is available
        try:
            import venv
            print("✅ venv module is available")
        except ImportError:
            print("❌ venv module is NOT available")

    except Exception as e:
        print(f"❌ Error checking Python installations: {e}")

def check_virtual_environments():
    """Check for existing virtual environments"""
    log_section("Virtual Environment Check")

    venv_dirs = ["venv", ".venv", "env", ".env"]
    found_venvs = []

    for venv_dir in venv_dirs:
        if Path(venv_dir).exists():
            found_venvs.append(venv_dir)
            print(f"✅ Found virtual environment: {venv_dir}")

            # Check if it has activation scripts
            if platform.system() == "Windows":
                activate_path = Path(venv_dir) / "Scripts" / "activate.bat"
            else:
                activate_path = Path(venv_dir) / "bin" / "activate"

            if activate_path.exists():
                print(f"✅ Activation script found: {activate_path}")
            else:
                print(f"❌ Activation script missing: {activate_path}")

    if not found_venvs:
        print("❌ No virtual environments found in project directory")

def check_environment_variables():
    """Check relevant environment variables"""
    log_section("Environment Variables Check")

    env_vars = ["VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV"]
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def test_venv_creation():
    """Test virtual environment creation"""
    log_section("Virtual Environment Creation Test")

    test_venv = "test_venv"
    try:
        # Try to create a test virtual environment
        result = subprocess.run([sys.executable, "-m", "venv", test_venv],
                              capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("[OK] Virtual environment creation successful")

            # Test activation
            if platform.system() == "Windows":
                activate_cmd = f"{test_venv}\\Scripts\\activate.bat && python --version"
            else:
                activate_cmd = f"source {test_venv}/bin/activate && python --version"

            # Clean up
            import shutil
            shutil.rmtree(test_venv)
            print("[OK] Test virtual environment cleaned up")
        else:
            print(f"[ERROR] Virtual environment creation failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ Virtual environment creation timed out")
    except Exception as e:
        print(f"❌ Error during virtual environment creation test: {e}")

def check_common_issues():
    """Check for common virtual environment issues"""
    log_section("Common Issues Check")

    issues = []

    # Check if we're in a conda environment that might interfere
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        issues.append(f"Conda environment active: {conda_prefix}")

    # Check if Python path contains spaces (can cause issues on Windows)
    if " " in sys.executable and platform.system() == "Windows":
        issues.append(f"Python path contains spaces: {sys.executable}")

    # Check if we have write permissions
    try:
        test_file = Path("venv_test_permissions.txt")
        test_file.write_text("test")
        test_file.unlink()
    except PermissionError:
        issues.append("❌ No write permissions in current directory")

    if issues:
        print("Potential issues found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ No obvious issues detected")

def main():
    print("Virtual Environment Diagnostic Tool")
    print("Running comprehensive checks...")

    check_python_installations()
    check_virtual_environments()
    check_environment_variables()
    test_venv_creation()
    check_common_issues()

    print(f"\n{'='*60}")
    print("Diagnostic complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()