from twilio.rest import Client
class Notification:
    def twilioWhatsAppAPI(text_=""):
        try:
            account_sid = 'AC2988655d43ae51c67524e2ad046b5e38' 
            auth_token = 'd5bbdc8cd2c5a10055ce417bf68c2425' 
            client = Client(account_sid, auth_token) 
            
            message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body=text_,      
                                    to='whatsapp:+919653406905' 
                                ) 
            
            #print(message.sid)
        except Exception as ex:
            print(str(ex))
        