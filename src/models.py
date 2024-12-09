from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # You can change this to another database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    due_date = db.Column(db.String(50))
    description = db.Column(db.String(200))
    priority = db.Column(db.String(50))
    task_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='pending')  # Add the 'status' column

    def __repr__(self):
        return f'<Task {self.title}>'


    def __repr__(self):
        return f'<Task {self.title}>'

# Create the database and tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
'''


'''

