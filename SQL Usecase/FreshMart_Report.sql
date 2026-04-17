CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(150) NOT NULL,
    CategoryID INT,
    StockCount INT DEFAULT 0,
    ExpiryDate DATE,
    CostPrice DECIMAL(10,2),
    SellingPrice DECIMAL(10,2),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE SalesTransactions (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    QuantitySold INT,
    SaleDate DATE,
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO Categories (CategoryName) VALUES
('Dairy'),
('Bakery'),
('Beverages'),
('Snacks'),
('Frozen Foods');

INSERT INTO Products (ProductName, CategoryID, StockCount, ExpiryDate, CostPrice, SellingPrice) VALUES
('Whole Milk 1L',        1, 120, CURDATE() + INTERVAL 3 DAY,  40.00,  55.00),
('Cheddar Cheese 200g',  1,  80, CURDATE() + INTERVAL 5 DAY,  90.00, 120.00),
('White Bread',          2,  60, CURDATE() + INTERVAL 2 DAY,  25.00,  35.00),
('Croissant Pack',       2,  30, CURDATE() + INTERVAL 6 DAY,  50.00,  70.00),
('Orange Juice 1L',      3,  90, CURDATE() + INTERVAL 10 DAY, 55.00,  75.00),
('Green Tea Bags',       3, 200, CURDATE() + INTERVAL 90 DAY, 80.00, 110.00),
('Potato Chips 100g',    4, 150, CURDATE() + INTERVAL 60 DAY, 20.00,  35.00),
('Chocolate Biscuits',   4,  55, CURDATE() + INTERVAL 4 DAY,  45.00,  65.00),
('Frozen Pizza',         5,  40, CURDATE() + INTERVAL 30 DAY, 150.00,200.00),
('Ice Cream 500ml',      5,  70, CURDATE() + INTERVAL 20 DAY, 100.00,140.00);

INSERT INTO SalesTransactions (ProductID, QuantitySold, SaleDate, TotalAmount) VALUES
(1,  5, CURDATE() - INTERVAL 5 DAY,   275.00),
(1,  3, CURDATE() - INTERVAL 10 DAY,  165.00),
(2,  2, CURDATE() - INTERVAL 3 DAY,   240.00),
(3,  4, CURDATE() - INTERVAL 7 DAY,   140.00),
(5,  6, CURDATE() - INTERVAL 15 DAY,  450.00),
(6,  3, CURDATE() - INTERVAL 20 DAY,  330.00),
(7, 10, CURDATE() - INTERVAL 2 DAY,   350.00),
(7,  8, CURDATE() - INTERVAL 25 DAY,  280.00),
(9,  2, CURDATE() - INTERVAL 40 DAY,  400.00),
(10, 4, CURDATE() - INTERVAL 12 DAY,  560.00);


-- REPORT 1: Expiring Soon

SELECT 
    p.ProductID,
    p.ProductName,
    c.CategoryName,
    p.StockCount,
    p.ExpiryDate,
    DATEDIFF(p.ExpiryDate, CURDATE()) AS DaysUntilExpiry
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE p.ExpiryDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
  AND p.StockCount > 50;


-- REPORT 2: Dead Stock

SELECT 
    p.ProductID,
    p.ProductName,
    c.CategoryName,
    p.StockCount
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE p.ProductID NOT IN (
    SELECT DISTINCT ProductID
    FROM SalesTransactions
    WHERE SaleDate >= DATE_SUB(CURDATE(), INTERVAL 60 DAY)
);


-- REPORT 3: Revenue by Category (Last Month)

SELECT 
    c.CategoryName,
    SUM(st.TotalAmount) AS TotalRevenue
FROM SalesTransactions st
JOIN Products p ON st.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE st.SaleDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY c.CategoryID, c.CategoryName
ORDER BY TotalRevenue DESC;