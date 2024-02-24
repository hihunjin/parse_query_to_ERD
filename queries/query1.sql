WITH ProductSales AS (
    SELECT
        p.ProductID,
        p.Name AS ProductName,
        SUM(s.Quantity) AS TotalUnitsSold,
        AVG(s.Amount) AS AverageSaleAmount,
        ARRAY_AGG(DISTINCT c.Category) AS ProductCategories
    FROM
        `project.dataset.sales` s
    JOIN
        `project.dataset.products` p ON s.ProductID = p.ProductID
    LEFT JOIN
        `project.dataset.categories` c ON p.CategoryID = c.CategoryID
    GROUP BY
        p.ProductID
),
CustomerSpending AS (
    SELECT
        s.CustomerID,
        c.Name AS CustomerName,
        SUM(s.Amount) AS TotalSpent,
        CASE
            WHEN SUM(s.Amount) > 10000 THEN 'Premium'
            WHEN SUM(s.Amount) > 5000 THEN 'Gold'
            ELSE 'Regular'
        END AS CustomerCategory
    FROM
        `project.dataset.sales` s
    JOIN
        `project.dataset.customers` c ON s.CustomerID = c.CustomerID
    GROUP BY
        s.CustomerID
)
SELECT
    ps.ProductName,
    ps.TotalUnitsSold,
    ps.AverageSaleAmount,
    ps.ProductCategories,
    cs.CustomerName,
    cs.TotalSpent,
    cs.CustomerCategory
FROM
    ProductSales ps
JOIN
    CustomerSpending cs ON ps.ProductID = cs.CustomerID
ORDER BY
    ps.TotalUnitsSold DESC, cs.TotalSpent DESC
LIMIT
    10;
