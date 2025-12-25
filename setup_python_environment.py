"""
Python Environment Setup Automation
Automated setup script for Python development environments
Handles virtual environments, dependencies, and system configuration for A6-9V projects
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional
import platform
import urllib.request
import zipfile
import tempfile


class PythonEnvironmentSetup:
    """
    Automated Python Environment Setup
    Creates and configures Python environments for development and production
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.system_info = self.get_system_info()
        self.python_version = "3.11"
        
    def get_system_info(self) -> Dict[str, str]:
        """Get system information"""
        return {
            'platform': platform.system(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version(),
            'machine': platform.machine()
        }
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are installed"""
        print("Checking prerequisites...")
        
        checks = {
            'Python': self.check_python(),
            'pip': self.check_pip(),
            'git': self.check_git(),
            'PowerShell': self.check_powershell() if self.system_info['platform'] == 'Windows' else True
        }
        
        all_good = True
        for tool, status in checks.items():
            status_text = "✓" if status else "✗"
            print(f"  {status_text} {tool}")
            if not status:
                all_good = False
        
        if not all_good:
            print("\\nSome prerequisites are missing. Please install them first.")
            self.show_installation_instructions()
        
        return all_good
    
    def check_python(self) -> bool:
        """Check if Python is installed"""
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_pip(self) -> bool:
        """Check if pip is installed"""
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_git(self) -> bool:
        """Check if git is installed"""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_powershell(self) -> bool:
        """Check if PowerShell is available (Windows only)"""
        try:
            result = subprocess.run(['pwsh', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            try:
                result = subprocess.run(['powershell', '--version'], capture_output=True, text=True)
                return result.returncode == 0
            except:
                return False
    
    def show_installation_instructions(self):
        """Show installation instructions for missing prerequisites"""
        print("\\nInstallation Instructions:")
        print("=" * 50)
        
        if self.system_info['platform'] == 'Windows':
            print("For Windows:")
            print("1. Python: Download from https://python.org/downloads/")
            print("2. Git: Download from https://git-scm.com/download/win")
            print("3. PowerShell: Usually pre-installed, or download PowerShell 7+")
        else:
            print("For Linux/macOS:")
            print("1. Python: Use your package manager (apt, yum, brew)")
            print("2. Git: Use your package manager")
    
    def setup_project_structure(self, project_name: str) -> Path:
        """Setup basic project directory structure"""
        project_path = self.project_root / project_name
        
        directories = [
            'src',
            'tests',
            'docs',
            'scripts',
            'config',
            'data',
            'logs',
            'venv'
        ]
        
        print(f"Setting up project structure for {project_name}...")
        project_path.mkdir(exist_ok=True)
        
        for directory in directories:
            (project_path / directory).mkdir(exist_ok=True)
            print(f"  ✓ Created directory: {directory}")
        
        return project_path
    
    def create_virtual_environment(self, project_path: Path, python_version: str = None) -> bool:
        """Create virtual environment for the project"""
        venv_path = project_path / 'venv'
        python_exe = python_version or sys.executable
        
        try:
            print(f"Creating virtual environment at {venv_path}...")
            
            # Remove existing venv if it exists
            if venv_path.exists():
                print("  Removing existing virtual environment...")
                shutil.rmtree(venv_path)
            
            # Create new virtual environment
            subprocess.run([python_exe, '-m', 'venv', str(venv_path)], check=True)
            print("  ✓ Virtual environment created successfully")
            
            # Get pip path
            if self.system_info['platform'] == 'Windows':
                pip_path = venv_path / 'Scripts' / 'pip.exe'
            else:
                pip_path = venv_path / 'bin' / 'pip'
            
            # Upgrade pip
            print("  Upgrading pip...")
            subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
            print("  ✓ Pip upgraded successfully")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error creating virtual environment: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False
    
    def install_base_packages(self, project_path: Path, additional_packages: List[str] = None) -> bool:
        """Install base packages in the virtual environment"""
        venv_path = project_path / 'venv'
        
        if self.system_info['platform'] == 'Windows':
            pip_path = venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_path = venv_path / 'bin' / 'pip'
        
        # Base packages for development
        base_packages = [
            'wheel',
            'setuptools',
            'requests',
            'python-dotenv',
            'pyyaml',
            'psutil',
            'pytest',
            'pytest-asyncio',
            'black',
            'flake8',
            'mypy'
        ]
        
        if additional_packages:
            base_packages.extend(additional_packages)
        
        try:
            print("Installing base packages...")
            for package in base_packages:
                print(f"  Installing {package}...")
                subprocess.run([str(pip_path), 'install', package], check=True, capture_output=True)
                print(f"  ✓ {package} installed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error installing packages: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False
    
    def install_from_requirements(self, project_path: Path, requirements_file: str = "requirements.txt") -> bool:
        """Install packages from requirements file"""
        venv_path = project_path / 'venv'
        requirements_path = project_path / requirements_file
        
        if not requirements_path.exists():
            print(f"  Requirements file {requirements_file} not found, skipping...")
            return True
        
        if self.system_info['platform'] == 'Windows':
            pip_path = venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_path = venv_path / 'bin' / 'pip'
        
        try:
            print(f"Installing packages from {requirements_file}...")
            subprocess.run([
                str(pip_path), 'install', '-r', str(requirements_path)
            ], check=True)
            print("  ✓ Requirements installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error installing from requirements: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False
    
    def create_project_files(self, project_path: Path, project_name: str):
        """Create basic project files"""
        files_to_create = {
            'README.md': self.get_readme_template(project_name),
            'requirements.txt': self.get_requirements_template(),
            '.env.example': self.get_env_template(),
            '.gitignore': self.get_gitignore_template(),
            'setup.py': self.get_setup_template(project_name),
            'pyproject.toml': self.get_pyproject_template(project_name),
            'src/__init__.py': '',
            'tests/__init__.py': '',
            'tests/test_main.py': self.get_test_template(project_name),
            'scripts/run.py': self.get_run_script_template(project_name),
            'config/settings.py': self.get_settings_template(project_name)
        }
        
        print("Creating project files...")
        for file_path, content in files_to_create.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not full_path.exists():
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Created: {file_path}")
            else:
                print(f"  - Skipped (exists): {file_path}")
    
    def get_readme_template(self, project_name: str) -> str:
        """Get README template"""
        return f"""# {project_name}

## Description
A Python project managed by A6-9V organization.

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment:
   - Windows: `venv\\Scripts\\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
```bash
python src/main.py
```

## Development
- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8 .`
- Type check: `mypy .`

## Configuration
Copy `.env.example` to `.env` and configure your settings.
"""
    
    def get_requirements_template(self) -> str:
        """Get requirements template"""
        return """# Core dependencies
requests>=2.31.0
python-dotenv>=1.0.0
pyyaml>=6.0
psutil>=5.9.0

# Development dependencies
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
"""
    
    def get_env_template(self) -> str:
        """Get .env template"""
        return """# Environment Configuration
# Copy this file to .env and configure your settings

# Application Settings
APP_NAME=MyApp
APP_VERSION=1.0.0
DEBUG=true

# Database Settings (if applicable)
# DATABASE_URL=sqlite:///./app.db

# API Keys (if applicable)
# API_KEY=your_api_key_here

# A6-9V Organization Settings
ORGANIZATION=A6-9V
ENVIRONMENT=development
"""
    
    def get_gitignore_template(self) -> str:
        """Get .gitignore template"""
        return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Data files
data/
*.csv
*.json
*.xlsx

# Temporary files
tmp/
temp/
"""
    
    def get_setup_template(self, project_name: str) -> str:
        """Get setup.py template"""
        return f"""from setuptools import setup, find_packages

setup(
    name="{project_name.lower().replace(' ', '-')}",
    version="1.0.0",
    description="A Python project by A6-9V organization",
    author="A6-9V",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "psutil>=5.9.0",
    ],
    extras_require={{
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ]
    }},
)
"""
    
    def get_pyproject_template(self, project_name: str) -> str:
        """Get pyproject.toml template"""
        return f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name.lower().replace(' ', '-')}"
version = "1.0.0"
description = "A Python project by A6-9V organization"
authors = [{{name = "A6-9V", email = "contact@a6-9v.org"}}]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "psutil>=5.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
]

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
"""
    
    def get_test_template(self, project_name: str) -> str:
        """Get test template"""
        return f"""import pytest
from src.main import main  # Adjust import as needed


def test_{project_name.lower().replace(' ', '_')}_basic():
    \"\"\"Basic test for {project_name}\"\"\"
    # Add your test logic here
    assert True


def test_{project_name.lower().replace(' ', '_')}_functionality():
    \"\"\"Test main functionality\"\"\"
    # Add specific functionality tests
    pass


if __name__ == "__main__":
    pytest.main([__file__])
"""
    
    def get_run_script_template(self, project_name: str) -> str:
        """Get run script template"""
        return f"""#!/usr/bin/env python3
\"\"\"
Run script for {project_name}
Handles environment setup and application startup
\"\"\"

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(project_root / ".env")


def main():
    \"\"\"Main entry point\"\"\"
    print("Starting {project_name}...")
    
    # Import and run your main application
    try:
        from main import main as app_main
        app_main()
    except ImportError:
        print("No main.py found in src directory")
        print("Create src/main.py with your application code")


if __name__ == "__main__":
    main()
"""
    
    def get_settings_template(self, project_name: str) -> str:
        """Get settings template"""
        return f"""\"\"\"
Settings and configuration for {project_name}
\"\"\"

import os
from pathlib import Path
from typing import Optional


class Settings:
    \"\"\"Application settings\"\"\"
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "{project_name}")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Organization
    ORGANIZATION: str = os.getenv("ORGANIZATION", "A6-9V")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_directories(cls):
        \"\"\"Ensure required directories exist\"\"\"
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
"""
    
    def setup_git_repository(self, project_path: Path) -> bool:
        """Initialize git repository"""
        try:
            print("Initializing git repository...")
            
            # Check if already a git repo
            if (project_path / '.git').exists():
                print("  - Git repository already exists")
                return True
            
            # Initialize git repo
            subprocess.run(['git', 'init'], cwd=project_path, check=True)
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_path, check=True)
            
            print("  ✓ Git repository initialized")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error initializing git repository: {e}")
            return False
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            return False
    
    def setup_complete_project(self, project_name: str, additional_packages: List[str] = None) -> bool:
        """Setup a complete Python project"""
        print(f"\\n{'='*60}")
        print(f"Setting up Python project: {project_name}")
        print(f"{'='*60}\\n")
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Setup project structure
        project_path = self.setup_project_structure(project_name)
        
        # Create virtual environment
        if not self.create_virtual_environment(project_path):
            return False
        
        # Install base packages
        if not self.install_base_packages(project_path, additional_packages):
            return False
        
        # Create project files
        self.create_project_files(project_path, project_name)
        
        # Install from requirements if it exists
        self.install_from_requirements(project_path)
        
        # Setup git repository
        self.setup_git_repository(project_path)
        
        print(f"\\n{'='*60}")
        print(f"✓ Project {project_name} setup completed successfully!")
        print(f"✓ Project location: {project_path}")
        print(f"{'='*60}")
        print("\\nNext steps:")
        print(f"1. cd {project_path}")
        print("2. Activate virtual environment:")
        if self.system_info['platform'] == 'Windows':
            print("   .\\venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("3. Start developing!")
        
        return True


def main():
    \"\"\"Main entry point for environment setup\"\"\"
    import argparse
    
    parser = argparse.ArgumentParser(description="Python Environment Setup Automation")
    parser.add_argument('project_name', help="Name of the project to create")
    parser.add_argument('--packages', nargs='*', help="Additional packages to install")
    parser.add_argument('--root', help="Project root directory", default=None)
    
    args = parser.parse_args()
    
    setup = PythonEnvironmentSetup(args.root)
    success = setup.setup_complete_project(args.project_name, args.packages)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()