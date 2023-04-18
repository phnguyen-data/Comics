import tkinter as tk
from PIL import Image, ImageTk
from Update import Update
from tkinter import ttk
import random
from lorem_text import lorem
import mysql.connector as sql
db = sql.connect(host="localhost", user="root", password="root", database="comics", port=3306, autocommit=True)
cursor = db.cursor(buffered=True)


class UserInfo:
    def __init__(self, window):
        self.window = window

        # self.user_data = {
        #     'avatar': 'images/orgasm.jpg',
        #     'username': 'Xern',
        #     'email': 'sonn.bi12-389@st.usth.edu.vn',
        #     'age': 20,
        #     'member_since': '28/11/2021',
        #     'user_role': 'administrator',
        #     'favorite': 'Spider-man',
        #     'comics_followed': 118,
        #     'comics_read': 135,
        #     'chapters_read': 2184
        # }

        # if user_data is None:
        user_data = {
            'avatar': 'images/orgasm.jpg',
            'username': None,
            'email': None,
            'age': None,
            'user_role': None,
            'favorite': None,
            'comics_followed': None,
        }

        self.user_data = user_data

    def show_user_info(self, event=None):
        self.user_info_window = tk.Toplevel()
        self.user_info_window.title("User Info")

        # Center the window on the screen
        window_width = 400
        window_height = 300
        screen_width = self.user_info_window.winfo_screenwidth()
        screen_height = self.user_info_window.winfo_screenheight()

        x_position = int((screen_width / 2) - (window_width / 2))
        y_position = int((screen_height / 2) - (window_height / 2))

        self.user_info_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # User's avatar
        avatar_image = Image.open(self.user_data['avatar'])
        avatar_image = avatar_image.resize((80, 80), Image.Resampling.LANCZOS)
        avatar_image_button = ImageTk.PhotoImage(avatar_image)

        avatar_label = tk.Label(self.user_info_window, image=avatar_image_button)
        avatar_label.image = avatar_image_button
        avatar_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), rowspan=6)

        # User's info
        username_label = tk.Label(self.user_info_window, text=f"Username: {self.user_data['username']}")
        username_label.grid(row=0, column=1, sticky=tk.W, pady=(10, 0))

        age_label = tk.Label(self.user_info_window, text=f"Age: {self.user_data['age']}")
        age_label.grid(row=1, column=1, sticky=tk.W)

        user_role_label = tk.Label(self.user_info_window, text=f"User Role: {self.user_data['user_role']}")
        user_role_label.grid(row=2, column=1, sticky=tk.W)

        favorite_label = tk.Label(self.user_info_window, text=f"About me: {self.user_data['favorite']}")
        favorite_label.grid(row=3, column=1, sticky=tk.W)

        comics_followed_label = tk.Label(self.user_info_window,
                                         text=f"Comics followed: {self.user_data['comics_followed']}")
        comics_followed_label.grid(row=4, column=1, sticky=tk.W)

        # Add a new column and configure it to expand
        self.user_info_window.columnconfigure(2, weight=1)

        # Button
        button = tk.Button(self.user_info_window, text="Update", command=self.update)
        button.grid(row=8, column=1, pady=(20, 10), sticky=tk.E + tk.W)
        button.configure(anchor='center')

        if self.user_data['user_role'] == 'user':
            button = tk.Button(self.user_info_window, text="Delete", command=self.hehe)
            button.grid(row=9, column=1, pady=(20, 10), sticky=tk.E + tk.W)
            button.configure(anchor='center')
        else:
            button = tk.Button(self.user_info_window, text="Show user list", command=self.show)
            button.grid(row=9, column=1, pady=(20, 10), sticky=tk.E + tk.W)
            button.configure(anchor='center')



    def update(self):
        Update(self.user_info_window)

    def hehe(self):
        data = self.user_data['username']
        cursor.execute("DELETE FROM table_name WHERE username = %s", data)

    def show(self):
        cursor.execute("SELECT * FROM users")
        datas = cursor.fetchall()

        # create a new Toplevel window
        tree_window = tk.Toplevel(self.user_info_window)
        tree_window.title("User List")

        # create the treeview widget and configure columns
        my_tree = ttk.Treeview(tree_window)
        my_tree["columns"] = ("Username", "Password", "Avatar", "Gmail", "Role", "Age", "About me", "Comics_followed")

        my_tree.heading("#0", text="ID")
        my_tree.heading("Username", text="Username")
        my_tree.heading("Password", text="Password")
        my_tree.heading("Avatar", text="Avatar")
        my_tree.heading("Gmail", text="Gmail")
        my_tree.heading("Role", text="Role")
        my_tree.heading("Age", text="Age")
        my_tree.heading("About me", text="About me")
        my_tree.heading("Comics_followed", text="Comics followed")
        count = 0
        for user in datas:
            my_tree.insert("", "end", text=count, values=(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7]))
            count = count + 1
        my_tree.pack()
