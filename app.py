import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from datetime import datetime
import re
from PIL import Image
# ------------------ Page Configuration --------------------
st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")
st.markdown("""
    <style>
        /* Main app background */
        .stApp {
            background-color: #fffaf0;  /* Floral White */
            color: #333333;  /* Dark gray text for readability */
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #f5f5dc;  /* Beige */
            color: #333333;  /* Dark text in sidebar */
        }

        /* Force headings and body text to be dark */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #333333 !important;
        }

        # /* Adjust spacing and layout */
        # .block-container {
        #     padding-top: 1rem;
        # }
    </style>
    """, unsafe_allow_html=True)
# st.markdown(
#     '<style>div[data-baseweb="select"]{background:black;color:white;} '
#     'div[data-baseweb="select"] *{color:white !important;} '
#     'div[data-baseweb="popover"] div{color:white !important; background:black !important;}</style>',
#     unsafe_allow_html=True
# )


# ------------------ Styling --------------------
st.markdown("""
    <style>
    .main {padding-top: 1rem;}
    .stButton>button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        margin-top: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stDataFrameContainer {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ DB Connection --------------------
def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Roshan@123",
            database="library"
        )
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# ------------------ Initialize Session State --------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome"

# ------------------ Login System --------------------
def login():
    # st.set_page_config(layout="wide")  # Set full width layout

    # Create 2 columns: left for image, right for login
    col1, col2 = st.columns([3, 2])  # Adjust ratio as needed

    with col1:
        img = Image.open("library_banner.jpg")
        st.image(img, use_container_width=True)

    with col2:
        st.markdown("### 👩‍💼 Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
                data = cursor.fetchone()
                conn.close()
                if data:
                    st.success("Login Successful ✅")
                    st.session_state["logged_in"] = True
                    st.session_state["page"] = "Welcome"
                    st.rerun()
                else:
                    st.error("Incorrect Username or Password ❌")
            else:
                st.error("Kindly Download this project in your local computer and connect" \
                            " with your MySql Database")            

# ------------------ Student Registration --------------------
def register_student():
    st.markdown("### 📝 Register New Student")
    student_id = st.number_input("Student ID", min_value=1)
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email")
    st.markdown(
    '<style>div[data-baseweb="select"]{background:black;color:white;} '
    'div[data-baseweb="select"] *{color:white !important;} '
    'div[data-baseweb="popover"] div{color:white !important; background:black !important;}</style>',
    unsafe_allow_html=True
)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone_no = st.text_input("Phone Number")
    student_pass = st.text_input("Password", type="password")

    if st.button("Register Student"):
        if not all([fname, lname, email, phone_no, student_pass]):
            st.error("All fields are required!")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Invalid email format!")
            return
        if not re.match(r"^\d{10}$", phone_no):
            st.error("Phone number must be 10 digits!")
            return

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM student WHERE student_id = %s OR email = %s", (student_id, email))
                if cursor.fetchone():
                    st.error("Student ID or Email already exists!")
                else:
                    cursor.execute(
                        "INSERT INTO student (student_id, fname, lname, email, gender, phone_no, student_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (student_id, fname, lname, email, gender, phone_no, student_pass)
                    )
                    conn.commit()
                    st.success("Student registered successfully!")
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()

# ------------------ View Students --------------------
def view_student():
    st.markdown("### 👨‍🎓 All Students")
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT student_id, fname, lname, email, gender, phone_no FROM student", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

# ------------------ Add Book --------------------
def add_book():
    st.markdown("### ➕ Add New Book")
    book_id = st.number_input("Book ID", min_value=1)
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    published_year = st.number_input("Published Year", min_value=1000, max_value=datetime.now().year)

    if st.button("Add Book"):
        if not all([title, author, genre]):
            st.error("All fields are required!")
            return
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO books (book_id, title, author, genre, published_year) VALUES (%s, %s, %s, %s, %s)",
                    (book_id, title, author, genre, published_year)
                )
                conn.commit()
                st.success("Book added successfully!")
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()

# ------------------ View All Books --------------------
def view_books():
    st.markdown("### 📖 All Books")
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT * FROM books", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

# ------------------ Search Books --------------------
def search_books():
    st.markdown("### 🔍 Search Books")
    search_term = st.text_input("Enter Title, Author, or Genre")
    if search_term:
        conn = create_connection()
        if conn:
            query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s"
            df = pd.read_sql(query, conn, params=(f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            conn.close()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No books found.")

# ------------------ Borrow Book --------------------
def borrow_book():
    st.markdown("### 📕 Borrow a Book")
    student_id = st.number_input("Student ID", min_value=1)
    book_id = st.number_input("Book ID", min_value=1)
    borrow_date = st.date_input("Borrow Date", value=datetime.today())
    return_date = st.date_input("Expected Return Date")

    if st.button("Borrow"):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
            if not cursor.fetchone():
                st.error("Student not registered!")
                return
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
            if not cursor.fetchone():
                st.error("Invalid Book ID!")
                return
            try:
                cursor.execute(
                    "INSERT INTO borrow_records (student_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
                    (student_id, book_id, borrow_date, return_date)
                )
                conn.commit()
                st.success("Book borrowed successfully!")
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()

# ------------------ Return Book --------------------
def return_book():
    st.markdown("### 💗 Return a Book")
    borrow_id = st.number_input("Borrow ID", min_value=1)
    actual_return_date = st.date_input("Actual Return Date", value=datetime.today())

    if st.button("Return"):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, return_date FROM borrow_records WHERE borrow_id = %s", (borrow_id,))
            record = cursor.fetchone()

            if record:
                _, expected_return_date = record
                fine = max((actual_return_date - expected_return_date).days, 0) * 10

                try:
                    cursor.execute(
                        "UPDATE borrow_records SET return_date = %s, fine = %s WHERE borrow_id = %s",
                        (actual_return_date, fine, borrow_id)
                    )
                    conn.commit()
                    st.success(f"Book returned! Fine: ₹{fine}")
                except mysql.connector.Error as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Invalid Borrow ID.")
            conn.close()

# ------------------ Borrow History --------------------
def view_borrow_history():
    st.markdown("### 🕑 Borrow History")
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT * FROM borrow_records", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.markdown("""
        <style>
        .stDownloadButton button {background-color: #4CAF50; color: white;}
        </style>
        """, unsafe_allow_html=True)

        st.download_button("Download Borrow History CSV", data=csv, file_name='borrow_history.csv', mime='text/csv')

# ------------------ Visualization --------------------
def visualize_borrow_trends():
    st.markdown("### 📊 Borrowing Trends")
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT borrow_date FROM borrow_records", conn)
        conn.close()
        if not df.empty:
            df['borrow_date'] = pd.to_datetime(df['borrow_date'])
            df['month'] = df['borrow_date'].dt.month_name()
            fig = px.histogram(df, x='month', title='Books Borrowed Each Month')
            st.plotly_chart(fig)
        else:
            st.warning("No borrowing records yet!")

# ------------------ Welcome Page --------------------
def welcome_page():
    # st.markdown("## 📚 Welcome to Library Management System")
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
   

    # st.image("library_banner.jpg")
    # st.markdown("""
    # <style>
    #     /* Main app background */
    #     .stApp {
    #         background-color: #fffaf0;  /* Floral White */
    #         color: #333333;  /* Dark gray text for readability */
    #     }

    #     /* Sidebar background */
    #     section[data-testid="stSidebar"] {
    #         background-color: #f5f5dc;  /* Beige */
    #         color: #333333;  /* Dark text in sidebar */
    #     }

    #     /* Force headings and body text to be dark */
    #     h1, h2, h3, h4, h5, h6, p, span, div {
    #         color: #333333 !important;
    #     }

    #     /* Adjust spacing and layout */
    #     .block-container {
    #         padding-top: 1rem;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # st.markdown("""
    # <style>
    #     /* Hide Streamlit's default hamburger menu and footer */
    #     #MainMenu, footer {visibility: hidden;}

    #     /* Remove black horizontal line behind top bar */
    #     .css-18ni7ap.e8zbici2 {
    #         background-color: transparent;
    #         box-shadow: none;
    #     }

    #     /* Optional: reduce padding to save space */
    #     .block-container {
    #         padding-top: 1rem;
    #     }
    # </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .welcome-title {
        margin-bottom: 0.2rem;
    }
    .welcome-subtitle {
        margin-top: 0.2rem;
    }
    </style>
    <h2 class="welcome-title">📚 Welcome to Library Management System</h2>
    <h4 class="welcome-subtitle"><span style="font-weight: 1500;">Manage your library efficiently with the following features:</span></h4>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        /* Reduce top padding of main content area */
        .block-container {
            padding-top: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)

    # st.write("#### Manage your library efficiently with the following features:")
    st.markdown("""
    - ✅ Add / View / Search Books
    - ✅ Register & Manage Students
    - ✅ Borrow and Return books
    - ✅ Track Borrow History
    - ✅ Analyze usage with Charts
    """)

# ------------------ Main --------------------
def main():
    
    if not st.session_state["logged_in"]:
        login()
        

    else:
        st.sidebar.image("library_banner.jpg", use_container_width=True)
        st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
        st.sidebar.markdown("### 📘 Menu")
        menu = [
            "Welcome",
            "Register Student",
            "View Students",
            "Add Book",
            "View All Books",
            "Search Books",
            "Borrow Book",
            "Return Book",
            "Borrow History",
            "Visualizations",
            "Logout"
        ]
        choice = st.sidebar.radio("Navigate", menu, index=menu.index(st.session_state["page"]))
        st.session_state["page"] = choice

        if choice == "Welcome":
            welcome_page()
        elif choice == "Register Student":
            register_student()
        elif choice == "View Students":
            view_student()
        elif choice == "Add Book":
            add_book()
        elif choice == "View All Books":
            view_books()
        elif choice == "Search Books":
            search_books()
        elif choice == "Borrow Book":
            borrow_book()
        elif choice == "Return Book":
            return_book()
        elif choice == "Borrow History":
            view_borrow_history()
        elif choice == "Visualizations":
            visualize_borrow_trends()
        elif choice == "Logout":
            st.session_state["logged_in"] = False
            st.session_state["page"] = "Welcome"
            st.rerun()

if __name__ == "__main__":
    main()
