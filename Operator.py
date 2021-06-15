import random as rnd

class Operator:

    def __init__(self, env, id, name, age):
        self.id = id
        self.name = name
        self.age = age
        self.steps = 0
        self.heart_rate = rnd.randrange(60,70)
        self.location = 1
        self.data_collection = env.process(self.data_collection(env))
    
    def data_collection(self, env):
        while True:
            with open("operators.csv",'a') as f:
                f.write(str(env.now) + ";" + str(self.id) + ";" + str(self.age) + ";" + str(self.steps) + ";" + str(self.heart_rate) + ";" + str(self.location) + "\n")
            yield env.timeout(5)

    def hr_variation_qa(self):
        self.heart_rate = rnd.randrange(rnd.randrange(60,70), int((220 - self.age) * (rnd.randrange(60,85)/100)))+10
        
            
    def walk(self,origin,destiny):
        step = 0.82
        total_steps = 0
        walking_time = 0
        avg_distance = 0
        if origin == 2:
            if destiny == 1:
                avg_distance = 14.5
            elif destiny == 3:
                avg_distance = 18.7
            self.location = destiny
        elif origin == 3:
            if destiny == 2:
                avg_distance = 18.7
            elif destiny == 4:
                avg_distance = 20.75
            self.location = destiny
        elif origin == 4:
            if destiny == 3:
                avg_distance = 20.75
            elif destiny == 5:
                avg_distance = 22.5
            self.location = destiny
        elif origin == 5:
            if destiny == 4:
                avg_distance = 22.5
            elif destiny == 6:
                avg_distance = 21.25
            self.location = destiny
        elif origin == 6:
            if destiny == 5:
                avg_distance = 21.25
            self.location = destiny
        else:
            avg_distance = 0
            self.location = origin
        total_steps = int(avg_distance * step)
        self.steps += total_steps
        walking_time = int(rnd.gauss((total_steps * 0.04), 0.2))
        self.heart_rate = rnd.randrange(rnd.randrange(60,70), int((220 - self.age) * (rnd.randrange(60,85)/100)))-10
        return walking_time