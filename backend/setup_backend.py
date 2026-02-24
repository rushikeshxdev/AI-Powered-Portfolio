#!/usr/bin/env python3
"""
Backend Setup Script

This script automates the entire backend setup process:
1. Checks Python version (3.8+ required)
2. Creates virtual environment if needed
3. Provides activation instructions
4. Installs dependencies
5. Runs health checks
6. Provides next steps

Works on Windows (PowerShell/CMD), macOS, and Linux.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Tuple, Optional


# ANSI color codes for terminal output
class Colors:
    """Terminal color codes."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(message: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {message}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.ENDC}\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ {message}{Colors.ENDC}")


def print_step(step_num: int, message: str) -> None:
    """Print a step message."""
    print(f"\n{Colors.BOLD}Step {step_num}: {message}{Colors.ENDC}")


def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.8 or higher."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python version: {version_str}")
    print_info(f"Python executable: {sys.executable}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} meets requirements (3.8+)")
        return True, version_str
    else:
        print_error(f"Python {version_str} is too old. Python 3.8+ is required.")
        return False, version_str


def get_venv_path() -> Path:
    """Get the virtual environment path."""
    backend_dir = Path(__file__).parent
    return backend_dir / "venv"


def check_venv_exists() -> bool:
    """Check if virtual environment already exists."""
    venv_path = get_venv_path()
    return venv_path.exists() and venv_path.is_dir()


def create_venv() -> bool:
    """Create a virtual environment."""
    print_step(2, "Creating Virtual Environment")
    
    venv_path = get_venv_path()
    
    if check_venv_exists():
        print_warning(f"Virtual environment already exists at: {venv_path}")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response != 'y':
            print_info("Skipping virtual environment creation.")
            return True
        else:
            print_info("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
    
    try:
        print_info(f"Creating virtual environment at: {venv_path}")
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print_success("Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        print_error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"Unexpected error creating virtual environment: {e}")
        return False


def get_activation_command() -> Tuple[str, str]:
    """Get the command to activate the virtual environment based on OS."""
    venv_path = get_venv_path()
    system = platform.system()
    
    if system == "Windows":
        # Check if running in PowerShell or CMD
        powershell_cmd = str(venv_path / "Scripts" / "Activate.ps1")
        cmd_cmd = str(venv_path / "Scripts" / "activate.bat")
        
        return (
            f"PowerShell: .\\venv\\Scripts\\Activate.ps1",
            f"CMD: venv\\Scripts\\activate.bat"
        )
    else:
        # macOS and Linux
        return (f"source venv/bin/activate", "")


def print_activation_instructions() -> None:
    """Print instructions for activating the virtual environment."""
    print_step(3, "Activate Virtual Environment")
    
    print_info("You need to activate the virtual environment before installing dependencies.")
    print()
    
    system = platform.system()
    
    if system == "Windows":
        print(f"{Colors.BOLD}For PowerShell:{Colors.ENDC}")
        print(f"  {Colors.CYAN}.\\venv\\Scripts\\Activate.ps1{Colors.ENDC}")
        print()
        print(f"{Colors.BOLD}For Command Prompt (CMD):{Colors.ENDC}")
        print(f"  {Colors.CYAN}venv\\Scripts\\activate.bat{Colors.ENDC}")
        print()
        print_warning("If you get an execution policy error in PowerShell, run:")
        print(f"  {Colors.CYAN}Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser{Colors.ENDC}")
    else:
        print(f"{Colors.BOLD}For macOS/Linux:{Colors.ENDC}")
        print(f"  {Colors.CYAN}source venv/bin/activate{Colors.ENDC}")
    
    print()
    print_info("After activation, you should see (venv) in your terminal prompt.")


def is_venv_activated() -> bool:
    """Check if we're running inside a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )


def get_pip_executable() -> str:
    """Get the pip executable path for the virtual environment."""
    venv_path = get_venv_path()
    system = platform.system()
    
    if system == "Windows":
        return str(venv_path / "Scripts" / "pip.exe")
    else:
        return str(venv_path / "bin" / "pip")


def install_dependencies() -> bool:
    """Install dependencies from requirements.txt."""
    print_step(4, "Installing Dependencies")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print_error("requirements.txt not found!")
        return False
    
    # Determine which pip to use
    if is_venv_activated():
        pip_cmd = "pip"
        print_info("Virtual environment is activated. Using pip from venv.")
    else:
        pip_cmd = get_pip_executable()
        print_warning("Virtual environment is NOT activated.")
        print_info(f"Using pip from: {pip_cmd}")
    
    try:
        print_info("Installing dependencies... This may take a few minutes.")
        print()
        
        # Upgrade pip first
        print_info("Upgrading pip...")
        subprocess.run(
            [pip_cmd, "install", "--upgrade", "pip"],
            check=True
        )
        
        # Install requirements
        print_info("Installing packages from requirements.txt...")
        subprocess.run(
            [pip_cmd, "install", "-r", str(requirements_file)],
            check=True
        )
        
        print()
        print_success("All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error installing dependencies: {e}")
        return False


def run_health_check() -> bool:
    """Run the backend health check script."""
    print_step(5, "Running Health Check")
    
    check_script = Path(__file__).parent / "check_backend.py"
    
    if not check_script.exists():
        print_warning("Health check script not found. Skipping.")
        return True
    
    # Determine which python to use
    if is_venv_activated():
        python_cmd = sys.executable
    else:
        venv_path = get_venv_path()
        system = platform.system()
        if system == "Windows":
            python_cmd = str(venv_path / "Scripts" / "python.exe")
        else:
            python_cmd = str(venv_path / "bin" / "python")
    
    try:
        print_info("Running health check...")
        print()
        
        result = subprocess.run(
            [python_cmd, str(check_script)],
            capture_output=False
        )
        
        print()
        if result.returncode == 0:
            print_success("Health check passed!")
            return True
        else:
            print_warning("Health check found some issues. Please review the output above.")
            return False
            
    except Exception as e:
        print_error(f"Failed to run health check: {e}")
        return False


def print_next_steps(health_check_passed: bool) -> None:
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    if not is_venv_activated():
        print_warning("Remember to activate your virtual environment:")
        print()
        system = platform.system()
        if system == "Windows":
            print(f"  PowerShell: {Colors.CYAN}.\\venv\\Scripts\\Activate.ps1{Colors.ENDC}")
            print(f"  CMD: {Colors.CYAN}venv\\Scripts\\activate.bat{Colors.ENDC}")
        else:
            print(f"  {Colors.CYAN}source venv/bin/activate{Colors.ENDC}")
        print()
    
    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print()
    
    if not health_check_passed:
        print("1. Fix any issues reported in the health check above")
        print("2. Make sure you have a .env file with required variables:")
        print("   - DATABASE_URL")
        print("   - OPENROUTER_API_KEY")
        print("3. Run the health check again:")
        print(f"   {Colors.CYAN}python check_backend.py{Colors.ENDC}")
        print()
    
    print(f"{Colors.BOLD}To start the development server:{Colors.ENDC}")
    print(f"  {Colors.CYAN}uvicorn src.main:app --reload{Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}To run tests:{Colors.ENDC}")
    print(f"  {Colors.CYAN}python run_tests.py{Colors.ENDC}")
    print(f"  or: {Colors.CYAN}pytest{Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}Useful commands:{Colors.ENDC}")
    print(f"  Health check: {Colors.CYAN}python check_backend.py{Colors.ENDC}")
    print(f"  Database migrations: {Colors.CYAN}alembic upgrade head{Colors.ENDC}")
    print(f"  View logs: {Colors.CYAN}tail -f logs/app.log{Colors.ENDC}")
    print()
    
    print(f"{Colors.BOLD}Documentation:{Colors.ENDC}")
    print("  - README.md - Project overview")
    print("  - SETUP_GUIDE.md - Detailed setup instructions")
    print("  - DATABASE.md - Database setup and migrations")
    print("  - INITIALIZATION_GUIDE.md - RAG system initialization")
    print()
    
    print_success("Happy coding! 🚀")


def main() -> int:
    """Main entry point."""
    print_header("Backend Setup Script")
    print_info("This script will set up your backend development environment.")
    print()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print_info(f"Working directory: {backend_dir}")
    
    # Step 1: Check Python version
    python_ok, version = check_python_version()
    if not python_ok:
        print()
        print_error("Setup cannot continue with incompatible Python version.")
        print_info("Please install Python 3.8 or higher and try again.")
        return 1
    
    # Step 2: Create virtual environment
    if not create_venv():
        print()
        print_error("Setup failed: Could not create virtual environment.")
        return 1
    
    # Step 3: Print activation instructions
    print_activation_instructions()
    
    # Check if venv is activated
    if not is_venv_activated():
        print()
        print_warning("Virtual environment is NOT currently activated.")
        print()
        response = input("Do you want to continue with dependency installation? (Y/n): ").strip().lower()
        if response == 'n':
            print()
            print_info("Setup paused. Please activate the virtual environment and run this script again.")
            print_info("Or manually install dependencies with: pip install -r requirements.txt")
            return 0
        else:
            print()
            print_info("Continuing with installation using venv pip directly...")
    
    # Step 4: Install dependencies
    if not install_dependencies():
        print()
        print_error("Setup failed: Could not install dependencies.")
        print_info("You can try installing manually with: pip install -r requirements.txt")
        return 1
    
    # Step 5: Run health check
    health_check_passed = run_health_check()
    
    # Print next steps
    print_next_steps(health_check_passed)
    
    return 0 if health_check_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print_warning("Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
