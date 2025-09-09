file = open('Todo-App/todos.txt', 'r')
todos = file.readlines()
file.close()

while True:
    user_action = input("Type add, show, edit, complete or exit: ")
    user_action = user_action.strip()

    match user_action:
        case 'add':
            todo = input("Enter a todo: ") + "\n"
            todos.append(todo)
            file = open('Todo-App/todos.txt', 'w')
            file.writelines(todos)
            file.close()
        case 'show':
            for item in todos:
                print(item.strip('\n'))
        case 'edit':
            number = int(input("Number of the todo to edit: "))
            number = number-1
            todos[number] = input("Enter the new value: ")
        case 'complete':
            number = int(input("Enter number to remove item from list: "))
            todos.pop(number-1)
        case 'exit':
            break
        case _:
            print("You have entered a wrong command")