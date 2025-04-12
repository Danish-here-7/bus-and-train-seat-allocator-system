
import streamlit as st
import mysql.connector
from datetime import datetime

# ---------------- DB Connection ---------------- #
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",  # Replace with your password
        database="ALLOCATEIT"  # Changed database name
    )

st.set_page_config(page_title="BUS AND TRAIN ALLOCATION SYSTEM", layout="wide")# css
st.markdown("""
    <style>

    .stApp {
            background: linear-gradient(to right, #fcb603, #feb47b);
     }
    h2, .stHeader {
            color:#fc14f1 ; text-align: center; font-weight:800;
            }
    .stButton>button {
            background-color: #ff6600; color: white; border-radius: 100px; padding: 10px 20px;
            }
    .stButton>button:hover {
            background-color: #28b7d4;
            }
    .stTextInput input {
            border: 2px solid #2fbceb; border-radius: 5px; padding: 10px;
            }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🚌 BUS AND TRAIN SET ALLOCATION SYSTEM</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 14px; font-style: italic;'>BY:Danish,Christy,Dhanush,Chiranth</h3>", unsafe_allow_html=True)


# ---------------- Role Selection ---------------- #
role = st.selectbox("Sign in as", ["Select", "Admin", "Staff", "Passenger"])
st.write("---")

# ---------------- Admin Panel ---------------- #
def admin_panel():
    st.subheader("🧑‍💼 Admin Dashboard")
    menu = st.selectbox("Admin Options", ["Add Vehicle", "Add Route", "Delete Route", "Assign Schedule", "View Vehicles", "View Routes", "View Schedules", "View Bookings"])

    if menu == "Add Vehicle":
        vehicle_number = st.text_input("Vehicle Number")
        vehicle_type = st.selectbox("Vehicle Type", ["Bus", "Train"])
        capacity = st.number_input("Capacity", min_value=1)

        if st.button("Add Vehicle"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Vehicles (number, type, capacity) VALUES (%s, %s, %s)", (vehicle_number, vehicle_type, capacity))
            conn.commit()
            conn.close()
            st.success("Vehicle added successfully")

    elif menu == "Add Route":
        source = st.text_input("Source")
        destination = st.text_input("Destination")
        stops = st.text_area("Stops (comma-separated)")

        if st.button("Add Route"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Routes (source, destination, stops) VALUES (%s, %s, %s)", (source, destination, stops))
            conn.commit()
            conn.close()
            st.success("Route added successfully")

    elif menu == "Delete Route":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, source, destination FROM Routes")
        routes = cursor.fetchall()
        route_to_delete = st.selectbox("Select Route to Delete", [f"{r[0]} - {r[1]} to {r[2]}" for r in routes])
        if st.button("Delete Route"):
            route_id = int(route_to_delete.split(" - ")[0])
            cursor.execute("DELETE FROM Routes WHERE id = %s", (route_id,))
            conn.commit()
            conn.close()
            st.success("Route deleted successfully")

    elif menu == "Assign Schedule":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, number FROM Vehicles")
        vehicles = cursor.fetchall()
        cursor.execute("SELECT id, source, destination FROM Routes")
        routes = cursor.fetchall()

        vehicle_option = st.selectbox("Select Vehicle", [f"{v[0]} - {v[1]}" for v in vehicles])
        route_option = st.selectbox("Select Route", [f"{r[0]} - {r[1]} to {r[2]}" for r in routes])
        departure_time = st.time_input("Departure Time")
        arrival_time = st.time_input("Arrival Time")
        schedule_date = st.date_input("Schedule Date")

        if st.button("Assign Schedule"):
            v_id = int(vehicle_option.split(" - ")[0])
            r_id = int(route_option.split(" - ")[0])
            cursor.execute("INSERT INTO Schedules (vehicle_id, route_id, departure_time, arrival_time, schedule_date) VALUES (%s, %s, %s, %s, %s)",
                           (v_id, r_id, departure_time, arrival_time, schedule_date))
            conn.commit()
            conn.close()
            st.success("Schedule assigned successfully")

    elif menu == "View Vehicles":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehicles")
        vehicles = cursor.fetchall()
        st.table(vehicles)
        conn.close()

    elif menu == "View Routes":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Routes")
        routes = cursor.fetchall()
        st.table(routes)
        conn.close()

    elif menu == "View Schedules":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT s.id, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i'), TIME_FORMAT(s.arrival_time, '%H:%i'), s.schedule_date FROM Schedules s JOIN Vehicles v ON s.vehicle_id = v.id JOIN Routes r ON s.route_id = r.id")
        rows = cursor.fetchall()
        st.table(rows)
        conn.close()

    elif menu == "View Bookings":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT b.id, p.name, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i') AS departure_time, b.seat_number "
                       "FROM Bookings b "
                       "JOIN Passengers p ON b.passenger_id = p.id "
                       "JOIN Schedules s ON b.schedule_id = s.id "
                       "JOIN Vehicles v ON s.vehicle_id = v.id "
                       "JOIN Routes r ON s.route_id = r.id")
        bookings = cursor.fetchall()
        st.table(bookings)
        conn.close()

# ---------------- Staff Panel ---------------- #
def staff_panel():
    st.subheader("🛠️ Staff Dashboard")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT s.id, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i'), TIME_FORMAT(s.arrival_time, '%H:%i'), s.schedule_date FROM Schedules s JOIN Vehicles v ON s.vehicle_id = v.id JOIN Routes r ON s.route_id = r.id")
    rows = cursor.fetchall()
    st.table(rows)
    conn.close()

    # View Bookings for Staff
    if st.button("View Bookings"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT b.id, p.name, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i') AS departure_time, b.seat_number "
                       "FROM Bookings b "
                       "JOIN Passengers p ON b.passenger_id = p.id "
                       "JOIN Schedules s ON b.schedule_id = s.id "
                       "JOIN Vehicles v ON s.vehicle_id = v.id "
                       "JOIN Routes r ON s.route_id = r.id")
        bookings = cursor.fetchall()
        st.table(bookings)
        conn.close()

# ---------------- Passenger Panel ---------------- #
def passenger_panel():
    st.subheader("👤 Passenger Dashboard")
    name = st.text_input("Your Name")
    contact = st.text_input("Contact Number")

    if st.button("Register"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Passengers (name, contact) VALUES (%s, %s)", (name, contact))
        conn.commit()
        passenger_id = cursor.lastrowid  # Get the auto-generated ID
        conn.close()
        st.success(f"Registered successfully! Your Passenger ID is {passenger_id}")

    st.markdown("---")
    st.markdown("### Book Ticket")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT s.id, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i'), s.schedule_date FROM Schedules s JOIN Vehicles v ON s.vehicle_id = v.id JOIN Routes r ON s.route_id = r.id")
    schedules = cursor.fetchall()
    conn.close()

    schedule = st.selectbox("Select Schedule", [f"{s[0]} - {s[1]} from {s[2]} to {s[3]} at {s[4]} on {s[5]}" for s in schedules])
    passenger_id = st.number_input("Passenger ID (get this after registration)", min_value=1)
    seat_number = st.number_input("Seat Number", min_value=1)

    if st.button("Book Ticket"):
        schedule_id = int(schedule.split(" - ")[0])
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Bookings (passenger_id, schedule_id, seat_number) VALUES (%s, %s, %s)", (passenger_id, schedule_id, seat_number))
        conn.commit()
        conn.close()
        st.success("Ticket booked successfully")

    # View Bookings for Passenger
    if st.button("View My Bookings"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT b.id, v.number, r.source, r.destination, TIME_FORMAT(s.departure_time, '%H:%i') AS departure_time, b.seat_number "
                       "FROM Bookings b "
                       "JOIN Passengers p ON b.passenger_id = p.id "
                       "JOIN Schedules s ON b.schedule_id = s.id "
                       "JOIN Vehicles v ON s.vehicle_id = v.id "
                       "JOIN Routes r ON s.route_id = r.id "
                       "WHERE p.id = %s", (passenger_id,))
        bookings = cursor.fetchall()
        st.table(bookings)
        conn.close()

# ---------------- Role Handling ---------------- #
if role == "Admin":
    admin_panel()
elif role == "Staff":
    staff_panel()
elif role == "Passenger":
    passenger_panel()
