CREATE TABLE account_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    metadata_key VARCHAR(255) NOT NULL,
    metadata_value VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
