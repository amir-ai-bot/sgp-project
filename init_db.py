import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from auth_utils import hash_password

def setup_database(pg_password):
    print("Connecting to PostgreSQL to setup the database...")
    try:
        # Connect to the default 'postgres' database as the 'postgres' superuser
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=pg_password,
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Create the sgp_user role
        try:
            cursor.execute("CREATE USER sgp_user WITH PASSWORD 'sgp_password';")
            print("[OK] User 'sgp_user' created.")
        except Exception as e:
            print(f"[INFO] User creation note: {e}")

        # Create the sgp_db database
        try:
            cursor.execute("CREATE DATABASE sgp_db OWNER sgp_user;")
            print("[OK] Database 'sgp_db' created.")
        except Exception as e:
            print(f"[INFO] Database creation note: {e}")
            
        cursor.close()
        conn.close()

        print("Connecting to the new 'sgp_db' database to create tables...")
        # Now connect to the newly created database with the new user
        conn_db = psycopg2.connect(
            dbname='sgp_db',
            user='sgp_user',
            password='sgp_password',
            host='localhost',
            port='5432'
        )
        cursor_db = conn_db.cursor()

        # Create Roles table
        cursor_db.execute("""
            CREATE TABLE IF NOT EXISTS Roles (
                id_role SERIAL PRIMARY KEY,
                nom_role VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        print("[OK] Table 'Roles' created.")

        # Create Utilisateurs table
        cursor_db.execute("""
            CREATE TABLE IF NOT EXISTS Utilisateurs (
                id_utilisateur SERIAL PRIMARY KEY,
                nom_utilisateur VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                mot_de_passe VARCHAR(255) NOT NULL,
                id_role INTEGER REFERENCES Roles(id_role) ON DELETE SET NULL
            );
        """)
        print("[OK] Table 'Utilisateurs' created.")

        # Insert default roles
        cursor_db.execute("""
            INSERT INTO Roles (nom_role) VALUES ('Admin'), ('Utilisateur')
            ON CONFLICT (nom_role) DO NOTHING;
        """)

        # Insert a default admin user (password 'admin123' will be hashed)
        hashed_pw = hash_password('admin123')
        cursor_db.execute("""
            INSERT INTO Utilisateurs (nom_utilisateur, email, mot_de_passe, id_role)
            VALUES ('Administrateur', 'admin@sgp.com', %s, 1)
            ON CONFLICT (email) DO NOTHING;
        """, (hashed_pw,))
        print("[OK] Default Admin user created.")

        conn_db.commit()
        cursor_db.close()
        conn_db.close()
        
        print("\n--- Setup Complete! ---")
        print("You can now connect to your application using:")
        print("Email: admin@sgp.com")
        print("Password: admin123")

    except psycopg2.OperationalError as e:
        print(f"\n[ERROR] Connection failed: {e}")
        print("Make sure your PostgreSQL password is correct and the server is running.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("This script will create the database 'sgp_db', user 'sgp_user', and the necessary tables.")
    pwd = input("Please enter your PostgreSQL 'postgres' user password: ")
    setup_database(pwd)
