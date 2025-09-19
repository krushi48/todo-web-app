import streamlit as st
import func as functions


def get_todos_with_status():
    try:
        with open('todos.txt', 'r') as file:
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


def write_todos_with_status(todos):
    with open('todos.txt', 'w') as file:
        for todo in todos:
            prefix = "[DONE] " if todo["completed"] else ""
            file.write(f"{prefix}{todo['text']}\n")


# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = get_todos_with_status()


def add_todo():
    new_todo = st.session_state["new_todo"].strip()
    if new_todo:
        todo_data = {"text": new_todo, "completed": False}
        st.session_state.todos.append(todo_data)
        write_todos_with_status(st.session_state.todos)
        st.session_state["new_todo"] = ""


def delete_todo(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        deleted_todo = st.session_state.todos.pop(todo_index)
        write_todos_with_status(st.session_state.todos)


def toggle_todo_completion(todo_index):
    if 0 <= todo_index < len(st.session_state.todos):
        st.session_state.todos[todo_index]["completed"] = not st.session_state.todos[todo_index]["completed"]
        write_todos_with_status(st.session_state.todos)


st.title("My Todo App")
st.subheader("This is my todo app.")

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
