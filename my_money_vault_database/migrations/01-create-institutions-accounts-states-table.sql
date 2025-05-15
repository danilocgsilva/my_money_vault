CREATE TABLE institutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    institution_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    FOREIGN KEY (institution_id) REFERENCES institutions(id)
);

CREATE TABLE states (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);