from sqlalchemy import insert, text
from app.database import database
from app.models import models
from app.utils.crypto import hash

admin = {
    "email": "n2gv32i3sfm@mail.com",
    "password": "jkObY05yCrxF18Uz2te6lTZMPNqEhfQpWAowdVca9IH7",
    "role": "admin",
}

manager = {
    "email": "vlrwk0gplj9@mail.com",
    "password": "jkObY05yCrxF18Uz2te6lTZMPNqEhfQpWAowdVca9IH7",
    "role": "manager",
}

try:
    with database.engine.connect() as conn:
        conn.execute(
            text(
                f"INSERT INTO users (email, password,role) VALUES ('{admin['email']}','{hash(admin['password'])}','{admin['role']}')"
            )
        )
        conn.execute(
            text(
                f"INSERT INTO users (email, password,role) VALUES ('{manager['email']}','{hash(manager['password'])}','{manager['role']}')"
            )
        )
        conn.commit()
except Exception as e:
    print(e)
    print("Admin and manager already exist in db")

print("Admin and Manager created successfully\n")
print("admin-username: ", admin["email"], "\nadmin-password: ", admin["password"])
print(
    "\nmanager-username: ",
    manager["email"],
    "\nmanager-password: ",
    manager["password"],
)
