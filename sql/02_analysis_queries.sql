-- Q4. Monthly order trend
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::TIMESTAMP)::DATE AS order_month,
    COUNT(*) AS total_orders
FROM olist_orders
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY 1
ORDER BY 1;


-- Q5. Top 10 product categories by item sales
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'Unknown'
    ) AS category,
    ROUND(SUM(oi.price::NUMERIC), 2) AS item_sales,
    COUNT(*) AS items_sold
FROM olist_order_items oi
JOIN olist_products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY 1
ORDER BY item_sales DESC
LIMIT 10;


-- Q6. Top 10 customer states
SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM olist_customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;


-- Q7. Order status distribution
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM olist_orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- Q8. Payment method analysis
SELECT
    payment_type,
    COUNT(*) AS payment_records,
    ROUND(SUM(payment_value::NUMERIC), 2) AS total_payment_value,
    ROUND(AVG(payment_value::NUMERIC), 2) AS average_payment_value
FROM olist_order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- Q9. Review score analysis
SELECT
    review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM olist_order_reviews
GROUP BY review_score
ORDER BY review_score DESC;


-- Q10. Average delivery time in days
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date::TIMESTAMP -
                    order_purchase_timestamp::TIMESTAMP
                )
            ) / 86400
        )::NUMERIC,
        2
    ) AS avg_delivery_days
FROM olist_orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_purchase_timestamp IS NOT NULL
  AND order_delivered_customer_date::TIMESTAMP
      >= order_purchase_timestamp::TIMESTAMP;