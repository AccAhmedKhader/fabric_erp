# FabricERP Repository Validation Tools

## Overview

This directory contains tools for validating the FabricERP repository.

## Repository Validator

The `repository_validator.py` script performs comprehensive validation of the entire repository.

### Features

- Python compilation validation
- Syntax validation using AST
- Import resolution validation
- Dependency completeness check
- Django system check
- Migration validation
- Circular import detection
- Template syntax validation
- Static files validation

### Usage

```bash
# Run all validations
python tools/repository_validator.py

# Run quick validation (skip slow checks)
python tools/repository_validator.py --quick

# Generate JSON report
python tools/repository_validator.py --output validation_report.json

# Validate specific project root
python tools/repository_validator.py --project-root /path/to/project