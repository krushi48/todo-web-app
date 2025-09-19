FILEPATH = "todos.txt"

def get_todos(filepath="todos.txt"):
    try:
        with open(filepath, 'r') as file_local:
            todos_local = file_local.readlines()
        return todos_local
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist

def write_todos(todos_arg, filepath = FILEPATH):
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)

if __name__ == "__main__":
    print("Hello")
    print(get_todos())
