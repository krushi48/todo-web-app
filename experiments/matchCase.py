todos = []



while True:
    user_action = input("Enter options below to function\n 1. add\n 2. show\n").strip()
    #user_action = user_action.strip()

    match user_action:
        case '1':
            todo = input("Enter a todo: ")
            todos.append(todo)
        case '2':
            print(todos)
            for item in todos:
                print(item)
            break

