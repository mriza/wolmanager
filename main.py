from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import re
import struct
import socket
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

csrf = CSRFProtect(app)  # Enable CSRF protection

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to send Wake-on-LAN magic packet
def send_wol(mac_address):
    # Validate MAC address format
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address):
        raise ValueError("Invalid MAC address format")

    mac_bytes = bytes.fromhex(mac_address.replace("-", "").replace(":", ""))
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(magic_packet, ('255.255.255.255', 9))  # Broadcast address

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):  # Compare hashed password
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        devices_count = conn.execute("SELECT COUNT(*) FROM devices").fetchone()[0]

    return render_template('dashboard.html', users=users_count, devices=devices_count)

# List users (Admin only)
@app.route('/users')
def users():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    with get_db_connection() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()

    return render_template('users.html', users=users)

# Add user (Admin only)
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Hash password
        role = request.form['role']

        with get_db_connection() as conn:
            try:
                conn.execute(
                    "INSERT INTO users (full_name, email, phone, username, password, role) VALUES (?, ?, ?, ?, ?, ?)",
                    (full_name, email, phone, username, password, role)
                )
                conn.commit()
                flash('User added successfully!', 'success')
            except sqlite3.IntegrityError:
                flash('Username already exists!', 'danger')
            except sqlite3.OperationalError:
                flash('An error occurred while adding the user.', 'danger')
                conn.rollback()

        return redirect(url_for('users'))

    return render_template('add_user.html')


# Edit user (Admin only)
@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

        if not user:
            flash('User not found!', 'danger')
            return redirect(url_for('users'))

        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            password = generate_password_hash(request.form['password'])  # Hash password
            role = request.form['role']

            try:
                conn.execute(
                    "UPDATE users SET full_name = ?, email = ?, phone = ?, password = ?, role = ? WHERE id = ?",
                    (full_name, email, phone, password, role, user_id)
                )
                conn.commit()
                flash('User updated successfully!', 'success')
            except sqlite3.OperationalError:
                flash('An error occurred while updating the user.', 'danger')
                conn.rollback()

            return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)

# Delete user (Admin only)
@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))

# Device management
@app.route('/devices')
def devices():
    if 'user' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        devices = conn.execute("SELECT * FROM devices").fetchall()

    return render_template('devices.html', devices=devices)

# Profile management
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (session['user'],)).fetchone()

        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            password_confirm = request.form['password_confirm']

            # Validate required fields
            if not full_name or not email or not phone:
                flash('Full Name, Email, and Phone are required fields.', 'danger')
                return redirect(url_for('profile'))

            # Validate email format
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                flash('Invalid email format.', 'danger')
                return redirect(url_for('profile'))

            # Validate password confirmation
            if password or password_confirm:
                if password != password_confirm:
                    flash('Passwords do not match.', 'danger')
                    return redirect(url_for('profile'))

                # Hash the new password
                password_hash = generate_password_hash(password)
            else:
                # Keep the current password if no new password is provided
                password_hash = user['password']

            try:
                conn.execute(
                    "UPDATE users SET full_name = ?, email = ?, phone = ?, password = ? WHERE username = ?",
                    (full_name, email, phone, password_hash, session['user'])
                )
                conn.commit()
                flash('Profile updated successfully', 'success')
            except sqlite3.OperationalError:
                flash('An error occurred while updating the profile.', 'danger')
                conn.rollback()

    return render_template('profile.html', user=user)

# Wake-on-LAN
@app.route('/wol', methods=['POST'])
def wol():
    if 'user' not in session:
        return redirect(url_for('login'))

    mac_address = request.form['mac_address']
    try:
        send_wol(mac_address)
        flash(f'Magic packet sent to {mac_address}', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)