import chatterbot
import cherrypy
from chatterbot.conversation import Statement

class Server:
    def __init__(self, template_key, template_chat, bots, badwords=()):
        self.t_key = template_key
        self.t_chat = template_chat
        self.bots = bots
        self.badwords = badwords

    @cherrypy.expose
    def index(self, key=""):
        if key not in self.bots.keys():
            return self.t_key

        return self.t_chat.replace("(*KEY_HERE*)", key)

    @cherrypy.expose
    def api(self,  msg, key="EMPTY"):
        if key not in self.bots.keys():
            raise cherrypy.HTTPError(401, "کلید اشتباه!")
        msg_low = msg.lower()
        for badword in self.badwords:
            if badword in msg_low:
                raise cherrypy.HTTPError(403, "پیغام یک کلمه رکیک دارد: " + badword)
        res = self.bots[key].get_response(Statement(msg)).text
        print(msg, "/", res)
        return res

def a_chatbot_pls(read_only=False):
    return chatterbot.ChatBot("Kalpak", read_only=read_only)

                              

if __name__ == "__main__":
    t_key = ""
    t_chat = ""
    with open("./index_key.html") as fp:
        t_key = fp.read()
    with open("./index_chat.html") as fp:
        t_chat = fp.read()

    bots = {
        "EMPTY": a_chatbot_pls(True)
    }
    keys = (
        "DrKhaliliba0",
        "BSJbi0",
        "DeChickenkiller00001",
        "AuntS1399",
        "DynamicMemoryAllocation"
    )
    
    for key in keys:
        bots[key] = a_chatbot_pls(True)
    badwords = ("کیر", "کون", "مادرجنه", "پدرسگ")
    print(bots.keys())
    print(badwords)
    
    conf = {"global":
        {
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 57057
        }
    }
    cherrypy.quickstart(Server(t_key, t_chat, bots, badwords), "/", conf)
