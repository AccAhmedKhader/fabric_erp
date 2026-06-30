# FabricERP Enterprise

# Financial Dimensions Specification

Version: 1.0

Status: Official

---

# Purpose

توفير نظام موحد للأبعاد المحاسبية المستخدمة فى جميع القيود والتقارير.

---

# Supported Dimensions

Company

Branch

Cost Center

Department

Project

Business Unit

Region

Salesperson

Profit Center

Customer Group

Supplier Group

Item Category

Warehouse

Channel

Campaign

Future Custom Dimensions

---

# Rules

كل Dimension يمكن أن يكون:

Mandatory

Optional

Disabled

حسب نوع الحساب.

---

# Cost Centers

Tree Structure

Budget Support

Closing Rules

Allocation Rules

---

# Projects

Budget

Revenue

Expense

WIP

Completion Percentage

---

# Profit Centers

Revenue Analysis

Expense Analysis

Profitability Reports

---

# Allocation Rules

Fixed %

Dynamic %

Equal Distribution

Formula Based

Driver Based

---

# Validation

Dimensions must belong to Company.

Dimensions must be Active.

Dimensions must match Fiscal Year.

---

# APIs

GET /dimensions

POST /dimensions

POST /validate-dimensions

---

# Database

dimensions

dimension_values

dimension_sets

dimension_rules

dimension_allocations

---

# Testing

Validation Tests

Posting Tests

Reporting Tests

Budget Tests

Allocation Tests

---

# Non-Negotiable Rules

✓ جميع القيود تستخدم Dimension Sets.

✓ لا يسمح باستخدام Dimension غير نشط.

✓ جميع التعديلات Audited.

End Of Document