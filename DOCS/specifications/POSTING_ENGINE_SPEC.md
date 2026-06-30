# docs/specifications/POSTING_ENGINE_SPEC.md

# FabricERP Enterprise

# Posting Engine Specification

Version: 1.0.0

Status: Official Specification

Module: Accounting Core

Owner: Chief Software Architect

---

# Table of Contents

1. Introduction
2. Objectives
3. Design Principles
4. Responsibilities
5. Architecture
6. Posting Pipeline
7. Posting Sources
8. Journal Structure
9. Posting Rules
10. Validation Rules
11. Transaction Rules
12. Number Generation
13. Currency Handling
14. Cost Centers
15. Projects
16. Multi Company
17. Multi Branch
18. Reversing Entries
19. Error Handling
20. Events
21. Security
22. Performance
23. Audit Trail
24. APIs
25. Database Tables
26. Testing
27. Future Extensions

---

# 1. Introduction

Posting Engine هو القلب المحاسبى للنظام.

لا يسمح لأى Module بإنشاء قيود محاسبية بصورة مباشرة.

جميع القيود تمر حصرياً من خلال Posting Engine.

---

# 2. Objectives

يهدف المحرك إلى:

- ضمان صحة القيود المحاسبية.
- تطبيق نظام القيد المزدوج.
- منع القيود غير المتوازنة.
- توحيد منطق الترحيل.
- ضمان Atomicity.
- تسجيل Audit كامل.
- دعم التوسع.

---

# 3. Design Principles

✓ Single Entry Point

✓ Double Entry Accounting

✓ Immutable Journal

✓ Atomic Transactions

✓ Idempotent Posting

✓ Auditability

✓ Traceability

✓ High Performance

---

# 4. Responsibilities

Posting Engine مسئول عن:

- إنشاء القيود
- التحقق من الحسابات
- التحقق من العملات
- التحقق من مراكز التكلفة
- إنشاء أرقام القيود
- الترحيل للأستاذ العام
- تحديث الأرصدة
- إصدار الأحداث
- إنشاء Audit

---

# 5. High-Level Architecture

Source Module

↓

Posting Request

↓

Posting Validator

↓

Posting Service

↓

Journal Builder

↓

Journal Validator

↓

Posting Repository

↓

Database

↓

Domain Events

↓

Audit Trail

---

# 6. Posting Sources

يسمح فقط للوحدات التالية بطلب الترحيل:

Sales

Purchases

Inventory

Treasury

Assets

Payroll

Manufacturing

Opening Balance

General Journal

Year Closing

---

ولا يسمح بكتابة Journal مباشرة.

---

# 7. Journal Structure

Journal Header

↓

Journal Lines

↓

Ledger Entries

---

Journal Header

يتضمن

UUID

Journal Number

Company

Branch

Fiscal Year

Posting Date

Reference

Status

Currency

Exchange Rate

Created By

Approved By

Posted By

Posted At

---

Journal Line

يتضمن

Account

Debit

Credit

Currency

Cost Center

Project

Dimension

Description

Reference

---

# 8. Posting Pipeline

Posting يبدأ بالمراحل التالية:

1

Receive Request

↓

2

Validate Document

↓

3

Validate Workflow

↓

4

Validate Company

↓

5

Validate Fiscal Year

↓

6

Validate Accounts

↓

7

Validate Currency

↓

8

Validate Cost Centers

↓

9

Build Journal

↓

10

Validate Journal

↓

11

Assign Number

↓

12

Save Journal

↓

13

Post Ledger

↓

14

Update Balances

↓

15

Publish Events

↓

16

Write Audit

↓

17

Commit Transaction

---

إذا فشلت أى خطوة

Rollback بالكامل.

---

# 9. Journal Validation Rules

كل Journal يجب أن يحقق:

Debit = Credit

على مستوى Header.

---

لا يسمح:

Debit < 0

Credit < 0

---

لا يسمح

بسطر

Debit و Credit

معاً.

---

لا يسمح

Journal بدون Lines.

---

لا يسمح

Journal بدون Company.

---

لا يسمح

Journal بدون Fiscal Year.

---

# 10. Account Validation

كل حساب يجب أن يكون:

Active

Posting Allowed

Company Match

ليس Header Account

ليس Deleted

ليس Frozen

---

# 11. Fiscal Validation

تاريخ القيد يجب أن يكون:

داخل سنة مالية مفتوحة.

---

لا يسمح بالترحيل

فى فترة مغلقة.

---

# 12. Currency Rules

يدعم النظام:

Base Currency

Transaction Currency

Reporting Currency

---

كل Journal يحتفظ بـ

Original Amount

Base Amount

Exchange Rate

---

# 13. Exchange Rates

يتم قراءة سعر الصرف من

Exchange Rate Service.

---

يسجل السعر المستخدم داخل القيد.

---

لا يتغير بعد الترحيل.

---

# 14. Cost Centers

إذا كان الحساب

Requires Cost Center

فيجب إدخال Cost Center.

---

# 15. Project Accounting

الحسابات التى تدعم Project

تتطلب Project Code.

---

# 16. Posting Transaction

جميع عمليات Posting

داخل

transaction.atomic()

---

ولا يسمح

Partial Commit.

---

# 17. Numbering

رقم القيد

يصدر فقط من

Numbering Engine.

---

مثال

JV-2026-000123

---

# 18. Ledger Update

بعد نجاح Journal

يتم تحديث:

General Ledger

Account Balance

Period Balance

Daily Balance

Monthly Balance

Year Balance

---

# 19. Reversing Entries

التعديل

لا يتم على Journal.

بل

Reverse Journal

↓

New Journal

---

# 20. Audit Trail

يسجل

User

IP

Company

Date

Old State

New State

Reference

Reason

---

# 21. Domain Events

بعد نجاح Posting

تصدر الأحداث التالية:

JournalPosted

LedgerUpdated

AccountBalanceChanged

FinancialTransactionCompleted

AuditCreated

---

# 22. Error Codes

POST001

Unbalanced Journal

---

POST002

Account Not Found

---

POST003

Account Frozen

---

POST004

Fiscal Period Closed

---

POST005

Currency Missing

---

POST006

Invalid Exchange Rate

---

POST007

Duplicate Posting

---

POST008

Workflow Not Approved

---

POST009

Number Generation Failed

---

POST010

Database Error

---

# 23. API Contract

POST

/api/v1/accounting/post

Request

Document UUID

Response

Journal UUID

Status

Posting Number

---

# 24. Database Tables

journal_headers

journal_lines

ledger_entries

posting_batches

posting_logs

posting_errors

posting_queue

---

# 25. Performance Targets

Posting Time

<300 ms

---

10,000

Journal Lines

فى Transaction واحدة.

---

يدعم

Bulk Posting.

---

# 26. Security

Posting يحتاج صلاحية

ACCOUNTING_POST

---

لا يسمح بتجاوز Workflow.

---

لا يسمح بالتعديل بعد Posting.

---

# 27. Logging

يسجل:

Execution Time

SQL Count

User

Journal

Module

Errors

---

# 28. Testing

Unit Tests

Integration Tests

Concurrency Tests

Rollback Tests

Performance Tests

Stress Tests

Recovery Tests

---

# 29. Future Roadmap

Distributed Posting

Async Posting

Event Bus

Kafka Integration

Multi Ledger

Parallel Posting

Financial Dimensions

AI Validation

---

# Sequence Diagram

Sales Invoice

↓

Posting Service

↓

Journal Builder

↓

Journal Validator

↓

Numbering Engine

↓

Journal Repository

↓

Ledger

↓

Events

↓

Audit

↓

Commit

---

# Non-Negotiable Rules

✓ لا يوجد Posting خارج Posting Engine.

✓ لا يوجد Journal غير متوازن.

✓ لا يوجد تعديل بعد Posting.

✓ لا يوجد حذف للقيود.

✓ جميع العمليات داخل Transaction.

✓ جميع القيود تمر بـ Validation.

✓ جميع القيود تسجل Audit.

✓ جميع القيود تصدر Events.

✓ جميع القيود تستخدم Numbering Engine.

---

End of Document