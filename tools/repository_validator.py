#!/usr/bin/env python
"""
Repository Validation Tool for FabricERP.

Automatically validates the entire repository for:
- Python syntax compilation
- Indentation and tab errors
- Import resolution
- Dependency completeness
- Django system checks
- Migration validation
- Circular import detection
- Template syntax
- Static files
"""

import os
import sys
import ast
import subprocess
import importlib
import pkgutil
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class ValidationResult:
    """Container for validation results."""
    success: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'success': self.success,
            'message': self.message,
            'details': self.details,
            'errors': self.errors,
            'warnings': self.warnings,
        }


class RepositoryValidator:
    """
    Comprehensive repository validation tool.
    """

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize the validator with the project root path.
        """
        if project_root is None:
            self.project_root = Path(__file__).resolve().parent.parent
        else:
            self.project_root = Path(project_root)

        self.results = {
            'python_compilation': ValidationResult(False, 'Not run'),
            'syntax_validation': ValidationResult(False, 'Not run'),
            'import_validation': ValidationResult(False, 'Not run'),
            'dependency_validation': ValidationResult(False, 'Not run'),
            'django_system_check': ValidationResult(False, 'Not run'),
            'migration_validation': ValidationResult(False, 'Not run'),
            'circular_import_detection': ValidationResult(False, 'Not run'),
            'template_validation': ValidationResult(False, 'Not run'),
            'static_files_validation': ValidationResult(False, 'Not run'),
        }
        self.overall_success = False

    def run_all(self) -> ValidationResult:
        """
        Run all validation checks.
        """
        print("=" * 60)
        print("FabricERP Repository Validator")
        print("=" * 60)
        print(f"Project Root: {self.project_root}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 60)

        self.results['python_compilation'] = self.validate_python_compilation()
        self.results['syntax_validation'] = self.validate_syntax()
        self.results['import_validation'] = self.validate_imports()
        self.results['dependency_validation'] = self.validate_dependencies()
        self.results['django_system_check'] = self.validate_django_system()
        self.results['migration_validation'] = self.validate_migrations()
        self.results['circular_import_detection'] = self.detect_circular_imports()
        self.results['template_validation'] = self.validate_templates()
        self.results['static_files_validation'] = self.validate_static_files()

        self.overall_success = all(
            r.success for r in self.results.values()
        )

        return self.get_summary()

    def validate_python_compilation(self) -> ValidationResult:
        """
        Validate all Python files compile without syntax errors.
        """
        print("\n[1/9] Validating Python compilation...")

        errors = []
        warnings = []
        details = {
            'total_files': 0,
            'compiled_files': 0,
            'failed_files': 0,
            'failed_details': []
        }

        python_files = list(self.project_root.rglob('*.py'))

        # Exclude virtual environment
        python_files = [f for f in python_files if 'venv' not in str(f) and 'env' not in str(f)]

        details['total_files'] = len(python_files)

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self._compile_single_file, f): f
                for f in python_files
            }

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    success, error = future.result()
                    if success:
                        details['compiled_files'] += 1
                    else:
                        details['failed_files'] += 1
                        details['failed_details'].append({
                            'file': str(file_path),
                            'error': error
                        })
                        errors.append(f"Compilation error in {file_path}: {error}")
                except Exception as e:
                    details['failed_files'] += 1
                    details['failed_details'].append({
                        'file': str(file_path),
                        'error': str(e)
                    })
                    errors.append(f"Unexpected error in {file_path}: {e}")

        success = details['failed_files'] == 0

        print(f"   ✓ Total files: {details['total_files']}")
        print(f"   ✓ Compiled: {details['compiled_files']}")
        print(f"   ✓ Failed: {details['failed_files']}")

        return ValidationResult(
            success=success,
            message=f"Compiled {details['compiled_files']} of {details['total_files']} files successfully",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def _compile_single_file(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Compile a single Python file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, str(file_path), 'exec')
            return True, None
        except SyntaxError as e:
            return False, f"SyntaxError at line {e.lineno}: {e.msg}"
        except IndentationError as e:
            return False, f"IndentationError at line {e.lineno}: {e.msg}"
        except TabError as e:
            return False, f"TabError at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)

    def validate_syntax(self) -> ValidationResult:
        """
        Validate Python syntax using AST parsing.
        """
        print("\n[2/9] Validating syntax with AST...")

        errors = []
        warnings = []
        details = {
            'total_files': 0,
            'valid_syntax': 0,
            'invalid_syntax': 0,
            'invalid_details': []
        }

        python_files = list(self.project_root.rglob('*.py'))
        python_files = [f for f in python_files if 'venv' not in str(f) and 'env' not in str(f)]
        details['total_files'] = len(python_files)

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                ast.parse(source, filename=str(file_path))
                details['valid_syntax'] += 1
            except SyntaxError as e:
                details['invalid_syntax'] += 1
                error_msg = f"SyntaxError in {file_path}: {e.msg} (line {e.lineno})"
                details['invalid_details'].append(error_msg)
                errors.append(error_msg)
            except Exception as e:
                details['invalid_syntax'] += 1
                error_msg = f"Error in {file_path}: {str(e)}"
                details['invalid_details'].append(error_msg)
                errors.append(error_msg)

        success = details['invalid_syntax'] == 0

        print(f"   ✓ Total files: {details['total_files']}")
        print(f"   ✓ Valid syntax: {details['valid_syntax']}")
        print(f"   ✓ Invalid syntax: {details['invalid_syntax']}")

        return ValidationResult(
            success=success,
            message=f"AST validation: {details['valid_syntax']} valid, {details['invalid_syntax']} invalid",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_imports(self) -> ValidationResult:
        """
        Validate all imports resolve correctly.
        """
        print("\n[3/9] Validating imports...")

        errors = []
        warnings = []
        details = {
            'total_imports': 0,
            'resolved_imports': 0,
            'failed_imports': 0,
            'failed_details': []
        }

        # Add project root to path
        sys.path.insert(0, str(self.project_root))

        python_files = list(self.project_root.rglob('*.py'))
        python_files = [f for f in python_files if 'venv' not in str(f) and 'env' not in str(f)]

        imported_modules = set()

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                tree = ast.parse(source, filename=str(file_path))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imported_modules.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imported_modules.add(node.module.split('.')[0])

            except Exception as e:
                warnings.append(f"Could not parse imports in {file_path}: {e}")

        details['total_imports'] = len(imported_modules)

        for module_name in imported_modules:
            try:
                importlib.import_module(module_name)
                details['resolved_imports'] += 1
            except ImportError as e:
                # Skip built-in modules and relative imports
                if module_name in sys.builtin_module_names:
                    details['resolved_imports'] += 1
                elif module_name.startswith('apps.') or module_name.startswith('core.'):
                    try:
                        importlib.import_module(module_name)
                        details['resolved_imports'] += 1
                    except ImportError as e2:
                        details['failed_imports'] += 1
                        details['failed_details'].append(f"{module_name}: {str(e2)}")
                        errors.append(f"Import error: {module_name} - {str(e2)}")
                else:
                    details['failed_imports'] += 1
                    details['failed_details'].append(f"{module_name}: {str(e)}")
                    errors.append(f"Import error: {module_name} - {str(e)}")

        success = details['failed_imports'] == 0

        print(f"   ✓ Total imports: {details['total_imports']}")
        print(f"   ✓ Resolved: {details['resolved_imports']}")
        print(f"   ✓ Failed: {details['failed_imports']}")

        return ValidationResult(
            success=success,
            message=f"Import validation: {details['resolved_imports']} resolved, {details['failed_imports']} failed",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_dependencies(self) -> ValidationResult:
        """
        Validate all dependencies are installed.
        """
        print("\n[4/9] Validating dependencies...")

        errors = []
        warnings = []
        details = {
            'required_packages': [],
            'missing_packages': [],
            'installed_packages': [],
        }

        requirements_file = self.project_root / 'requirements.txt'

        if not requirements_file.exists():
            warnings.append("requirements.txt not found")
            return ValidationResult(
                success=False,
                message="requirements.txt not found",
                details=details,
                errors=errors,
                warnings=warnings
            )

        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name
                    package = line.split('==')[0].split('>=')[0].split('<=')[0].split('<')[0].strip()
                    details['required_packages'].append(package)

        import pkg_resources

        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        details['installed_packages'] = list(installed_packages)

        for package in details['required_packages']:
            if package.lower() not in installed_packages:
                details['missing_packages'].append(package)
                errors.append(f"Missing package: {package}")

        success = len(details['missing_packages']) == 0

        print(f"   ✓ Required packages: {len(details['required_packages'])}")
        print(f"   ✓ Installed packages: {len(details['installed_packages'])}")
        print(f"   ✓ Missing packages: {len(details['missing_packages'])}")

        return ValidationResult(
            success=success,
            message=f"Dependency validation: {len(details['required_packages'])} required, {len(details['missing_packages'])} missing",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_django_system(self) -> ValidationResult:
        """
        Run Django system checks.
        """
        print("\n[5/9] Validating Django system...")

        errors = []
        warnings = []
        details = {
            'checks': [],
            'output': '',
        }

        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

            result = subprocess.run(
                [sys.executable, 'manage.py', 'check'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )

            details['output'] = result.stdout + result.stderr

            if result.returncode == 0:
                details['checks'].append('System check passed')
            else:
                errors.append(f"Django check failed: {result.stderr}")

        except Exception as e:
            errors.append(f"Failed to run Django check: {str(e)}")
            details['output'] = str(e)

        success = len(errors) == 0

        print(f"   ✓ System check: {'PASSED' if success else 'FAILED'}")

        return ValidationResult(
            success=success,
            message="Django system check completed" if success else "Django system check failed",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_migrations(self) -> ValidationResult:
        """
        Validate Django migrations.
        """
        print("\n[6/9] Validating migrations...")

        errors = []
        warnings = []
        details = {
            'makemigrations_output': '',
            'migration_plan': [],
            'has_changes': False,
        }

        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

            # Check for migration changes
            result = subprocess.run(
                [sys.executable, 'manage.py', 'makemigrations', '--dry-run'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )

            details['makemigrations_output'] = result.stdout + result.stderr

            if 'No changes detected' in result.stdout:
                details['has_changes'] = False
            else:
                details['has_changes'] = True
                warnings.append('Model changes detected - migrations need to be created')

            # Get migration plan
            plan_result = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--plan'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )

            details['migration_plan'] = plan_result.stdout.strip().split('\n')

        except Exception as e:
            errors.append(f"Failed to validate migrations: {str(e)}")

        success = len(errors) == 0

        print(f"   ✓ Migration changes: {'Yes' if details['has_changes'] else 'No'}")

        return ValidationResult(
            success=success,
            message="Migration validation completed" if success else "Migration validation failed",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def detect_circular_imports(self) -> ValidationResult:
        """
        Detect circular imports in the repository.
        """
        print("\n[7/9] Detecting circular imports...")

        errors = []
        warnings = []
        details = {
            'modules_checked': 0,
            'circular_imports': [],
            'import_graph': {}
        }

        python_files = list(self.project_root.rglob('*.py'))
        python_files = [f for f in python_files if 'venv' not in str(f) and 'env' not in str(f)]

        import_graph = {}

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                tree = ast.parse(source, filename=str(file_path))

                module_name = str(file_path.relative_to(self.project_root)).replace('\\', '/').replace('/', '.').replace('.py', '')

                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                import_graph[module_name] = imports
                details['modules_checked'] += 1

            except Exception as e:
                warnings.append(f"Could not parse imports in {file_path}: {e}")

        details['import_graph'] = import_graph

        # Simple circular import detection (not full graph traversal)
        for module, imports in import_graph.items():
            for imp in imports:
                if imp in import_graph and module in import_graph.get(imp, []):
                    circular = f"{module} <-> {imp}"
                    if circular not in details['circular_imports']:
                        details['circular_imports'].append(circular)
                        warnings.append(f"Potential circular import: {circular}")

        success = len(details['circular_imports']) == 0

        print(f"   ✓ Modules checked: {details['modules_checked']}")
        print(f"   ✓ Circular imports found: {len(details['circular_imports'])}")

        return ValidationResult(
            success=success,
            message=f"Circular import detection: {len(details['circular_imports'])} found" if not success else "No circular imports detected",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_templates(self) -> ValidationResult:
        """
        Validate Django templates.
        """
        print("\n[8/9] Validating templates...")

        errors = []
        warnings = []
        details = {
            'total_templates': 0,
            'valid_templates': 0,
            'invalid_templates': 0,
            'invalid_details': []
        }

        templates_dir = self.project_root / 'templates'

        if not templates_dir.exists():
            warnings.append("templates directory not found")
            return ValidationResult(
                success=False,
                message="templates directory not found",
                details=details,
                errors=errors,
                warnings=warnings
            )

        try:
            from django.template import Template, TemplateSyntaxError
            from django.conf import settings

            # Initialize Django if not already
            if not settings.configured:
                settings.configure()

            template_files = list(templates_dir.rglob('*.html'))
            details['total_templates'] = len(template_files)

            for template_file in template_files:
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    Template(content)
                    details['valid_templates'] += 1
                except TemplateSyntaxError as e:
                    details['invalid_templates'] += 1
                    error_msg = f"Template error in {template_file}: {e}"
                    details['invalid_details'].append(error_msg)
                    errors.append(error_msg)
                except Exception as e:
                    details['invalid_templates'] += 1
                    error_msg = f"Error in {template_file}: {str(e)}"
                    details['invalid_details'].append(error_msg)
                    errors.append(error_msg)

        except Exception as e:
            errors.append(f"Failed to validate templates: {str(e)}")
            details['error'] = str(e)

        success = details['invalid_templates'] == 0

        print(f"   ✓ Total templates: {details['total_templates']}")
        print(f"   ✓ Valid templates: {details['valid_templates']}")
        print(f"   ✓ Invalid templates: {details['invalid_templates']}")

        return ValidationResult(
            success=success,
            message=f"Template validation: {details['valid_templates']} valid, {details['invalid_templates']} invalid",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def validate_static_files(self) -> ValidationResult:
        """
        Validate static files.
        """
        print("\n[9/9] Validating static files...")

        errors = []
        warnings = []
        details = {
            'static_dirs': [],
            'total_files': 0,
            'css_files': 0,
            'js_files': 0,
            'image_files': 0,
            'other_files': 0,
            'missing_files': [],
        }

        static_dir = self.project_root / 'static'

        if not static_dir.exists():
            warnings.append("static directory not found")
            return ValidationResult(
                success=False,
                message="static directory not found",
                details=details,
                errors=errors,
                warnings=warnings
            )

        # Check static directories
        details['static_dirs'] = [d.name for d in static_dir.iterdir() if d.is_dir()]

        for file_path in static_dir.rglob('*'):
            if file_path.is_file():
                details['total_files'] += 1
                ext = file_path.suffix.lower()
                if ext == '.css':
                    details['css_files'] += 1
                elif ext == '.js':
                    details['js_files'] += 1
                elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'):
                    details['image_files'] += 1
                else:
                    details['other_files'] += 1

        # Check for required static files
        required_files = [
            'css/style.css',
            'css/dashboard.css',
            'js/main.js',
            'js/auth.js',
        ]

        for required_file in required_files:
            if not (static_dir / required_file).exists():
                details['missing_files'].append(required_file)
                errors.append(f"Required static file not found: {required_file}")

        success = len(details['missing_files']) == 0

        print(f"   ✓ Total static files: {details['total_files']}")
        print(f"   ✓ CSS: {details['css_files']}, JS: {details['js_files']}, Images: {details['image_files']}")
        print(f"   ✓ Missing required files: {len(details['missing_files'])}")

        return ValidationResult(
            success=success,
            message=f"Static files validation: {details['total_files']} files found",
            details=details,
            errors=errors,
            warnings=warnings
        )

    def get_summary(self) -> ValidationResult:
        """
        Get comprehensive validation summary.
        """
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        all_errors = []
        all_warnings = []
        details = {
            'checks': {},
            'total_checks': len(self.results),
            'passed_checks': 0,
            'failed_checks': 0,
            'validation_time': datetime.now().isoformat(),
            'project_root': str(self.project_root),
        }

        for check_name, result in self.results.items():
            details['checks'][check_name] = {
                'success': result.success,
                'message': result.message,
                'errors_count': len(result.errors),
                'warnings_count': len(result.warnings),
            }

            if result.success:
                details['passed_checks'] += 1
            else:
                details['failed_checks'] += 1

            if result.errors:
                all_errors.extend([f"[{check_name}] {e}" for e in result.errors])
            if result.warnings:
                all_warnings.extend([f"[{check_name}] {w}" for w in result.warnings])

        overall_success = details['failed_checks'] == 0

        print(f"Total Checks: {details['total_checks']}")
        print(f"Passed: {details['passed_checks']}")
        print(f"Failed: {details['failed_checks']}")
        print(f"Overall Status: {'✅ PASSED' if overall_success else '❌ FAILED'}")

        if all_errors:
            print("\nErrors:")
            for error in all_errors:
                print(f"  ❌ {error}")

        if all_warnings:
            print("\nWarnings:")
            for warning in all_warnings:
                print(f"  ⚠️ {warning}")

        print("=" * 60)
        print(f"Validation completed at: {datetime.now().isoformat()}")
        print("=" * 60)

        return ValidationResult(
            success=overall_success,
            message="Repository validation completed" if overall_success else "Repository validation failed",
            details=details,
            errors=all_errors,
            warnings=all_warnings
        )


def main():
    """
    Entry point for the validation tool.
    """
    import argparse

    parser = argparse.ArgumentParser(description='FabricERP Repository Validator')
    parser.add_argument(
        '--project-root',
        type=str,
        help='Project root directory (default: current directory)',
        default=None
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output report file (JSON format)',
        default=None
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick validation (skip slow checks)',
        default=False
    )

    args = parser.parse_args()

    validator = RepositoryValidator(args.project_root)

    if args.quick:
        # Run only essential checks
        print("Running quick validation...")
        result = ValidationResult(
            success=False,
            message="Quick validation not fully implemented",
            details={'quick_mode': True}
        )
    else:
        result = validator.run_all()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\nReport saved to: {args.output}")

    return 0 if result.success else 1


if __name__ == '__main__':
    sys.exit(main())