-- ====================================================================
-- RETAIL DATA WAREHOUSE - BUSINESS ANALYTICAL QUERIES (SQL)
-- Target Schema: retail_dw (Star Schema)
-- Designed for business analysis and Power BI dashboard metric validation.
-- ====================================================================

-- 1. STORE PERFORMANCE ANALYSIS
-- Question: Which store types (A, B, C) generate the highest total revenue and average weekly sales?
SELECT 
    s.type AS store_type,
    COUNT(DISTINCT s.store) AS total_stores,
    ROUND(SUM(f.weekly_sales)::numeric, 2) AS total_revenue,
    ROUND(AVG(f.weekly_sales)::numeric, 2) AS avg_weekly_sales
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_store s ON f.store = s.store
GROUP BY s.type
ORDER BY total_revenue DESC;


-- 2. HOLIDAY LIFT / IMPACT ON SALES
-- Question: How do holiday weeks compare to regular weeks in average weekly sales?
SELECT 
    f.isholiday,
    COUNT(*) AS total_records,
    ROUND(AVG(f.weekly_sales)::numeric, 2) AS avg_weekly_sales,
    ROUND(SUM(f.weekly_sales)::numeric, 2) AS total_sales
FROM retail_dw.fact_sales f
GROUP BY f.isholiday;


-- 3. TOP 10 DEPARTMENTS BY REVENUE
-- Question: Which product departments contribute the most to company revenue?
SELECT 
    f.dept,
    ROUND(SUM(f.weekly_sales)::numeric, 2) AS total_dept_sales,
    ROUND(AVG(f.weekly_sales)::numeric, 2) AS avg_weekly_sales
FROM retail_dw.fact_sales f
GROUP BY f.dept
ORDER BY total_dept_sales DESC
LIMIT 10;


-- 4. MONTHLY SALES SEASONALITY
-- Question: What are the monthly sales trends across the year to identify peak seasons?
SELECT 
    d.month,
    ROUND(SUM(f.weekly_sales)::numeric, 2) AS total_monthly_sales,
    ROUND(AVG(f.weekly_sales)::numeric, 2) AS avg_weekly_sales
FROM retail_dw.fact_sales f
JOIN retail_dw.dim_date d ON f.date = d.date
GROUP BY d.month
ORDER BY d.month;


-- 5. PROMOTIONAL MARKDOWNS VS WEEKLY SALES
-- Question: During holiday weeks, what was the average sales volume when promotional markdowns were active?
SELECT 
    f.isholiday,
    CASE 
        WHEN (f.markdown1 IS NOT NULL OR f.markdown2 IS NOT NULL OR f.markdown3 IS NOT NULL) THEN 'Promotions Active'
        ELSE 'No Promotions'
    END AS promo_status,
    ROUND(AVG(f.weekly_sales)::numeric, 2) AS avg_weekly_sales,
    ROUND(SUM(f.weekly_sales)::numeric, 2) AS total_sales
FROM retail_dw.fact_sales f
GROUP BY f.isholiday, promo_status
ORDER BY f.isholiday DESC, avg_weekly_sales DESC;
