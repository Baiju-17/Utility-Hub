import pyttsx3
from rich.table import Table
from rich.console import Console
from rich import print

text = input('enter here: ')
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate',160)



console = Console()


def create_table():
    
    speak('sir enter the name of your table title')
    table = Table(title=input('enter title:'))
    speak('enter the name of first column , sir')
    col1 = input('enter col one:')
    speak('enter the name of second column , sir')
    col2 = input('enter col two:')
    speak('two size of column table created , sir , please look')
    
    table.add_column(col1)
    table.add_column(col2)
    
    console.print(table)   
    speak('sir enter the first row details')
    table.add_row(input('name'),input('add'))
    speak('sir enter the Second row details')
    table.add_row(input('name'),input('add')) 
    speak('table is completed sir , please look') 
    
    console.print(table)  
    speak('is that good sir')
    if 'yes' in text:
        speak('thanks my lord')

if 'ct' in text:
    speak('okay sir')
    create_table()