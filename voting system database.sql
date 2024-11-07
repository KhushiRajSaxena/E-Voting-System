CREATE DATABASE voting_system;

-- Table for storing voter details
CREATE TABLE voter_table (
    RollNo VARCHAR(12) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Sex ENUM('F', 'M', 'OTHER') NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Department ENUM('CSE', 'ET&T', 'IT', 'AI', 'AI/ML', 'CSE(AI)', 'CIVIL', 'MECHANICAL') NOT NULL,
    AdmissionYear YEAR NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

-- Table for storing user login details
CREATE TABLE user_table (
    vid VARCHAR(10) PRIMARY KEY,
    RollNo VARCHAR(12),
    Password VARCHAR(255) NOT NULL,
    FOREIGN KEY (RollNo) REFERENCES voter_table(RollNo)
);

-- Table for storing positions for which candidates can be nominated
CREATE TABLE positions (
    PositionId INT AUTO_INCREMENT PRIMARY KEY,
    PositionName VARCHAR(255) NOT NULL UNIQUE
);

-- Table for storing candidate details
CREATE TABLE candidates (
    CandidateId INT AUTO_INCREMENT PRIMARY KEY,
    PositionId INT,
    CandidateName VARCHAR(255) NOT NULL,
    FOREIGN KEY (PositionId) REFERENCES positions(PositionId)
);

-- Table for storing votes
CREATE TABLE votes (
    VoteId INT AUTO_INCREMENT PRIMARY KEY,
    RollNo VARCHAR(12),
    CandidateId INT,
    FOREIGN KEY (RollNo) REFERENCES voter_table(RollNo),
    FOREIGN KEY (CandidateId) REFERENCES candidates(CandidateId)
);
SELECT* FROM candidates;
DELETE FROM candidates
WHERE CandidateId  = "4";