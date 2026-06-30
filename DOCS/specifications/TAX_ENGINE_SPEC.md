# FabricERP Enterprise

# Tax Engine Specification

Version: 1.0.0

Status: Official Specification

Module: Tax Engine

Owner: Finance Architecture Team

Classification: Core Financial Engine

---

# 1. Purpose

Tax Engine هو المحرك المركزي المسؤول عن احتساب الضرائب والتحقق منها وتسجيلها وربطها بالقيود المحاسبية.

لا يجوز لأي وحدة (Sales, Purchasing, Treasury...) حساب الضرائب مباشرة.

---

# 2. Objectives

- Centralized Tax Calculation
- Multi-Country Support
- Configurable Tax Rules
- Real-Time Validation
- Full Auditability
- Compliance Ready

---

# 3. Supported Tax Types

VAT

GST

Sales Tax

Withholding Tax

Service Tax

Excise Tax

Custom Duties

Municipality Tax

Environmental Tax

Future Custom Taxes

---

# 4. Tax Rule Components

Tax Code

Tax Group

Tax Type

Rate

Effective Date

Expiry Date

Jurisdiction

Priority

Calculation Method

Recoverable Flag

Posting Accounts

---

# 5. Calculation Methods

Percentage

Fixed Amount

Progressive

Compound Tax

Tax Included

Tax Excluded

Threshold Based

---

# 6. Tax Scope

Company

↓

Country

↓

State

↓

City

↓

Customer

↓

Supplier

↓

Item

↓

Item Category

↓

Document Type

---

# 7. Tax Determination Priority

1. Document Override

2. Customer/Supplier Tax Profile

3. Item Tax Group

4. Company Default

---

# 8. Posting Integration

Tax Engine لا ينشئ قيودًا محاسبية.

بعد احتساب الضريبة يرسل Tax Lines إلى Posting Engine.

---

# 9. Validation Rules

- Tax Code Active
- Effective Date Valid
- Company Match
- Currency Match
- Rate Exists

---

# 10. Events

TaxCalculated

TaxValidated

TaxAdjusted

TaxReversed

TaxRuleUpdated

---

# 11. APIs

POST /api/v1/tax/calculate

POST /api/v1/tax/validate

GET /api/v1/tax/rates

---

# 12. Database

tax_codes

tax_rates

tax_groups

tax_rules

tax_jurisdictions

tax_transactions

tax_adjustments

---

# 13. Performance

Calculation < 15 ms

Supports Bulk Calculation

---

# 14. Security

RBAC Protected

Audit Required

---

# 15. Testing

VAT Tests

Compound Tax Tests

Reverse Tax Tests

Bulk Tests

Performance Tests

---

# Non-Negotiable Rules

✓ جميع الضرائب تمر عبر Tax Engine.

✓ لا توجد نسب ضرائب Hardcoded.

✓ جميع العمليات Audited.

End Of Document