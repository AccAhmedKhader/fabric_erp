# docs/specifications/WORKFLOW_ENGINE_SPEC.md

# FabricERP Enterprise

# Workflow Engine Specification

Version: 1.0.0

Status: Official Specification

Module: Workflow Engine

Owner: Chief Software Architect

Last Updated: 2026

---

# Table of Contents

1. Purpose
2. Objectives
3. Scope
4. Architecture
5. Core Concepts
6. Workflow Components
7. Workflow States
8. State Transitions
9. Workflow Lifecycle
10. Approval Engine
11. Approval Matrix
12. Role Resolution
13. Delegation
14. Escalation
15. Timeout Policies
16. Parallel Approval
17. Sequential Approval
18. Conditional Approval
19. Workflow Versioning
20. Workflow Events
21. Notifications
22. Security
23. Audit Trail
24. API Specification
25. Database Design
26. Performance
27. Testing
28. Future Enhancements

---

# 1. Purpose

Workflow Engine هو المحرك المسؤول عن إدارة دورة حياة جميع المستندات داخل FabricERP.

أي مستند يمكن أن يمر بعدة حالات (States) ويحتاج إلى موافقات (Approvals) يجب أن يستخدم هذا المحرك.

---

# 2. Objectives

يهدف المحرك إلى:

- توحيد دورة حياة المستندات.
- فصل منطق الموافقات عن الوحدات التجارية.
- دعم سياسات الموافقات متعددة المستويات.
- دعم العمل متعدد الشركات والفروع.
- ضمان إمكانية تتبع جميع التغييرات.
- منع تجاوز الصلاحيات.

---

# 3. Supported Modules

- Sales
- Purchasing
- Inventory
- Treasury
- Accounting
- HR
- Assets
- Manufacturing
- CRM

---

# 4. Architecture

```text
Business Document
        │
        ▼
Workflow Service
        │
        ▼
State Machine
        │
        ▼
Approval Engine
        │
        ▼
Notification Service
        │
        ▼
Audit Trail
```

---

# 5. Core Concepts

## Workflow Definition

تعريف لمسار المستند.

---

## Workflow Instance

نسخة فعلية مرتبطة بمستند معين.

---

## State

الحالة الحالية.

---

## Transition

الانتقال بين حالتين.

---

## Action

الإجراء المطلوب.

---

## Approval

الموافقة.

---

## Rejection

الرفض.

---

## Cancellation

الإلغاء.

---

# 6. Default States

Draft

↓

Pending Approval

↓

Approved

↓

Posted

↓

Closed

كما يدعم:

Rejected

Cancelled

Returned

Archived

---

# 7. State Rules

Draft

يمكن التعديل.

---

Pending Approval

لا يسمح بالتعديل إلا للمصرح لهم.

---

Approved

جاهز للترحيل.

---

Posted

لا يسمح بالتعديل.

---

Closed

منتهي.

---

Cancelled

لا يمكن استخدامه.

---

Returned

يعود للمرسل مع الملاحظات.

---

Archived

للقراءة فقط.

---

# 8. State Transition Matrix

| From | To |
|------|-----|
| Draft | Pending Approval |
| Pending Approval | Approved |
| Pending Approval | Rejected |
| Approved | Posted |
| Posted | Closed |
| Draft | Cancelled |
| Rejected | Draft |
| Returned | Draft |

أي Transition غير معرف يعتبر مرفوضاً.

---

# 9. Workflow Lifecycle

Create

↓

Draft

↓

Submit

↓

Approval

↓

Approved

↓

Posting

↓

Completed

---

# 10. Approval Levels

يدعم النظام:

Single Level

Two Levels

Three Levels

Unlimited Levels

---

مثال

Employee

↓

Supervisor

↓

Department Manager

↓

Finance Manager

↓

General Manager

---

# 11. Approval Policies

حسب:

المبلغ

القسم

الفرع

الشركة

نوع المستند

المورد

العميل

مركز التكلفة

المشروع

---

# 12. Role Resolution

الموافقة تعتمد على:

Role

وليس User.

مثال

Finance Manager

بدلاً من

Ahmed

---

# 13. Delegation

يمكن للمستخدم تفويض صلاحياته مؤقتاً.

يتم تسجيل:

المفوض

المفوض إليه

الفترة

السبب

---

# 14. Escalation

إذا انتهت مدة الموافقة:

يتم إرسال إشعار.

ثم تصعيد للمستوى الأعلى.

---

# 15. Timeout

كل خطوة يمكن أن تمتلك:

SLA

مثال

48 ساعة.

---

بعدها:

Reminder

↓

Escalation

↓

Automatic Action (اختياري)

---

# 16. Parallel Approval

يدعم النظام:

موافقة أكثر من شخص فى نفس الوقت.

ويحدد:

All Required

أو

Any One

---

# 17. Sequential Approval

المستوى الثانى

لا يبدأ

إلا بعد انتهاء الأول.

---

# 18. Conditional Workflow

مثال

إذا كانت الفاتورة أقل من

5000

↓

مدير القسم فقط.

أما إذا زادت

↓

مدير القسم

↓

المدير المالي

↓

المدير العام.

---

# 19. Workflow Versioning

كل Workflow له:

Version

ولا يؤثر تعديل Workflow جديد على المستندات القديمة.

---

# 20. Workflow Events

WorkflowStarted

WorkflowSubmitted

ApprovalRequested

Approved

Rejected

Returned

Cancelled

Posted

Closed

---

# 21. Notifications

يدعم:

Email

In-App

Push Notification

SMS (Future)

---

الإشعارات تشمل:

طلب موافقة

تذكير

تصعيد

رفض

اعتماد

إلغاء

---

# 22. Security

كل انتقال بين الحالات يتطلب:

Authentication

Authorization

Permission Check

Company Isolation

Branch Isolation

Workflow Validation

---

# 23. Audit Trail

يسجل:

Document

Workflow

Old State

New State

User

Date

IP

Reason

Comment

Execution Time

---

# 24. API

## Submit

POST

/api/v1/workflow/submit

---

## Approve

POST

/api/v1/workflow/approve

---

## Reject

POST

/api/v1/workflow/reject

---

## Return

POST

/api/v1/workflow/return

---

## Cancel

POST

/api/v1/workflow/cancel

---

## History

GET

/api/v1/workflow/history/{document}

---

# 25. Database Design

workflow_definitions

workflow_versions

workflow_states

workflow_transitions

workflow_instances

workflow_tasks

workflow_approvals

workflow_delegations

workflow_escalations

workflow_history

workflow_comments

workflow_notifications

---

# 26. Performance

هدف الأداء:

إنشاء Workflow

< 30 ms

---

اعتماد مستند

< 50 ms

---

قراءة Workflow

< 20 ms

---

يدعم

10000

Workflow نشطة.

---

# 27. Error Codes

WF001

Workflow Not Found

WF002

Invalid Transition

WF003

Permission Denied

WF004

Already Approved

WF005

Already Posted

WF006

Workflow Locked

WF007

Approval Timeout

WF008

Duplicate Approval

WF009

Invalid State

WF010

Company Mismatch

---

# 28. Testing Strategy

Unit Tests

State Transition Tests

Approval Tests

Permission Tests

Delegation Tests

Escalation Tests

Timeout Tests

Concurrency Tests

API Tests

Performance Tests

Security Tests

---

# 29. Integration Points

يتكامل مع:

Authentication Engine

↓

RBAC

↓

Posting Engine

↓

Notification Engine

↓

Audit Trail

↓

Numbering Engine

↓

Reporting Engine

---

# 30. Non-Negotiable Rules

✓ لا يمكن تجاوز Workflow.

✓ لا يمكن Posting قبل Approval.

✓ جميع الانتقالات مسجلة.

✓ جميع الموافقات Audited.

✓ لا يمكن اعتماد مستند مرتين.

✓ كل Workflow Versioned.

✓ جميع الأحداث تصدر Domain Events.

✓ جميع العمليات داخل Transaction.

✓ جميع الصلاحيات تعتمد على Roles.

✓ جميع العمليات قابلة للتتبع.

---

# 31. Future Roadmap

- BPMN 2.0 Import/Export
- Graphical Workflow Designer
- Dynamic Approval Matrix
- AI-based Approval Suggestions
- SLA Dashboard
- Process Analytics
- Workflow Templates Marketplace
- Cross-Company Workflows
- Integration with External BPM Systems

---

# Appendix A - Default Workflow for Financial Documents

```text
Draft
   │
   ▼
Pending Approval
   │
   ▼
Approved
   │
   ▼
Posted
   │
   ▼
Closed
```

---

# Appendix B - Default Workflow for Purchase Orders

```text
Draft
   │
   ▼
Department Approval
   │
   ▼
Finance Approval
   │
   ▼
General Manager Approval
   │
   ▼
Approved
   │
   ▼
Issued
```

---

# End of Document