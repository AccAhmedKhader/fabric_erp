# FabricERP Enterprise
# Coding Standards

Version: 1.0.0

Status: Official Standard

Owner: Architecture Team

---

# Table of Contents

1. Introduction
2. Philosophy
3. General Principles
4. Software Engineering Principles
5. Clean Architecture Rules
6. Project Structure
7. Folder Structure
8. Naming Conventions
9. Python Standards
10. Django Standards
11. Service Layer Standards
12. Repository Layer Standards
13. Domain Model Standards
14. API Standards
15. Database Standards
16. Security Standards
17. Logging Standards
18. Error Handling Standards
19. Testing Standards
20. Performance Standards
21. Documentation Standards
22. Git Standards
23. Code Review Standards
24. Pull Request Standards
25. Release Standards

---

# 1. Introduction

هذا المستند هو المرجع الرسمي لجميع المطورين العاملين على مشروع FabricERP Enterprise.

لا يجوز كتابة أي كود يخالف هذا المستند إلا بعد إصدار Architecture Decision Record (ADR).

تعتبر هذه الوثيقة جزءًا من Architecture Governance الخاصة بالمشروع.

---

# 2. Coding Philosophy

هدفنا ليس كتابة كود يعمل فقط.

هدفنا كتابة كود:

- واضح
- قابل للصيانة
- قابل للاختبار
- قابل للتوسع
- آمن
- سريع
- سهل القراءة

أي كود يصعب فهمه يعتبر كودًا سيئًا حتى لو كان صحيحًا.

---

# 3. General Principles

يجب الالتزام بالمبادئ التالية:

SOLID

DRY

KISS

YAGNI

Separation of Concerns

Single Responsibility

Dependency Injection

Explicit Business Rules

Composition over Inheritance

Fail Fast

Immutable Financial Records

Idempotent Operations

---

# 4. Software Engineering Principles

## Readability First

الكود يقرأ أكثر مما يُكتب.

سهولة القراءة أهم من اختصار عدد الأسطر.

يفضل:

```python
if customer.is_blocked:
    raise CustomerBlockedError()
```

ولا يفضل:

```python
if not customer.active:
    ...
```

إذا كان الاسم لا يوضح السبب الحقيقي.

---

## Explicit Better Than Implicit

لا تعتمد على السلوك الضمني.

اجعل الكود واضحًا.

---

## One Responsibility

كل Class له مسئولية واحدة.

كل Function لها مسئولية واحدة.

كل Module له مسئولية واحدة.

---

## Small Functions

يفضل أن تكون الدوال قصيرة.

الحد الأقصى المقترح:

40 سطرًا.

إذا زادت عن ذلك يجب التفكير في تقسيمها.

---

## No Business Logic in Views

الـ Views مسئولة فقط عن:

- استقبال الطلب
- التحقق من الصلاحيات
- استدعاء Service
- إعادة Response

أي Business Logic داخل View ممنوع.

مثال خاطئ

```python
invoice.total = invoice.items.aggregate(...)
invoice.save()
```

الصحيح

```python
InvoiceService.calculate_total(invoice)
```

---

## Fat Services

Business Logic

↓

Services

وليس

Views

ولا

Models

---

# 5. Clean Architecture Rules

Architecture

Presentation

↓

Application

↓

Domain

↓

Infrastructure

↓

Database

---

يسمح بالاعتماد:

Presentation

↓

Application

↓

Repository

↓

ORM

---

يمنع:

Repository

↓

View

---

Model

↓

View

---

Template

↓

Business Logic

---

# 6. Project Structure

كل App يجب أن يكون بالشكل التالي

apps/

inventory/

models/

services/

repositories/

selectors/

validators/

permissions/

signals/

serializers/

api/

views/

urls/

tests/

management/

migrations/

templates/

admin.py

apps.py

---

كل App مسئول عن نفسه بالكامل.

ولا يجوز استدعاء قاعدة البيانات مباشرة من App آخر.

---

# 7. Folder Standards

models/

Models فقط

---

services/

Business Logic فقط

---

repositories/

Database Access فقط

---

selectors/

Read Queries فقط

---

validators/

Business Validation فقط

---

signals/

Event Hooks فقط

---

tests/

جميع الاختبارات

---

api/

REST API

---

templates/

HTML

---

management/

Management Commands

---

# 8. Naming Conventions

Classes

PascalCase

```python
SalesInvoiceService
```

Models

PascalCase

```python
Customer
```

Functions

snake_case

```python
calculate_total()
```

Variables

snake_case

```python
customer_balance
```

Constants

UPPER_CASE

```python
MAX_RETRY_COUNT
```

Private Methods

```python
_prepare_lines()
```

Boolean

يبدأ بـ

is_

has_

can_

should_

مثال

```python
is_posted

has_balance

can_edit

should_post
```

---

# 9. File Naming

صحيح

```text
invoice_service.py

posting_engine.py

customer_repository.py
```

خطأ

```text
InvoiceService.py

InvoiceSERVICE.py

service.py
```

---

# 10. Import Rules

ترتيب الـ Imports

Standard Library

↓

Third Party

↓

Project Apps

↓

Local Module

مثال

```python
from decimal import Decimal

from django.db import transaction

from apps.sales.models import Invoice

from .services import PostingService
```

---

# 11. Typing

إلزامي استخدام Type Hints.

مثال

```python
def calculate_total(invoice: Invoice) -> Decimal:
```

ولا يفضل

```python
def calculate_total(invoice):
```

---

# 12. Docstrings

كل Public Class

و

كل Public Function

يجب أن تحتوي على Docstring.

مثال

```python
def post(self):
    """
    Post invoice to general ledger.

    Raises:
        PostingError

    Returns:
        JournalEntry
    """
```

---

# End of Part 1# 13. Python Standards

## 13.1 Python Version

الإصدار الرسمي للمشروع

Python 3.13+

يحظر استخدام أى مكتبات غير متوافقة مع الإصدار الرسمي.

---

## 13.2 Style Guide

يلتزم المشروع بالكامل بـ

PEP8

PEP257

PEP484

PEP561

---

## 13.3 Line Length

الحد الأقصى

```text
100 characters
```

يسمح حتى

120

فى الحالات الاستثنائية فقط.

---

## 13.4 Indentation

استخدم

4 Spaces

ولا تستخدم

Tabs

---

## 13.5 Encoding

جميع الملفات

UTF-8

---

## 13.6 Quotes

يفضل

Double Quotes

```python
customer.name = "Ahmed"
```

---

## 13.7 F Strings

يفضل دائما

```python
message = f"Invoice {invoice.number} posted."
```

ولا يفضل

```python
"Invoice %s" % invoice.number
```

---

## 13.8 Enumerations

يجب استخدام Enum

بدلاً من Magic Strings

خطأ

```python
status = "POSTED"
```

صحيح

```python
class InvoiceStatus(StrEnum):
    DRAFT = "draft"
    POSTED = "posted"
```

---

## 13.9 Dataclasses

تستخدم فى

Value Objects

DTO

Configuration Objects

ولا تستخدم مع Django Models.

---

## 13.10 Context Managers

يفضل

```python
with transaction.atomic():
```

بدلاً من

فتح وإغلاق Transaction يدوياً.

---

## 13.11 Exceptions

لا تستخدم

```python
except:
```

مطلقاً.

الصحيح

```python
except ValidationError:
```

---

## 13.12 Mutable Defaults

ممنوع

```python
def test(items=[]):
```

الصحيح

```python
def test(items=None):
```

---

## 13.13 Global Variables

ممنوعة.

---

## 13.14 Magic Numbers

خطأ

```python
if discount > 25:
```

الصحيح

```python
MAX_ALLOWED_DISCOUNT = 25
```

---

## 13.15 Comprehension

يفضل

```python
active = [c for c in customers if c.active]
```

---

## 13.16 Lambda

تستخدم فقط عندما تكون بسيطة جداً.

---

## 13.17 Walrus Operator

يستخدم عند الحاجة فقط.

---

## 13.18 Match Statement

يفضل فى Python الحديثة

```python
match status:
```

بدلاً من

سلسلة طويلة من

if elif

---

# 14. Django Standards

## 14.1 Django Apps

كل Module عبارة عن App مستقلة.

مثال

```text
sales

inventory

accounting

treasury

crm
```

---

## 14.2 Fat Models ممنوع

لا يجوز وضع Business Logic داخل Model.

خطأ

```python
class Invoice(models.Model):

    def post(self):
```

الصحيح

```python
InvoicePostingService.post(invoice)
```

---

## 14.3 Views

Views يجب أن تكون صغيرة.

يفضل ألا تتجاوز

50 سطر.

---

## 14.4 CBV

يفضل استخدام

Class Based Views

كلما أمكن.

---

## 14.5 FBV

تستخدم فقط للحالات الصغيرة.

---

## 14.6 Serializers

مسئوليتها

Validation

Transformation

ولا تحتوى على Business Logic.

---

## 14.7 Managers

Managers

للـ Query فقط.

ولا تحتوى على Business Logic.

---

## 14.8 QuerySets

يفضل

Custom QuerySet

بدلاً من تكرار Filters.

---

## 14.9 Signals

Signals تستخدم فقط للأحداث الثانوية.

ولا تستخدم فى

Posting

ولا

Inventory

ولا

Workflow

---

## 14.10 Migrations

لا تعدل Migration قديمة بعد نشرها.

---

## 14.11 Settings

جميع الإعدادات الحساسة داخل

.env

---

## 14.12 Secrets

ممنوع حفظ

Passwords

Tokens

Secrets

داخل Git.

---

# 15. Service Layer Standards

كل Business Logic داخل Services.

مثال

```python
SalesOrderService

InvoicePostingService

InventoryReservationService

PaymentService

JournalService
```

---

كل Service يجب أن يحقق:

Single Responsibility

---

## Services ممنوع أن

ترجع HttpResponse

---

تقرأ Request مباشرة

---

تعتمد على Template

---

تكتب HTML

---

# 16. Repository Standards

Repository مسئول فقط عن

CRUD

Queries

Persistence

ولا يحتوى على

Business Rules

---

مثال

```python
CustomerRepository

InvoiceRepository

WarehouseRepository
```

---

يفضل

```python
customer_repository.get_active()
```

بدلاً من

```python
Customer.objects.filter(active=True)
```

داخل Services.

---

# 17. Selectors

Selectors خاصة بالقراءة فقط.

مثال

```python
SalesDashboardSelector

CustomerBalanceSelector
```

---

ولا تقوم بكتابة بيانات.

---

# 18. Validators

كل Validation معقد

ينقل إلى

validators/

ولا يكتب داخل View.

---

مثال

```python
CreditLimitValidator

PostingValidator

WarehouseValidator
```

---

# 19. DTO

عند نقل البيانات بين الطبقات

يفضل استخدام DTO.

---

# 20. Domain Events

كل حدث مهم يصدر Event.

مثال

```text
Invoice Posted

↓

Journal Posted

↓

Stock Updated

↓

Customer Balance Updated

↓

Notification Sent
```

---

الأحداث يجب أن تكون

Idempotent

---

وقابلة لإعادة التنفيذ.

---

# 21. Transactions

كل عملية مالية

داخل

```python
transaction.atomic()
```

إلزامياً.

---

ولا يسمح بوجود

Nested Transactions

بدون سبب واضح.

---

# 22. Decimal

جميع العمليات المالية

تستخدم

Decimal

ولا تستخدم

float

مطلقاً.

خطأ

```python
price = 10.55
```

الصحيح

```python
price = Decimal("10.55")
```

---

# 23. Date & Time

يستخدم

timezone.now()

ولا يستخدم

datetime.now()

مباشرة.

---

# 24. UUID

جميع الجداول الأساسية

تستخدم

UUID

كمعرف داخلى.

أما أرقام المستندات

فتصدر من

Numbering Engine.

---

# 25. Soft Delete

لا يستخدم

delete()

مباشرة.

بل

```python
soft_delete()
```

مع الاحتفاظ بالسجل.

---

# 26. Audit Trail

كل تعديل

يسجل:

User

Timestamp

Old Value

New Value

IP Address

Reason

إذا وجد.

---

# End of Part 2# 27. Database Standards

## 27.1 Database Engine

يعتمد FabricERP على:

- PostgreSQL (Production)
- SQLite (Development فقط)

يمنع استخدام SQLite في بيئة الإنتاج.

---

## 27.2 Naming Convention

### Tables

snake_case

مثال

```text
sales_invoice

journal_entry

inventory_transaction
```

---

### Columns

snake_case

```text
customer_id

created_at

posted_at

updated_by
```

---

### Primary Key

جميع الجداول تستخدم

```python
id = models.UUIDField(...)
```

ولا يستخدم Auto Increment كمفتاح أساسي.

---

## 27.3 Required Columns

كل جدول رئيسى يجب أن يحتوى على:

```text
id

company_id

branch_id

created_at

updated_at

created_by

updated_by

is_deleted

deleted_at

version
```

---

## 27.4 Foreign Keys

يستخدم دائماً

PROTECT

للبيانات المالية.

مثال

```python
on_delete=models.PROTECT
```

ويمنع

CASCADE

فى القيود المحاسبية.

---

## 27.5 Decimal Fields

جميع القيم المالية

```python
DecimalField(
    max_digits=19,
    decimal_places=4
)
```

---

## 27.6 Monetary Precision

يتم التقريب حسب إعدادات الشركة.

ولا يتم استخدام round()

داخل Business Logic.

---

## 27.7 Indexes

يجب إنشاء Index لكل:

Foreign Key

Number

Code

Status

Date

Company

Branch

---

## 27.8 Composite Indexes

مثال

```python
(company, number)

(company, code)

(company, status)
```

---

## 27.9 Constraints

يفضل استخدام

UniqueConstraint

CheckConstraint

---

مثال

```python
balance >= 0
```

---

## 27.10 Data Integrity

لا يسمح بحذف:

Journal

Posted Invoice

Inventory Transaction

بعد الترحيل.

---

# 28. API Standards

يعتمد المشروع على

REST API

---

## URL Style

```text
/api/v1/customers/

/api/v1/invoices/

/api/v1/journals/
```

---

## Versioning

كل API

تبدأ بـ

```text
v1
```

---

## Methods

GET

قراءة

POST

إنشاء

PUT

استبدال

PATCH

تعديل

DELETE

Soft Delete فقط

---

## Response Format

```json
{
    "success": true,
    "data": {},
    "message": "",
    "errors": []
}
```

---

## Pagination

إلزامية

فى جميع Lists.

---

## Filtering

يستخدم

django-filter

---

## Sorting

عن طريق

ordering

---

## Searching

عن طريق

search

---

## API Documentation

OpenAPI

Swagger

إلزامية.

---

# 29. Authentication Standards

يعتمد المشروع على

Django Authentication

---

يستخدم

JWT

للـ API.

---

Passwords

تخزن

Hash فقط.

---

Password Policy

Minimum 12 Characters

Uppercase

Lowercase

Numbers

Special Characters

---

Session Timeout

Configurable

---

# 30. Authorization Standards

يعتمد المشروع على

RBAC

Role Based Access Control

---

Permissions

Module

↓

Action

↓

Object

---

مثال

```text
Sales

Create

Read

Update

Delete

Approve

Post

Cancel

Print

Export
```

---

كل عملية

تراجع الصلاحيات.

---

# 31. Security Standards

المشروع يلتزم بـ

OWASP Top 10

---

## SQL Injection

ممنوع

Raw SQL

إلا عند الضرورة.

---

## XSS

يستخدم

Auto Escape

فى Templates.

---

## CSRF

مفعل دائماً.

---

## Secrets

داخل

.env

فقط.

---

## Encryption

يستخدم

HTTPS

فى الإنتاج.

---

Sensitive Data

يمكن تشفيرها.

---

# 32. Logging Standards

يعتمد المشروع على

Python Logging

---

أنواع Logs

Application

Audit

Security

Performance

System

---

Log Levels

DEBUG

INFO

WARNING

ERROR

CRITICAL

---

يمنع

print()

داخل المشروع.

---

# 33. Error Handling

كل Exceptions

مخصصة.

مثال

```python
PostingError

InventoryError

CreditLimitError

WorkflowError
```

---

ولا يستخدم

```python
raise Exception()
```

---

# 34. Performance Standards

يمنع

N+1 Queries

---

يفضل

select_related()

prefetch_related()

---

Bulk Operations

عند إدخال بيانات كثيرة.

---

Pagination

إلزامية.

---

Query Count

يراجع أثناء Code Review.

---

# 35. Cache Standards

Redis

هو Cache الرسمى.

---

يتم Cache

Settings

Reference Data

Dashboard

Metadata

---

لا يتم Cache

Journal Posting

Financial Balances

Inventory Movement

---

# 36. Celery Standards

جميع العمليات الثقيلة

تنفذ بواسطة

Celery.

---

مثل

PDF

Excel

Email

Notifications

Large Reports

Imports

Exports

---

كل Task

Idempotent

---

# 37. Testing Standards

كل Feature

لابد أن تمتلك Tests.

---

أنواع الاختبارات

Unit

Integration

API

Performance

Security

End-to-End

---

Minimum Coverage

90%

---

Factories

بدلاً من Fixtures

كلما أمكن.

---

pytest

هو Framework الرسمى.

---

# 38. Git Standards

Branches

main

develop

feature/*

release/*

hotfix/*

---

Commit Style

يفضل

Conventional Commits

---

مثال

```text
feat:

fix:

refactor:

docs:

test:

perf:

chore:
```

---

# 39. Pull Request Standards

كل Pull Request

يجب أن يحتوى على

Description

Issue

Screenshots (إن وجدت)

Tests

Migration Notes

---

لا يتم Merge

قبل

Code Review

ومرور جميع الاختبارات.

---

# 40. Code Review Checklist

يجب مراجعة

✓ Architecture

✓ Naming

✓ Security

✓ Performance

✓ Tests

✓ Logging

✓ Transactions

✓ Documentation

✓ Type Hints

✓ Exceptions

✓ Permissions

✓ Migrations

✓ API

✓ SQL Queries

✓ Business Rules

---

# 41. Release Standards

كل Release

تشمل

Release Notes

Migration Guide

Rollback Plan

Database Backup

Tag

Version

---

Semantic Versioning

MAJOR.MINOR.PATCH

---

# 42. Definition of Done

لا تعتبر المهمة منتهية إلا إذا:

✓ الكود مكتمل

✓ جميع الاختبارات نجحت

✓ Documentation محدثة

✓ Migration مضافة

✓ API موثقة

✓ Logging موجود

✓ Security Reviewed

✓ Performance Reviewed

✓ Code Reviewed

✓ Approved

---

# 43. Final Principles

FabricERP ليس مجرد مشروع Django.

بل منصة Enterprise.

كل سطر كود يجب أن يكون:

- واضحاً.
- قابلاً للاختبار.
- قابلاً للصيانة.
- قابلاً للتوسع.
- آمناً.
- موثقاً.
- متوافقاً مع المعمارية.

أي كود يخالف هذه الوثيقة يجب إعادة مراجعته قبل دمجه.

---

# Appendix A - Recommended Tools

Formatting

- black

Linting

- ruff

Import Sorting

- isort

Typing

- mypy

Security

- bandit

Dependency Audit

- pip-audit

Testing

- pytest

Coverage

- pytest-cov

Documentation

- mkdocs

Pre-Commit

- pre-commit

---

# Appendix B - Repository Quality Gates

لا يسمح بدمج أي Pull Request إذا فشل أحد الشروط التالية:

✓ جميع الاختبارات ناجحة.

✓ Coverage ≥ 90%.

✓ Ruff بدون أخطاء.

✓ Black بدون تعديلات.

✓ Mypy بدون أخطاء حرجة.

✓ Bandit بدون ثغرات عالية الخطورة.

✓ Migration صحيحة.

✓ Documentation محدثة.

✓ Code Review Approved.

---

# End of Coding Standards

Document Status: Official

Owner: Architecture Team

Review Cycle: Every Major Release

Next Review: Version 1.1