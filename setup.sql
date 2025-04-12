-- Create Vehicles table
CREATE TABLE IF NOT EXISTS Vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    type TEXT NOT NULL,
    capacity INTEGER NOT NULL
);

-- Create Routes table
CREATE TABLE IF NOT EXISTS Routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    stops TEXT NOT NULL
);

-- Create Schedules table
CREATE TABLE IF NOT EXISTS Schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    route_id INTEGER NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    schedule_date DATE NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(id),
    FOREIGN KEY (route_id) REFERENCES Routes(id)
);

-- Create Passengers table
CREATE TABLE IF NOT EXISTS Passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT NOT NULL
);

-- Create Bookings table
CREATE TABLE IF NOT EXISTS Bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    schedule_id INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES Passengers(id),
    FOREIGN KEY (schedule_id) REFERENCES Schedules(id)
);
INSERT INTO Routes (source, destination, stops)
VALUES
('DELHI', 'MUMBAI', 'SURAT, PUNE'),
('DELHI', 'BANGALORE', 'HUBLI, BELGAVI');
INSERT INTO Vehicles (number, type, capacity)
VALUES
('DL23CS45', 'Bus', 50),
('MH3C344', 'Train', 150);
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

