import copy
spisok=['москва', 'киев','астрахань','новосибирск','алжир','донецк','винница']
states={}
def game(chat_id,stroka):
    
    print(chat_id)
    if chat_id not in states:
        states[chat_id] = copy.copy(spisok)
    states[chat_id].remove(stroka)

game(1,'москва')

game(2,'киев')   

print(states)     