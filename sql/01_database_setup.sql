-- Run this in pgAdmin's Query Tool after connecting to your PostgreSQL server.
-- Create the database separately if needed:
-- CREATE DATABASE retailpulse;
--
-- Connect to the retailpulse database before running project schema scripts.
-- Table definitions and imports will be added after we inspect the CSV columns.

-- RetailPulse: verify raw table structure before transformations
-- Raw imports remain unchanged; create typed analytics views.

CREATE OR REPLACE VIEW vw_order_payments AS
SELECT
    order_id,
    payment_sequential::INTEGER AS payment_sequential,
    payment_type,
    payment_installments::INTEGER AS payment_installments,
    payment_value::NUMERIC(12,2) AS payment_value
FROM olist_order_payments;

CREATE OR REPLACE VIEW vw_orders AS
SELECT
    order_id,
    customer_id,
    order_status,
    NULLIF(order_purchase_timestamp, '')::TIMESTAMP
        AS order_purchase_timestamp,
    NULLIF(order_approved_at, '')::TIMESTAMP
        AS order_approved_at,
    NULLIF(order_delivered_customer_date, '')::TIMESTAMP
        AS order_delivered_customer_date,
    NULLIF(order_estimated_delivery_date, '')::TIMESTAMP
        AS order_estimated_delivery_date
FROM olist_orders;

CREATE OR REPLACE VIEW vw_order_items AS
SELECT
    order_id,
    order_item_id::INTEGER AS order_item_id,
    product_id,
    seller_id,
    shipping_limit_date::TIMESTAMP AS shipping_limit_date,
    price::NUMERIC(12,2) AS price,
    freight_value::NUMERIC(12,2) AS freight_value
FROM olist_order_items;
