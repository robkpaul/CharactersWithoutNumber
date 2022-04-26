import json, re, random
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'type': 'connection_established'}))
    
    def receive(self, text_data):
        response = 'invalid command'
        text_data_json = json.loads(text_data)
        
        if(text_data_json['message'] != ''):
            message = str(text_data_json['message']).split()
            dice_pattern = re.compile("^d(4|8|10|12|20|100)$") # accepts dice rolls that are 4, 8, 10, 12, 20, and 100
            result = re.match(dice_pattern, message[0])
            if result: 
                die_num = int(message[0][1:])
                response = random.randint(1, die_num)
                self.send(text_data=json.dumps({'type': 'dice_roll', 'roll': response}))
        print(response)