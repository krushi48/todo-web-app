import streamlit as st
import func as functions
import os


def get_all_usernames():
    """Get list of all existing usernames"""
    if not os.path.exists("users"):
        os.makedirs("users")

    usernames = []
    for filename in os.listdir("users"):
        if filename.startswith("todos_") and filename.endswith(".txt"):
            username = filename[6:-4]  # Remove "todos_" prefix and ".txt" suffix
            usernames.append(username)
    return usernames


def get_user_file(username):
    """Get user-specific file path"""
    if not os.path.exists("users"):
        os.makedirs("users")
    return f"users/todos_{username}.txt"


def get_todos_with_status(username):
    filepath = get_user_file(username)
    try:
        with open(filepath, 'r') as file:
            todos = []
            for line in file.readlines():
                line = line.strip()
                if line:
                    if line.startswith("[DONE] "):
                        todos.append({"text": line[7:], "completed": True})
                    else:
                        todos.append({"text": line, "completed": False})
            return todos
    except FileNotFoundError:
        return []


def write_todos_with_status(todos, username):
    filepath = get_user_file(username)
    with open(filepath, 'w') as file:
        for todo in todos:
            prefix = "[DONE] " if todo["completed"] else ""
            file.write(f"{prefix}{todo['text']}\n")


# Check if user is logged in
if 'username' not in st.session_state:
    st.session_state.username = None
    st.session_state.login_attempted = False

print(st.session_state.username is None)

# Login popup/modal
if st.session_state.username is None:
    # st.markdown("""
    # <div style="
    #     position: fixed;
    #     top: 0;
    #     left: 0;
    #     width: 100%;
    #     height: 100%;
    #     background-color: rgba(0,0,0,0.5);
    #     z-index: 999;
    #     display: flex;
    #     justify-content: center;
    #     align-items: center;
    # ">
    # </div>
    # """, unsafe_allow_html=True)

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
        """, unsafe_allow_html=True)

        st.title("🗒️ Welcome to Todo App")
        st.markdown("**Enter your name to access your personal todo list:**")

        # Get existing usernames
        existing_users = get_all_usernames()

        # Username input
        username_input = st.text_input(
            "Your Name:",
            placeholder="Enter your name (e.g., John, Sarah, etc.)",
            key="username_input"
        )

        col_login, col_view = st.columns(2)

        with col_login:
            if st.button("📝 Enter", use_container_width=True):
                if username_input.strip():
                    clean_username = username_input.strip().lower().replace(" ", "_")

                    # Check if username exists
                    if clean_username in existing_users:
                        st.success(f"Welcome back, {username_input}! 👋")
                        st.session_state.username = clean_username
                        st.session_state.display_name = username_input.strip()
                        st.rerun()
                    else:
                        st.info(f"Creating new todo list for {username_input} ✨")
                        st.session_state.username = clean_username
                        st.session_state.display_name = username_input.strip()
                        st.rerun()
                else:
                    st.error("Please enter a name!")

        with col_view:
            if st.button("👥 View All Users", use_container_width=True):
                if existing_users:
                    st.markdown("**Existing Users:**")
                    for user in sorted(existing_users):
                        display_user = user.replace("_", " ").title()
                        st.write(f"• {display_user}")
                else:
                    st.info("No users yet!")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()  # Stop execution until user logs in

# User is logged in - show the app
username = st.session_state.username
display_name = st.session_state.get('display_name', username)

# Initialize todos for this user
if 'todos' not in st.session_state:
    st.session_state.todos = get_todos_with_status(username)


def add_todo():
    new_todo = st.session_state["new_todo"].strip()
    if new_todo:
        todo_data = {"text": new_todo, "completed": False}
        st.session_state.todos.append(todo_data)
        write_todos_with_status(st.session_state.todos, username)
        st.session_state["new_todo"] = ""


def delete_todo(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        deleted_todo = st.session_state.todos.pop(todo_index)
        write_todos_with_status(st.session_state.todos, username)


def toggle_todo_completion(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        st.session_state.todos[todo_index]["completed"] = not st.session_state.todos[todo_index]["completed"]
        write_todos_with_status(st.session_state.todos, username)


def logout():
    st.session_state.username = None
    st.session_state.todos = []
    if 'display_name' in st.session_state:
        del st.session_state.display_name
    st.rerun()


# Header with user info
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"📝 {display_name}'s Todo App")
    # st.subheader("Manage your personal tasks")

with col2:
    if st.button("🚪 Logout", help="Switch to different user"):
        logout()

# Show user stats
total_todos = len(st.session_state.todos)
completed_todos = len([todo for todo in st.session_state.todos if todo["completed"]])
pending_todos = total_todos - completed_todos

# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Total Tasks", total_todos)
# with col2:
#     st.metric("Completed", completed_todos)
# with col3:
#     st.metric("Pending", pending_todos)

st.markdown("---")

# Display all todos
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.checkbox(
                todo["text"],
                value=todo["completed"],
                key=f"checkbox_{i}",
                on_change=toggle_todo_completion,
                args=(i,)
            )

        with col2:
            if st.button("❌", key=f"delete_{i}", help=f"Delete: {todo['text']}"):
                delete_todo(i)
                st.rerun()
else:
    st.info("🎉 No todos yet! Add your first task below.")

# Add new todo
st.markdown("### ➕ Add New Task")
st.text_input(
    label="Enter a todo",
    placeholder="What do you need to do?",
    on_change=add_todo,
    key='new_todo'
)

# Footer info
# st.markdown("---")
# st.markdown(f"""
# **ℹ️ How it works:**
# - Your todos are saved automatically as `{display_name}`
# - Use the logout button to switch users
# - Each person gets their own separate todo list
# - All data is persistent - your todos will be here when you return!
# """)
