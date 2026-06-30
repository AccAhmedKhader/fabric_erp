# docs/ARCHITECTURE.md

# FabricERP Enterprise Architecture

**Version:** 1.0.0

**Status:** Draft

**Architecture Style:** Clean Architecture + Domain-Driven Design (DDD) + Modular Monolith

---

# Table of Contents

1. Introduction
2. Architecture Goals
3. Guiding Principles
4. High-Level Architecture
5. Architecture Layers
6. Module Architecture
7. Folder Structure
8. Dependency Rules
9. Request Lifecycle
10. Domain Model
11. Service Layer
12. Repository Layer
13. Event-Driven Architecture
14. Posting Engine
15. Numbering Engine
16. Workflow Engine
17. Security Architecture
18. Multi-Tenant Strategy
19. Performance Strategy
20. Caching Strategy
21. Background Processing
22. Reporting Architecture
23. Integration Architecture
24. Logging & Monitoring
25. Future Architecture

---

# 1. Introduction

FabricERP هو نظام ERP Enterprise يعتمد على تصميم Modular Monolith مع إمكانية التحول مستقبلاً إلى Microservices دون إعادة كتابة منطق الأعمال.

الهدف هو فصل منطق الأعمال عن Django Framework بحيث يبقى النظام قابلاً للاختبار والتوسع.

---

# 2. Architecture Goals

- High Cohesion
- Low Coupling
- Scalability
- Maintainability
- Testability
- Extensibility
- Security
- Performance

---

# 3. Guiding Principles

- SOLID
- DRY
- KISS
- YAGNI
- Separation of Concerns
- Single Responsibility
- Explicit Business Rules
- Immutable Accounting Records

---

# 4. High-Level Architecture

```text
                 +----------------------+
                 |      Web / API       |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Presentation Layer   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Application Layer    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Domain Layer         |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Infrastructure Layer |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | PostgreSQL / Redis   |
                 +----------------------+
```

---

# 5. Architecture Layers

## Presentation Layer

Responsibilities:

- Django Views
- DRF ViewSets
- HTML Templates
- REST Endpoints
- Authentication

Must NOT:

- contain business logic
- write SQL
- create accounting entries

---

## Application Layer

Responsibilities:

- Use Cases
- Services
- Transactions
- Validation
- Authorization

Examples

SalesOrderService

InvoiceService

PostingService

InventoryService

---

## Domain Layer

Contains:

Entities

Value Objects

Business Rules

Specifications

Domain Events

Policies

Factories

This layer NEVER imports Django Views.

---

## Infrastructure Layer

Contains

ORM

Repositories

Email

Redis

Celery

Storage

External APIs

---

# 6. Module Architecture

```text
apps/

authentication/

core/

accounting/

gl/

inventory/

sales/

purchases/

treasury/

banking/

crm/

assets/

hr/

reports/

dashboard/

workflow/

notification/

audit/

settings/

api/
```

Each module owns:

Models

Services

Repositories

Validators

Permissions

Signals

Tests

Serializers

URLs

Views

Templates

---

# 7. Folder Structure

Example

```text
sales/

models/

services/

repositories/

validators/

permissions/

api/

tests/

signals/

selectors/

templates/

management/

migrations/
```

---

# 8. Dependency Rules

Allowed

View

↓

Service

↓

Repository

↓

Model

Forbidden

View → Repository

View → Database

Serializer → Business Logic

Model → External API

---

# 9. Request Lifecycle

```text
HTTP Request

↓

View

↓

Serializer

↓

Service

↓

Repository

↓

Database

↓

Service

↓

Domain Events

↓

Response
```

---

# 10. Domain Model

Main Domains

Accounting

Inventory

Sales

Purchasing

Treasury

CRM

Assets

HR

Reporting

Workflow

Each domain is isolated.

---

# 11. Service Layer

Example

SalesOrderService

Responsibilities

Validate

Calculate totals

Reserve stock

Generate journal

Publish events

Commit transaction

Services contain business logic.

Views never contain business logic.

---

# 12. Repository Layer

Repositories isolate ORM access.

Example

CustomerRepository

InvoiceRepository

JournalRepository

InventoryRepository

Benefits

Easy Testing

Loose Coupling

Future Database Migration

---

# 13. Event-Driven Architecture

Every important action emits an event.

Example

InvoicePosted

↓

JournalGenerated

↓

InventoryUpdated

↓

CustomerBalanceUpdated

↓

NotificationSent

↓

AuditLogged

Events must be idempotent.

---

# 14. Posting Engine

Single engine responsible for accounting entries.

Rules

Double-entry only

Balanced journals

Atomic transaction

No direct posting from Views

Every module uses PostingService

---

# 15. Numbering Engine

Responsibilities

Invoice Numbers

Voucher Numbers

Journal Numbers

Purchase Numbers

Sales Numbers

Features

Per Company

Per Branch

Per Fiscal Year

Thread Safe

Gap Policy Configurable

---

# 16. Workflow Engine

States

Draft

Pending Approval

Approved

Posted

Closed

Cancelled

Transitions controlled by policies.

---

# 17. Security Architecture

Authentication

Django Authentication

Authorization

RBAC

Object Permissions

Future

MFA

OAuth2

SSO

Audit

Mandatory

---

# 18. Multi-Tenant Strategy

Isolation

Company

↓

Branch

↓

Warehouse

↓

User

Every business record belongs to one company.

---

# 19. Performance Strategy

Indexes

Bulk Operations

Query Optimization

Pagination

Caching

Async Tasks

Connection Pooling

---

# 20. Caching Strategy

Redis

Cache

Reference Data

Settings

Dashboard

Reports

Never Cache

Journal Posting

Inventory Transactions

Financial Balances

---

# 21. Background Processing

Celery Tasks

Email

PDF

Excel Export

Notifications

Large Reports

Rebuild Search

---

# 22. Reporting Architecture

Reports never contain business logic.

Reports consume Services.

Output

PDF

Excel

CSV

REST

Dashboard

---

# 23. Integration Architecture

REST API

Webhooks

Import Engine

Export Engine

Future

GraphQL

EDI

Message Queue

---

# 24. Logging & Monitoring

Application Logs

Audit Logs

Security Logs

Performance Logs

Error Logs

Monitoring

Health Check

Metrics

Tracing

Future

Prometheus

Grafana

OpenTelemetry

---

# 25. Future Architecture

Planned evolution

Modular Monolith

↓

Hybrid Modules

↓

Independent Services

↓

Cloud Native ERP

---

# Architecture Rules

✓ Business logic only in Services

✓ Accounting only through Posting Engine

✓ No SQL in Views

✓ No business rules in Templates

✓ Repository is the only data access layer

✓ Domain Events for cross-module communication

✓ Every operation must be auditable

✓ Every module must be independently testable

✓ Every API documented

✓ Every feature covered by automated tests

---

# Document Approval

Owner

Architecture Team

Status

Draft

Review

Every Major Release