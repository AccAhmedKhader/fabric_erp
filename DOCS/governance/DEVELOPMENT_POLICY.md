# FabricERP Enterprise

# Development Policy

Version: 1.0.0

Status: Official

Owner: Architecture Team

---

# Purpose

تهدف هذه السياسة إلى توحيد طريقة تطوير النظام.

أي مساهم فى المشروع يجب أن يلتزم بهذه الوثيقة.

---

# Development Philosophy

التطوير يتم وفق المبادئ التالية:

- Quality First
- Simplicity
- Maintainability
- Testability
- Security
- Performance
- Documentation

---

# Feature Development Lifecycle

كل Feature تمر بالمراحل التالية:

Business Requirement

↓

Analysis

↓

Architecture Review

↓

ADR (إن لزم)

↓

Implementation

↓

Tests

↓

Documentation

↓

Code Review

↓

Merge

↓

Release

---

# Definition of Feature

كل Feature يجب أن تكون:

- مستقلة
- قابلة للاختبار
- موثقة
- لا تكسر النظام

---

# Architecture Compliance

لا يسمح بإضافة Feature تخالف:

ARCHITECTURE.md

أو

ARCHITECTURE_PRINCIPLES.md

---

# Business Logic

جميع Business Rules

داخل Services فقط.

---

# Database

لا يتم تعديل قاعدة البيانات مباشرة.

جميع التعديلات من خلال Migrations.

---

# Dependencies

قبل إضافة مكتبة جديدة يجب:

- تقييمها
- مراجعة الترخيص
- مراجعة النشاط
- مراجعة الأمان

---

# Code Quality

كل كود جديد يجب أن يمر عبر:

- Ruff
- Black
- isort
- mypy
- pytest

---

# Documentation

لا تعتبر Feature مكتملة بدون:

- Documentation
- API
- Tests

---

# Technical Debt

أي Technical Debt يجب تسجيله فى Issue مع:

- السبب
- التأثير
- خطة المعالجة
- الموعد المتوقع