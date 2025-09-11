import FreeSimpleGUI as sg

label_feet = sg.Text('Enter feet')
inputBox_feet = sg.Input(key='feet')
label_inc = sg.Text('Enter inches')
inputBox_inc = sg.Input(key='inches')
convert_button = sg.Button('Convert')
resultText = sg.Text(key='result')

window = sg.Window('Convertor', layout=[[label_feet, inputBox_feet],[label_inc, inputBox_inc],[convert_button, resultText]])
while True:
    event, values = window.read()
    print(event, values)
    result = (float(values['feet'])*0.3048)+(float(values['inches'])*0.0254)
    window['result'].update(value=result)

window.close()