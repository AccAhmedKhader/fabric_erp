# FabricERP Enterprise

# Architecture Principles

Version: 1.0.0

Status: Official

Owner: Chief Software Architect

Priority: Mandatory

---

# Purpose

هذه الوثيقة تعتبر المرجع الأعلى لجميع القرارات المعمارية داخل مشروع FabricERP.

أي كود يخالف هذه المبادئ يجب رفضه أثناء Code Review ما لم يوجد Architecture Decision Record (ADR) يبرر ذلك.

---

# Architecture Philosophy

FabricERP ليس مجرد تطبيق Django.

FabricERP هو منصة Enterprise Business Platform.

لذلك فإن جميع القرارات يجب أن تحقق:

- Maintainability
- Scalability
- Testability
- Reliability
- Security
- Performance

ولا يسمح بالتضحية بأحد هذه المبادئ من أجل سرعة كتابة الكود.

---

# Principle 1

Business Logic Lives in Services

---

يحظر كتابة Business Logic داخل:

❌ Views

❌ Templates

❌ Django Models

❌ Serializers

Business Logic الوحيد يكون داخل:

```text
services/
```

مثال صحيح

```
InvoicePostingService

SalesOrderService

InventoryReservationService

CustomerCreditService
```

---

# Principle 2

Models Represent Data Only

---

Models تمثل البيانات فقط.

يسمح داخل Model بـ

Validation بسيطة

Properties

Relationships

ولا يسمح بكتابة:

Workflow

Posting

Calculations

Integration

Notifications

---

# Principle 3

Views Are Controllers

---

Views مسئولة عن:

Authentication

Authorization

Calling Services

Returning Response

ولا تقوم بـ:

Business Rules

Database Queries المعقدة

Financial Calculations

Posting

Workflow

---

# Principle 4

Repositories Own Database Access

---

الوصول إلى قاعدة البيانات يتم فقط من خلال

Repository Layer

ولا يسمح بكتابة

```python
Model.objects.filter(...)
```

داخل

Services

Views

Templates

---

# Principle 5

Selectors Own Read Operations

---

جميع عمليات القراءة المعقدة

داخل

selectors/

ولا يسمح باستخدامها فى الكتابة.

---

# Principle 6

Every Module Owns Its Domain

---

كل App تمتلك بياناتها الخاصة.

مثال

Sales

لا تقوم بتعديل

Inventory

مباشرة.

بل تستخدم

Service

أو

Domain Event

---

# Principle 7

Modules Communicate Through Contracts

---

التواصل بين Modules

لا يكون

Model → Model

بل

Service

↓

Domain Event

↓

API

---

# Principle 8

Posting Engine Is The Only Financial Writer

---

لا يسمح لأى Module

بإنشاء Journal Entries

إلا عن طريق

Posting Engine

---

حتى

Sales

Purchases

Treasury

Assets

Payroll

---

# Principle 9

Inventory Engine Owns Stock

---

لا يسمح لأى Module

بتعديل Quantity

مباشرة.

كل حركة تمر عبر

Inventory Engine

---

# Principle 10

Numbering Engine Owns Documents

---

جميع الأرقام تصدر من

Numbering Engine

مثل

Invoice

Voucher

Journal

Purchase Order

Receipt

Payment

---

ولا يسمح

بتوليد الأرقام يدوياً.

---

# Principle 11

Immutable Financial Records

---

بعد

Posting

لا يسمح بتعديل

Journal

ولا

Ledger

ولا

Inventory Transactions

---

التعديل يتم بواسطة

Reverse Entry

أو

Adjustment

---

# Principle 12

Everything Is Auditable

---

كل عملية يجب تسجيلها.

Audit يحتوى على:

User

Date

IP

Company

Branch

Old Value

New Value

Reason

---

# Principle 13

Soft Delete Only

---

لا يسمح باستخدام

delete()

فى البيانات التشغيلية.

يستخدم

Soft Delete

فقط.

---

# Principle 14

Atomic Transactions

---

كل عملية مالية

داخل

transaction.atomic()

---

ولا يسمح بوجود

Partial Commit

---

# Principle 15

Idempotent Operations

---

أى عملية

يمكن تنفيذها أكثر من مرة

دون فساد البيانات.

خصوصاً

Posting

Payment

Import

API

---

# Principle 16

Events Instead Of Direct Calls

---

يفضل

Invoice Posted

↓

Domain Event

↓

Inventory Updated

↓

Customer Updated

↓

Notification

بدلاً من

Service تستدعى خمس Services أخرى.

---

# Principle 17

Dependency Direction

---

الاتجاه الصحيح

Presentation

↓

Application

↓

Domain

↓

Infrastructure

---

ولا يسمح

بعكس الاتجاه.

---

# Principle 18

No Circular Dependency

---

لا يسمح بوجود

App A

↓

App B

↓

App A

---

# Principle 19

Explicit Is Better Than Implicit

---

اجعل الكود واضحاً.

ولا تعتمد على

Magic

Reflection

Hidden Behavior

---

# Principle 20

Single Source Of Truth

---

كل معلومة

لها مكان واحد فقط.

مثال

رصيد العميل

لا يخزن فى خمس جداول.

---

# Principle 21

Configuration Over Hard Coding

---

جميع

Settings

داخل

Configuration

ولا تستخدم

Magic Numbers

---

# Principle 22

Security First

---

كل API

تراجع

Authentication

Authorization

Permissions

Ownership

Company Isolation

---

# Principle 23

Company Isolation

---

لا يسمح

بظهور بيانات شركة

داخل شركة أخرى.

---

# Principle 24

Branch Isolation

---

كل فرع

يرى بياناته

إلا إذا كانت الصلاحيات تسمح.

---

# Principle 25

Performance Matters

---

يفضل

Bulk Operations

Caching

Indexes

Pagination

Streaming

---

ويمنع

N+1 Queries

---

# Principle 26

Database Integrity Before Speed

---

سلامة البيانات

أهم من

سرعة التنفيذ.

---

# Principle 27

Testing Is Mandatory

---

لا يسمح بإضافة Feature

بدون Tests.

---

# Principle 28

Documentation Is Part Of Development

---

الكود غير الموثق

كود غير مكتمل.

---

# Principle 29

Every Feature Requires ADR

إذا أثرت على:

Architecture

Database

Security

Workflow

Performance

Integration

---

# Principle 30

Backward Compatibility

---

يفضل

عدم كسر

API

ولا

Database

بين الإصدارات.

---

# Principle 31

Domain Before Framework

---

Django

هو مجرد Framework.

أما

Business Rules

فهى ملك

Domain.

---

# Principle 32

Enterprise Before Convenience

---

قد يكون الحل الأسرع

ليس هو الحل الصحيح.

يتم اختيار

الحل الذى يخدم

Enterprise Architecture

حتى لو كان أطول فى التنفيذ.

---

# Principle 33

No Technical Debt Without Approval

---

لا يسمح بإضافة

Temporary Code

Hack

Workaround

إلا بوجود:

Issue

ADR

Deadline

Owner

---

# Principle 34

Observability by Design

---

كل خدمة يجب أن توفر:

Structured Logging

Metrics

Tracing

Health Check

Correlation ID

حتى يسهل تتبع العمليات وتشخيص الأعطال في بيئات الإنتاج.

---

# Principle 35

API First

---

أي وظيفة أعمال جديدة يجب أن تكون قابلة للاستخدام عبر API موثقة، حتى لو كان لها واجهة ويب.

---

# Principle 36

Asynchronous by Design

---

العمليات الثقيلة مثل:

- إنشاء PDF
- تصدير Excel
- إرسال البريد
- الإشعارات
- إعادة بناء الفهارس

يجب تنفيذها عبر Background Jobs وليس أثناء طلب المستخدم.

---

# Principle 37

Stable Public Contracts

---

العقود العامة (Public APIs, Events, DTOs) لا تُغيّر بطريقة تكسر التوافق إلا في إصدار Major مع خطة ترحيل واضحة.

---

# Principle 38

Measure Before Optimize

---

لا يتم تحسين الأداء بناءً على التخمين.

أي تحسين يجب أن يستند إلى قياسات فعلية (Profiling / Metrics).

---

# Principle 39

Automation by Default

---

كل ما يمكن أتمتته يجب أتمتته:

- الاختبارات
- فحص جودة الكود
- النشر
- فحص الثغرات
- بناء الوثائق

---

# Principle 40

Architecture Is a Product

---

المعمارية ليست وثيقة تُكتب مرة واحدة.

بل منتج حي يتم تطويره مع المشروع.

أي تغيير كبير يجب أن ينعكس في:

- Architecture.md
- ADR
- Database Design
- Domain Model
- API Specification

---

# Non-Negotiable Rules

هذه القواعد لا يسمح بمخالفتها إلا بوجود ADR معتمد:

✓ لا Business Logic خارج Services.

✓ لا Posting خارج Posting Engine.

✓ لا تعديل مباشر للمخزون خارج Inventory Engine.

✓ لا حذف فعلي للبيانات المالية.

✓ لا كتابة SQL داخل Views.

✓ لا تخزين Secrets داخل Repository.

✓ لا Commit بدون Tests.

✓ لا Merge بدون Code Review.

✓ لا Feature بدون Documentation.

✓ لا تغيير معماري بدون ADR.

---

# Governance

جميع Pull Requests تخضع لمراجعة معمارية.

أي مخالفة لهذه الوثيقة تمنع دمج التغييرات حتى يتم تصحيحها أو اعتماد ADR رسمي يبرر الاستثناء.

---

# Document Status

Status: Official

Owner: Chief Software Architect

Review Frequency: Every Major Release

Effective From: Version 1.0

Supersedes: None