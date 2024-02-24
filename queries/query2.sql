WITH DepartmentSales AS (
    SELECT
        d.DepartmentID,
        d.Name AS DepartmentName,
        SUM(s.Amount) AS TotalDepartmentSales,
        COUNT(DISTINCT e.EmployeeID) AS NumberOfEmployees
    FROM
        `project.dataset.sales` s
    JOIN
        `project.dataset.employees` e ON s.EmployeeID = e.EmployeeID
    JOIN
        `project.dataset.departments` d ON e.DepartmentID = d.DepartmentID
    GROUP BY
        d.DepartmentID
),
EmployeePerformance AS (
    SELECT
        e.EmployeeID,
        CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
        e.DepartmentID,
        SUM(s.Amount) AS TotalSales,
        RANK() OVER(PARTITION BY e.DepartmentID ORDER BY SUM(s.Amount) DESC) AS PerformanceRank
    FROM
        `project.dataset.sales` s
    JOIN
        `project.dataset.employees` e ON s.EmployeeID = e.EmployeeID
    GROUP BY
        e.EmployeeID
)
SELECT
    ds.DepartmentName,
    ds.TotalDepartmentSales,
    ds.NumberOfEmployees,
    ep.EmployeeName,
    ep.TotalSales,
    ep.PerformanceRank
FROM
    DepartmentSales ds
JOIN
    EmployeePerformance ep ON ds.DepartmentID = ep.DepartmentID
ORDER BY
    ds.TotalDepartmentSales DESC, ep.PerformanceRank
LIMIT
    20;
