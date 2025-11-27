from app import app, db

# אם הטבלאות לא קיימות הוא יוצר אותםֿ, מרצים קובץ זה פעם ראשונה בייצרת הפרויקט, ואם הם קיימות הוא לא יצור 
with app.app_context():
    db.create_all()
    print("Database tables created successfully (if they did not already exist).")


# This is all database of project

# CREATE TABLE users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     email VARCHAR(100) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE events (
#     event_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     title VARCHAR(255) NOT NULL,
#     description TEXT,
#     start_time DATETIME NOT NULL,
#     end_time DATETIME,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );


