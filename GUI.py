import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
import pymysql
import conn_db_functions as db
import pymysql.cursors

import final_db_config

# I was having timeout issues and this helped me diagnose them
from datetime import datetime


# Connect to the database
try:
    conn = pymysql.connect(host=final_db_config.DB_SERVER,
                      user=final_db_config.DB_USER,
                      password=final_db_config.DB_PASS,
                      database=final_db_config.DB)

except (Exception) as error:
    print("Error while connecting to MYSQL", error)
    exit()

# test the db connection by pulling a single record
# try:
#     with conn.cursor() as cursor:
#         sql = "Select * from movie_db.actors where `nconst`=%s"
#         cursor.execute(sql, ('nm0000001'))
#         rows = cursor.fetchall()
#         for row in rows:
#             print(row) # this was annoying me
# except (Exception) as error:
#     print("kill me", error)
#     exit()
# finally:
#     conn.close()
#
# rows = None
# num_of_rows = None
# row_counter = 0


# ==== form code ============


def start_app():
    # Initiates the window
    form = tk.Tk()
    # Window title
    form.title("Movie database")
    # Window size
    form.geometry("500x500")
    return form


def create_tabbed_menu(parent):
    print("create_tabbed_menu function initiated")
    # "Notebook" is a tabbed interface; will be a child entity of "parent"
    # If you don't provide parent, the stuff pops up as a separate window instead of putting it on the one you have
    tab_parent = ttk.Notebook(parent)
    # Create tabs; frames of the parent
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)

    # Makes the tabs viewable in the notebook
    tab_parent.add(tab1, text="Search by actor")
    tab_parent.add(tab2, text="Search by title")

    try:
        build_tab1(tab1)
    except Exception as e:
        print(e)
        raise Exception("Error building Tab 1")
    try:
        build_tab2(tab2)
    except Exception as e:
        print(e)
        raise Exception("Error building Tab 2")

    # expand argument means the user can drag the corner to change the size of the window;
    # fill="both" means the width and height of the window adjust
    tab_parent.pack(expand=1, fill='both')

    # This just exits the function; it's done its job at this point
    return True


def load_from_title_results(title_name, title_type):
    print("load_from_title function initiated")

    # I was having timeout issues
    # Seeing how long it took before timing out helped me figure out what parameter needed to change
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Query start =", current_time)

    try:
        # A function defined in the db_function.py file (provided by Dr. Nittel)
        conn = db.open_database()
    except Exception as e:
        raise Exception("Database connection error")
    try:
        sql = ("SELECT a.primaryName, t_known.primaryTitle AS knownForTitle " +
            "FROM movie_db.actors a " +
            "JOIN movie_db.knownFor kf_known ON a.nconst = kf_known.nconst " +
            "JOIN movie_db.titles t_known ON kf_known.tconst = t_known.tconst " +
            "WHERE a.nconst IN (" +
            "SELECT a2.nconst " +
            "FROM movie_db.actors a2 " +
            "JOIN movie_db.knownFor kf ON a2.nconst = kf.nconst " +
            "JOIN movie_db.titles t ON kf.tconst = t.tconst " +
            "WHERE lower(t.primaryTitle) = lower(%s) " +
            "AND t.titleType = %s)")
        res = db.query_database(conn, sql, (title_name, title_type))
    except Exception:
        raise Exception("Error querying the database")
    # print("query result:", res)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Query end =", current_time)
    return res[1]


def display_from_title_results(table, title_name, title_type):
    print("display_from_title_results function initiated")
    try:
        results = load_from_title_results(title_name, title_type)
        # Clear previous results (if form is used twice)
        for item in table.get_children():
            table.delete(item)
        # Insert new results
        for row in results:
            table.insert("", "end", values=(row[0], row[1]))  # assuming tuples
    except Exception as e:
        print("Error loading data from database:", e)


def load_from_actor_results(actor_name):
    print("load_from_actor function initiated")
    try:
        conn = db.open_database()
    except Exception as e:
        raise Exception("Database connection error")

    try:
        sql = ("select `primaryTitle` , `originalTitle` from movie_db.titles where tconst in " +
               "(select tconst from movie_db.knownFor where nconst in (select `nconst` " +
                        "from movie_db.actors where primaryName like %s))")
        # print(sql)
        res = db.query_database(conn, sql, actor_name)
    except Exception:
        raise Exception("Error querying the database")
    # print("query result:", res)
    return res[1]


def display_from_actor_results(table, actor_name):
    print("display_from_actor_results function initiated")
    try:
        results = load_from_actor_results(actor_name)
        # Insert new results
        for row in results:
            table.insert("", "end", values=(row[0], row[1]))  # assuming tuples
    except Exception as e:
        print("Error loading data from database:", e)


def actors_search_warning(u_input):
    try:
        conn = db.open_database()
    except Exception as e:
        raise Exception("Database connection error")

    try:
        sql = "select count(*) from movie_db.actors where primaryName like %s"
        res = db.query_database(conn, sql, u_input)

    except Exception:
        raise Exception("Error querying the database")
    return res[1][0][0]


def titles_search_warning(u_input, title_type):
    print("titles_search_warning function initiated")
    try:
        conn = db.open_database() # a function we defined in the db_function.py file
    except Exception as e:
        raise Exception("Database connection error")

    try:
        sql = "select count(*) from movie_db.titles where primaryTitle like %s and titleType = %s"
        # print(sql)
        res = db.query_database(conn, sql, (u_input, title_type))
        # print("res:", res)
        # print(res[1][0][0])
    except Exception:
        raise Exception("Error querying the database")

    return res[1][0][0]


def run_actor_query_with_status(label, label2, tab, u_input):
    print("run_actor_query_with_status function initiated")
    for item in tab.get_children():
        tab.delete(item)
    label.config(text="Loading...")
    label.update()
    label2.config(text="")
    label2.update()
    if actors_search_warning(u_input) > 1:
        label2.config(text="Warning: multiple actors match that name")
        label2.update()
    elif actors_search_warning(u_input) == 0:
        label2.config(text="No actors match that name")
        label2.update()
    display_from_actor_results(table=tab, actor_name=u_input)
    label.config(text="")
    label.update()


def run_title_query_with_status(label, label2, tab, u_input, title_type):
    print("run_title_query_with_status function initiated")
    for item in tab.get_children():
        tab.delete(item)
    # print(u_input)
    label.config(text="Loading...")
    label.update()
    label2.config(text="")
    label2.update()
    nmatch = titles_search_warning(u_input, title_type)
    if nmatch > 1:
        label2.config(text="Warning: multiple titles match that name")
        label2.update()
    elif nmatch == 0:
        label2.config(text="No titles match that name")
        label2.update()
    display_from_title_results(table=tab, title_name=u_input, title_type=title_type)
    label.config(text="")
    label.update()


def build_tab1(parent):
    print("build_tab1 function initiated")

    # Variable (empty now) that will hold the user input
    actor_name = tk.StringVar()
    # Create a label for the field and put it on the window
    tk.Label(parent, text="Enter actor name").grid(row=0, column=0, padx=5, pady=5)
    # Creates empty field which will be filled in by the user
    actor_entry = tk.Entry(parent, textvariable=actor_name)
    actor_entry.grid(row=0, column=1, padx=5, pady=5)

    # Empty field 1: "Loading" message will appear here
    status_label = tk.Label(parent, text="")
    status_label.grid(row=4, column=0, columnspan=2, pady=5)
    # Empty field 2: multiple or 0 matches found warning will appear here
    status_label2 = tk.Label(parent, text="")
    status_label2.grid(row=5, column=0, columnspan=2, pady=5)

    # Create the table where the results will appear
    table = ttk.Treeview(parent,
                         columns=("primaryTitle", "originalTile"),
                         show="headings")
    table.heading("primaryTitle", text="Title")
    table.heading("originalTile", text="Additional title")
    table.grid(row=6, column=0, columnspan=2, rowspan=1, padx=5, pady=5)

    # Make the go button
    display_button = tk.Button(parent,
                               text="Display results",
                               command=lambda: run_actor_query_with_status(label=status_label,
                                                                     label2=status_label2,
                                                               tab=table,
                                                               u_input=actor_name.get()))
    # Put it on the window
    display_button.grid(row=1, column=0, rowspan=3, padx=5, pady=5)
    # Make it work by hitting enter in addition to clicking the button
    actor_entry.bind("<Return>", lambda event: run_actor_query_with_status(
        label=status_label,
        label2=status_label2,
        tab=table,
        u_input=actor_name.get()))

    return True


def build_tab2(parent):
    print("build_tab2 function initiated")
    # A variable that will hold the title that is entered
    title_name = tk.StringVar()
    # Create a label for the field and put it on the window
    tk.Label(parent, text="Enter title").grid(row=0, column=0, padx=5, pady=5)
    # Creates empty field which will be filled in after db connect established, next
    title_entry = tk.Entry(parent, textvariable=title_name)
    # Put it on the window
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    status_label = tk.Label(parent, text="")
    status_label.grid(row=4, column=0, columnspan=2, pady=5)
    # Empty field 2: multiple matches found warning will appear here
    status_label2 = tk.Label(parent, text="")
    status_label2.grid(row=5, column=0, columnspan=2, pady=5)

    # This displays the selection
    lbl = Label(parent, text="")

    def show():
        lbl.config(text=opt.get())

    title_types = ['short', 'movie', 'tvShort', 'tvMovie', 'tvEpisode', 'tvSeries',
       'tvMiniSeries', 'tvSpecial', 'video', 'videoGame', 'tvPilot']

    # Selected option variable
    opt = StringVar(value="movie")

    # make a dropdown menu
    dropdown = tk.OptionMenu(parent, opt, *title_types)
    # put it somewhere
    dropdown.grid(row=1, column=1, padx=5, pady=5)

    # Dropdown label and placement
    tk.Label(parent, text="Select type").grid(row=1, column=0, padx=5, pady=5)

    table = ttk.Treeview(parent,
                         columns=("primaryName", "primaryTitle"),
                         show="headings")
    table.heading("primaryName", text="Actor name")
    table.heading("primaryTitle", text="Known for")
    table.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

    display_button = tk.Button(parent, text="Display results",
                               command=lambda: run_title_query_with_status(label=status_label,
                                                                    label2=status_label2,
                                                                    tab=table,
                                                                    u_input=title_name.get(),
                                                                    title_type=opt.get()
                                                                    )
                               )
    display_button.grid(row=3, column=0, rowspan=1, padx=15, pady=15)

    # This makes it so hitting return triggers the display button as well
    title_entry.bind("<Return>", lambda event: run_title_query_with_status(
        label=status_label,
        label2=status_label2,
        tab=table,
        u_input=title_name.get(),
        title_type=opt.get()
    ))



#=================================================================
#======================== MAIN APPLICATION =======================
#=================================================================

app = start_app()

try:
    create_tabbed_menu(app)
except Exception as e:
    print(e)
    messagebox.showinfo("Connected to Database", e)
    exit(0)

app.mainloop()