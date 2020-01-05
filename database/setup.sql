CREATE TABLE users(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       VARCHAR(50) NOT NULL,
    username    VARCHAR(50) NOT NULL,
    password    TEXT        NOT NULL,
    created     TEXT        NOT NULL,
    surname     VARCHAR(50) NOT NULL,
    firstname   VARCHAR(50) NOT NULL,
    status      VARCHAR(50) NOT NULL,
    gender      VARCHAR(1)
    );

CREATE TABLE patients(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    surname     VARCHAR(50) NOT NULL,
    firstname   VARCHAR(50) NOT NULL,
    created     TEXT        NOT NULL,
    birthday    TEXT        NOT NULL,
    phone       TEXT        NOT NULL,
    gender      VARCHAR(1)
    );

CREATE TABLE pat_measurements(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pat_id      INTEGER(10) NOT NULL,
    user_id     INTEGER(10) NOT NULL,
    title       VARCHAR(50) NOT NULL,
    created     TEXT        NOT NULL,
    FOREIGN KEY(pat_id)     REFERENCES patients(id),
    FOREIGN KEY(user_id)    REFERENCES users(id)
    );

CREATE TABLE pat_status(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pat_id      INTEGER(10) NOT NULL,
    user_id     INTEGER(10) NOT NULL,
    status      VARCHAR(50) NOT NULL,
    department  VARCHAR(50) NOT NULL,
    created     TEXT        NOT NULL,
    FOREIGN KEY(pat_id)     REFERENCES patients(id),
    FOREIGN KEY(user_id)    REFERENCES users(id)
    );

CREATE TABLE pat_diagnostics(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pat_id      INTEGER(10) NOT NULL,
    user_id     INTEGER(10) NOT NULL,
    diagnostics TEXT        NOT NULL,
    date        TEXT        NOT NULL,
    FOREIGN KEY(pat_id)     REFERENCES patients(id),
    FOREIGN KEY(user_id)    REFERENCES users(id)
    );