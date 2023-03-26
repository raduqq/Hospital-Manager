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
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
    -- asssistant Id: daca cumva e 1-1 intre doctor-assistant
);

CREATE TABLE assistants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    -- one doctor, many assistants
    doctorId INTEGER,
    FOREIGN KEY(doctorId) REFERENCES doctor(id)
);

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    health INTEGER NOT NULL DEFAULT 100,
    assistantId INTEGER,
    recommendedTreatmentId INTEGER,
    -- one asisstant, many patients
    FOREIGN KEY(assistantId) REFERENCES assistant(id),
    -- one treatment, many patients 
    FOREIGN KEY(recommendedTreatmentId) REFERENCES treatment(id)
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    healthValue INTEGER NOT NULL
);