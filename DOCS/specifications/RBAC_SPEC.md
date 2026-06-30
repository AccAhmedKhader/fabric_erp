# docs/specifications/RBAC_SPEC.md

# FabricERP Enterprise

# Role Based Access Control Specification

Version: 1.0.0

Status: Official

Owner: Security Architecture Team

Classification: Security Core

---

# Table of Contents

1. Purpose
2. Objectives
3. RBAC Model
4. Security Layers
5. Users
6. Roles
7. Permissions
8. Scopes
9. Company Isolation
10. Branch Isolation
11. Warehouse Isolation
12. Data Ownership
13. Permission Resolution
14. Object Permissions
15. Dynamic Permissions
16. Approval Permissions
17. Financial Permissions
18. API Security
19. Audit Integration
20. Database
21. APIs
22. Testing

---

# 1. Purpose

توفير نظام صلاحيات مركزى لجميع وحدات FabricERP.

---

# 2. Objectives

Least Privilege

Role Based

Scalable

Auditable

Multi Company

Multi Branch

---

# 3. RBAC Model

User

↓

Role

↓

Permission

↓

Resource

↓

Action

---

# 4. Security Layers

Authentication

↓

Authorization

↓

Object Permission

↓

Business Rule

↓

Workflow Permission

---

# 5. Users

كل مستخدم يمكن أن يمتلك:

عدة Roles

عدة Companies

عدة Branches

عدة Warehouses

---

# 6. Roles

Examples

Administrator

Finance Manager

Accountant

Sales Manager

Sales User

Warehouse Manager

Cashier

HR Manager

Auditor

---

# 7. Permissions

Create

Read

Update

Delete

Approve

Reject

Post

Reverse

Export

Import

Print

Configure

Audit

---

# 8. Resource Types

Sales Invoice

Purchase Invoice

Journal

Customer

Supplier

Item

Warehouse

Bank

Cash

Asset

Employee

Payroll

Workflow

---

# 9. Company Scope

المستخدم يرى فقط شركاته.

---

# 10. Branch Scope

المستخدم يرى فقط فروعه.

---

# 11. Warehouse Scope

اختيارى.

حسب إعدادات الشركة.

---

# 12. Data Ownership

يمكن قصر الوصول إلى:

Own Records

Department

Branch

Company

Global

---

# 13. Permission Resolution

Explicit Deny

↓

Explicit Allow

↓

Inherited Allow

↓

Default Deny

---

# 14. Object Permissions

يمكن التحكم فى:

Invoice رقم 100

وليس كل الفواتير.

---

# 15. Dynamic Rules

مثال

يسمح بالموافقة إذا:

Amount < 10000

ويمنع إذا تجاوز.

---

# 16. Approval Permissions

Approve

Reject

Return

Cancel

Delegate

Escalate

---

# 17. Financial Permissions

Post Journal

Reverse Journal

Close Fiscal Year

Open Fiscal Year

Exchange Rates

Cost Centers

---

# 18. API Security

JWT

Refresh Token

Permission Middleware

Rate Limiting

Scopes

---

# 19. Audit Integration

كل قرار صلاحية يسجل فى Audit.

---

# 20. Database

users

roles

permissions

user_roles

role_permissions

permission_scopes

object_permissions

company_permissions

branch_permissions

warehouse_permissions

---

# 21. APIs

GET /roles

GET /permissions

POST /roles

POST /assign-role

POST /check-permission

---

# 22. Testing

Permission Tests

Role Tests

Isolation Tests

Escalation Tests

Workflow Tests

Performance Tests

Security Tests

---

# Standard Roles

System Administrator

Company Administrator

Finance Manager

Chief Accountant

Accountant

Treasury Manager

Cashier

Sales Manager

Sales Representative

Purchase Manager

Buyer

Warehouse Manager

Storekeeper

Inventory Auditor

HR Manager

Payroll Officer

Internal Auditor

External Auditor

Read Only

---

# Non-Negotiable Rules

✓ Default Deny.

✓ Least Privilege.

✓ Company Isolation.

✓ Branch Isolation.

✓ جميع الصلاحيات Audited.

✓ لا يوجد Super User داخل Business Logic.

✓ جميع عمليات Approval تعتمد على RBAC.

✓ لا يسمح بتجاوز Workflow بواسطة الصلاحيات.

---

End Of Document