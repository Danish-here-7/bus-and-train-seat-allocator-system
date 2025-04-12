import streamlit as st
import sqlite3
from datetime import datetime, time, date

# ---------------- DB Connection ---------------- #
def get_connection():
    return sqlite3.connect("allocateit.db")

# ---------------- Table Creation ---------------- #
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            type TEXT NOT NULL,
            capacity INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            stops TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            route_id INTEGER NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            schedule_date TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES Vehicles(id),
            FOREIGN KEY (route_id) REFERENCES Routes(id)
        );

        CREATE TABLE IF NOT EXISTS Passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_id INTEGER NOT NULL,
            schedule_id INTEGER NOT NULL,
            seat_number INTEGER NOT NULL,
            FOREIGN KEY (passenger_id) REFERENCES Passengers(id),
            FOREIGN KEY (schedule_id) REFERENCES Schedules(id)
        );
    """)
    conn.commit()
    conn.close()

create_tables()

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="BUS AND TRAIN SEAT ALLOCATION", layout="wide")# css
st.markdown("""
    <style>

    .stApp {
            background: linear-gradient(to right, #ffd103, #17ceeb);
     }
    h2, .stHeader {
            color:#81cf34 ; text-align: center; font-weight:800;
            }
    .stButton>button {
            background-color: #ff6600; color: white; border-radius: 100px; padding: 10px 20px;
            }
    .stButton>button:hover {
            background-color: #28b7d4;
            }
    .stTextInput input {
            border: 2px solid #e01fcd; border-radius: 5px; padding: 10px;
            }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>BUS AND TRAIN SEAT ALLOCATION SYSTEM</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 14px; font-style: italic;'>by: DANIH,CHRISTY,DHANUSH,CHIRANTH</h3>", unsafe_allow_html=True)
role = st.selectbox("Login as", ["Select", "Admin", "Staff", "Passenger"])
st.write("---")

# ---------------- Admin ---------------- #
def admin_panel():
    st.subheader("Admin Dashboard")
    menu = st.selectbox("Select Option", ["Add Vehicle", "Add Route", "Assign Schedule", "View Bookings", "View Schedules"])

    conn = get_connection()
    cursor = conn.cursor()

    if menu == "Add Vehicle":
        number = st.text_input("Vehicle Number")
        vtype = st.selectbox("Vehicle Type", ["Bus", "Train"])
        cap = st.number_input("Capacity", 1)
        if st.button("Add Vehicle"):
            cursor.execute("INSERT INTO Vehicles (number, type, capacity) VALUES (?, ?, ?)", (number, vtype, cap))
            conn.commit()
            st.success("Vehicle Added")

    elif menu == "Add Route":
        src = st.text_input("Source")
        dest = st.text_input("Destination")
        stops = st.text_area("Stops (comma-separated)")
        if st.button("Add Route"):
            cursor.execute("INSERT INTO Routes (source, destination, stops) VALUES (?, ?, ?)", (src, dest, stops))
            conn.commit()
            st.success("Route Added")

    elif menu == "Assign Schedule":
        cursor.execute("SELECT id, number FROM Vehicles")
        vehicles = cursor.fetchall()
        cursor.execute("SELECT id, source, destination FROM Routes")
        routes = cursor.fetchall()

        vehicle = st.selectbox("Vehicle", [f"{v[0]} - {v[1]}" for v in vehicles])
        route = st.selectbox("Route", [f"{r[0]} - {r[1]} to {r[2]}" for r in routes])
        dep_time = st.time_input("Departure Time")
        arr_time = st.time_input("Arrival Time")
        sched_date = st.date_input("Date")

        if st.button("Assign"):
            v_id = int(vehicle.split(" - ")[0])
            r_id = int(route.split(" - ")[0])
            cursor.execute("INSERT INTO Schedules (vehicle_id, route_id, departure_time, arrival_time, schedule_date) VALUES (?, ?, ?, ?, ?)",
                           (v_id, r_id, str(dep_time), str(arr_time), str(sched_date)))
            conn.commit()
            st.success("Schedule Assigned")

    elif menu == "View Bookings":
        cursor.execute("""SELECT b.id, p.name, v.number, r.source, r.destination, s.schedule_date, s.departure_time, b.seat_number
                          FROM Bookings b
                          JOIN Passengers p ON b.passenger_id = p.id
                          JOIN Schedules s ON b.schedule_id = s.id
                          JOIN Vehicles v ON s.vehicle_id = v.id
                          JOIN Routes r ON s.route_id = r.id""")
        st.table(cursor.fetchall())

    elif menu == "View Schedules":
        cursor.execute("""SELECT s.id, v.number, r.source, r.destination, s.departure_time, s.arrival_time, s.schedule_date
                          FROM Schedules s
                          JOIN Vehicles v ON s.vehicle_id = v.id
                          JOIN Routes r ON s.route_id = r.id""")
        st.table(cursor.fetchall())

    conn.close()

# ---------------- Staff ---------------- #
def staff_panel():
    st.subheader("Staff Dashboard")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT s.id, v.number, r.source, r.destination, s.departure_time, s.arrival_time, s.schedule_date
                      FROM Schedules s
                      JOIN Vehicles v ON s.vehicle_id = v.id
                      JOIN Routes r ON s.route_id = r.id""")
    st.table(cursor.fetchall())

    if st.button("View Bookings"):
        cursor.execute("""SELECT b.id, p.name, v.number, r.source, r.destination, s.departure_time, b.seat_number
                          FROM Bookings b
                          JOIN Passengers p ON b.passenger_id = p.id
                          JOIN Schedules s ON b.schedule_id = s.id
                          JOIN Vehicles v ON s.vehicle_id = v.id
                          JOIN Routes r ON s.route_id = r.id""")
        st.table(cursor.fetchall())
    conn.close()

# ---------------- Passenger ---------------- #
def passenger_panel():
    st.subheader("Passenger Dashboard")
    name = st.text_input("Name")
    contact = st.text_input("Contact")

    if st.button("Register"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Passengers (name, contact) VALUES (?, ?)", (name, contact))
        conn.commit()
        st.success("Registered successfully. Your ID is: " + str(cursor.lastrowid))
        conn.close()

    st.markdown("---")
    st.subheader("Book Ticket")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT s.id, v.number, r.source, r.destination, s.departure_time, s.schedule_date
                      FROM Schedules s
                      JOIN Vehicles v ON s.vehicle_id = v.id
                      JOIN Routes r ON s.route_id = r.id""")
    schedules = cursor.fetchall()
    conn.close()

    if schedules:
        sched = st.selectbox("Select Schedule", [f"{s[0]} - {s[1]} from {s[2]} to {s[3]} at {s[4]} on {s[5]}" for s in schedules])
        pid = st.number_input("Passenger ID", min_value=1)
        seat = st.number_input("Seat Number", min_value=1)

        if st.button("Book"):
            sched_id = int(sched.split(" - ")[0])
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Bookings (passenger_id, schedule_id, seat_number) VALUES (?, ?, ?)", (pid, sched_id, seat))
            conn.commit()
            conn.close()
            st.success("Ticket Booked!")

        if st.button("View My Bookings"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT b.id, v.number, r.source, r.destination, s.departure_time, b.seat_number
                              FROM Bookings b
                              JOIN Passengers p ON b.passenger_id = p.id
                              JOIN Schedules s ON b.schedule_id = s.id
                              JOIN Vehicles v ON s.vehicle_id = v.id
                              JOIN Routes r ON s.route_id = r.id
                              WHERE p.id = ?""", (pid,))
            st.table(cursor.fetchall())
            conn.close()

# ---------------- Handle Role ---------------- #
if role == "Admin":
    admin_panel()
elif role == "Staff":
    staff_panel()
elif role == "Passenger":
    passenger_panel()
