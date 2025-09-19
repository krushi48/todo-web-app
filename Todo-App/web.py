import streamlit as st
import func as functions
import uuid
import os

def get_user_id():
    """Get or create user ID"""
    if 'user_id' not in st.session_state:
        # Try to get from URL params first
        query_params = st.query_params
        if 'user' in query_params:
            st.session_state.user_id = query_params['user']
        else:
            # Generate new user ID
            st.session_state.user_id = str(uuid.uuid4())[:8]  # Short ID
            # Update URL with user ID
            st.query_params['user'] = st.session_state.user_id
    return st.session_state.user_id

def get_user_file(user_id):
    """Get user-specific file path"""
    if not os.path.exists("users"):
        os.makedirs("users")
    return f"users/todos_{user_id}.txt"

def get_todos_with_status(user_id):
    filepath = get_user_file(user_id)
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

def write_todos_with_status(todos, user_id):
    filepath = get_user_file(user_id)
    with open(filepath, 'w') as file:
        for todo in todos:
            prefix = "[DONE] " if todo["completed"] else ""
            file.write(f"{prefix}{todo['text']}\n")

# Get user ID
user_id = get_user_id()

# Initialize session state with user-specific todos
if 'todos' not in st.session_state:
    st.session_state.todos = get_todos_with_status(user_id)

def add_todo():
    new_todo = st.session_state["new_todo"].strip()
    if new_todo:
        todo_data = {"text": new_todo, "completed": False}
        st.session_state.todos.append(todo_data)
        write_todos_with_status(st.session_state.todos, user_id)
        st.session_state["new_todo"] = ""

def delete_todo(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        deleted_todo = st.session_state.todos.pop(todo_index)
        write_todos_with_status(st.session_state.todos, user_id)

def toggle_todo_completion(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        st.session_state.todos[todo_index]["completed"] = not st.session_state.todos[todo_index]["completed"]
        write_todos_with_status(st.session_state.todos, user_id)

# Header with user info
st.title("My Todo App")
st.subheader("This is my todo app.")

# Show user ID and sharing info
# col1, col2 = st.columns([3, 1])
# with col1:
#     st.info(f"Your ID: {user_id}")
# with col2:
#     if st.button("📋 Share Link"):
#         share_url = f"{st.get_option('browser.serverAddress')}:{st.get_option('browser.serverPort')}?user={user_id}"
#         st.code(share_url)

# Display all todos (no separation by completion status)
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([5, 1])

        with col1:
            # Checkbox that saves state to file when clicked
            st.checkbox(
                todo["text"],
                value=todo["completed"],
                key=f"checkbox_{i}",
                on_change=toggle_todo_completion,
                args=(i,)
            )

        with col2:
            # Delete button works regardless of checkbox status
            if st.button("x", key=f"delete_{i}", help=f"Delete: {todo['text']}"):
                delete_todo(i)
                st.rerun()
else:
    st.info("No todos yet! Add one below.")

st.text_input(
    label="Enter a todo",
    placeholder="Add new todo...",
    on_change=add_todo,
    key='new_todo'
)

# Instructions
# st.markdown("---")
# st.markdown("""
# **How it works:**
# - Each user gets a unique ID and their own todo list
# - Your todos are automatically saved and will persist when you return
# - Share your URL with others to let them access their own separate lists
# - Refresh the page anytime - your todos will remain!
# """)
