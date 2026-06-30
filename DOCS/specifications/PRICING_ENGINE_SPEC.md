# FabricERP Enterprise

# Pricing Engine Specification

Version: 1.0.0

Status: Official

---

# Purpose

توفير محرك مركزي لتحديد الأسعار في جميع وحدات النظام.

---

# Supported Price Sources

Standard Price

Customer Price

Contract Price

Price List

Promotional Price

Campaign Price

Volume Price

Manual Override

---

# Pricing Priority

Manual

↓

Contract

↓

Promotion

↓

Customer

↓

Price List

↓

Default

---

# Price Factors

Customer

Supplier

Item

Variant

Warehouse

Currency

Date

Quantity

Unit Of Measure

Branch

Company

---

# Features

Multiple Price Lists

Effective Dates

Currency Conversion

Minimum Price

Maximum Discount

Approval Rules

Margin Validation

---

# APIs

POST /pricing/calculate

GET /pricing/lists

---

# Performance

Calculation <10 ms

---

# Events

PriceCalculated

PriceChanged

PriceExpired

---

# Database

price_lists

price_rules

price_items

customer_prices

supplier_prices

---

# Non-Negotiable Rules

✓ جميع الأسعار تمر عبر Pricing Engine.

✓ لا يسمح بحساب السعر داخل الوحدات التجارية.

End Of Document