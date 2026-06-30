# FabricERP Enterprise

# Numbering Engine Specification

Version: 1.0.0

Status: Official

Owner: Architecture Team

Module: Core Services

---

# Table of Contents

1. Introduction
2. Objectives
3. Scope
4. Design Principles
5. Architecture
6. Number Formats
7. Number Policies
8. Sequence Generation
9. Concurrency
10. Reservation
11. Rollback
12. Fiscal Years
13. Multi Company
14. Multi Branch
15. Performance
16. Security
17. Audit
18. API
19. Database
20. Testing

---

# 1. Introduction

Numbering Engine هو المسئول الوحيد عن إصدار جميع أرقام المستندات داخل FabricERP.

ولا يسمح لأي Module بإنشاء الأرقام بنفسه.

---

# 2. Supported Documents

Sales Invoice

Purchase Invoice

Journal Voucher

Receipt Voucher

Payment Voucher

Delivery Note

Purchase Order

Sales Order

Quotation

Transfer

Adjustment

Asset

Payroll

Production Order

أي مستند جديد يضاف مستقبلاً.

---

# 3. Design Goals

✓ Thread Safe

✓ High Performance

✓ Distributed Ready

✓ Configurable

✓ Atomic

✓ Audit Enabled

✓ Multi Company

✓ Multi Branch

✓ Fiscal Year Aware

---

# 4. Architecture

Document

↓

Number Request

↓

Validation

↓

Sequence Resolver

↓

Lock Manager

↓

Counter Update

↓

Audit

↓

Return Number

---

# 5. Number Components

يمكن أن يتكون الرقم من:

Prefix

Company Code

Branch Code

Fiscal Year

Month

Day

Sequence

Suffix

مثال

```
INV-C01-B02-2026-00001254
```

---

# 6. Number Policies

يدعم النظام:

Continuous Numbering

Gap Allowed

Gap Not Allowed

Daily Sequence

Monthly Sequence

Yearly Sequence

Manual Approval Sequence

Custom Sequence

---

# 7. Number Formats

Examples

```
INV-2026-000001

JV-2026-000045

PO-2026-000981

RCP-2026-000221
```

---

# 8. Sequence Storage

لكل Sequence يتم حفظ:

UUID

Company

Branch

Fiscal Year

Document Type

Current Value

Last Value

Status

Updated At

Version

---

# 9. Concurrency

المحرك يجب أن يدعم:

1000+

Concurrent Requests

بدون تكرار رقم واحد.

---

يعتمد على:

Database Lock

Optimistic Lock

أو

Redis Lock

حسب البيئة.

---

# 10. Reservation

يمكن حجز رقم

قبل إنشاء المستند.

الحالة

Reserved

↓

Used

أو

Released

---

# 11. Rollback

إذا فشلت العملية

يحدد النظام حسب السياسة:

Gap Allowed

يترك الرقم.

Gap Not Allowed

يعاد استخدام الرقم.

---

# 12. Fiscal Year Rules

كل سنة مالية

تمتلك Sequence مستقلة.

مثال

2026

↓

000001

---

2027

↓

000001

---

# 13. Company Isolation

كل شركة

تمتلك Sequences مستقلة.

---

# 14. Branch Isolation

اختياري

حسب إعدادات الشركة.

---

# 15. Validation

قبل إصدار الرقم

يتحقق من:

Company

Branch

Fiscal Year

Permission

Sequence Status

---

# 16. API

POST

/api/v1/core/numbering/next

Request

Document Type

Company

Branch

Fiscal Year

Response

Generated Number

Sequence Id

Timestamp

---

# 17. Security

الصلاحيات:

NUMBER_GENERATE

NUMBER_ADMIN

---

# 18. Audit

يسجل:

Generated Number

User

Company

Branch

Date

IP

Execution Time

---

# 19. Performance

Response Time

<20 ms

---

Concurrent Requests

1000+

---

# 20. Database Tables

document_sequences

sequence_history

sequence_reservations

sequence_locks

---

# 21. Error Codes

NUM001

Sequence Not Found

NUM002

Fiscal Closed

NUM003

Company Missing

NUM004

Lock Timeout

NUM005

Permission Denied

NUM006

Sequence Overflow

---

# 22. Testing

Unit Tests

Concurrency Tests

Stress Tests

Rollback Tests

Performance Tests

Recovery Tests

---

# Non-Negotiable Rules

✓ لا يوجد توليد أرقام خارج Numbering Engine.

✓ جميع الأرقام Unique.

✓ جميع العمليات Thread Safe.

✓ جميع العمليات Audited.

✓ جميع العمليات Atomic.

---

End Of Document