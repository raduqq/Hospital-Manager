DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS assistants;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS treatments;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE assistants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    -- one doctor, many assistants
    doctor_id INTEGER,
    FOREIGN KEY(doctor_id) REFERENCES doctor(id)
);
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    health INTEGER NOT NULL DEFAULT 50,
    assistant_id INTEGER,
    treatment_id INTEGER,
    -- one asisstant, many patients
    FOREIGN KEY(assistant_id) REFERENCES assistant(id),
    -- one treatment, many patients 
    FOREIGN KEY(treatment_id) REFERENCES treatment(id)
);
CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    health_value INTEGER NOT NULL
);