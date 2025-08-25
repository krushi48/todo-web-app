# import FreeSimpleGUI as sg
#
# label1 = sg.Text("Enter feet: ")
# input1 = sg.Input()
#
# label2 = sg.Text("Enter inches: ")
# input2 = sg.InputText()
#
# button = sg.Button("Convert")
#
# window = sg.Window("Convertor", layout=[
#     [label1, input1],
#     [label2, input2],
#     [button]
# ])
# window.read()
# window.close()

import FreeSimpleGUI as sg

label = sg.Text("What are dolphins?")
option1 = sg.Radio("Amphibians", group_id="question1")
option2 = sg.Radio("Fish", group_id="question1")
option3 = sg.Radio("Mammals", group_id="question1")
option4 = sg.Radio("Birds", group_id="question1")

window = sg.Window("File Compressor",
                   layout=[[label],
                           [[option1],
                            [option2],
                            [option3],
                            [option4]],
                           ])

window.read()
window.close()