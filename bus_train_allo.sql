CREATE DATABASE IF NOT EXISTS ALLOCATEIT;
USE ALLOCATEIT;

-- Create the Vehicles table
CREATE TABLE IF NOT EXISTS Vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(20) NOT NULL,
    type ENUM('Bus', 'Train') NOT NULL,
    capacity INT NOT NULL
);

-- Create the Routes table
CREATE TABLE IF NOT EXISTS Routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    stops TEXT NOT NULL
);

-- Create the Schedules table
CREATE TABLE IF NOT EXISTS Schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    route_id INT NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    schedule_date DATE NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(id),
    FOREIGN KEY (route_id) REFERENCES Routes(id)
);

-- Create the Passengers table
CREATE TABLE IF NOT EXISTS Passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20) NOT NULL
);

-- Create the Bookings table
CREATE TABLE IF NOT EXISTS Bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT NOT NULL,
    schedule_id INT NOT NULL,
    seat_number INT NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES Passengers(id),
    FOREIGN KEY (schedule_id) REFERENCES Schedules(id)
);

-- Optional: Adding some example data for Vehicles
INSERT INTO Vehicles (number, type, capacity)
VALUES
('DL23CS45', 'Bus', 50),
('MH3C344', 'Train', 150);

-- Optional: Adding some example data for Routes
INSERT INTO Routes (source, destination, stops)
VALUES
('DELHI', 'MUMBAI', 'SURAT, PUNE'),
('DELHI', 'BANGALORE', 'HUBLI, BELGAVI');

-- Optional: Adding some example data for Schedules
INSERT INTO Schedules (vehicle_id, route_id, departure_time, arrival_time, schedule_date)
VALUES
(1, 1, '08:00:00', '14:00:00', '2025-04-15'),
(2, 2, '09:00:00', '16:00:00', '2025-04-16');

-- Optional: Adding some example data for Passengers
INSERT INTO Passengers (name, contact)
VALUES
('MOHAN', '1234567890'),
('SHAM', '0987654321');

-- Optional: Adding some example data for Bookings
INSERT INTO Bookings (passenger_id, schedule_id, seat_number)
VALUES
(1, 1, 12),
(2, 2, 34);
