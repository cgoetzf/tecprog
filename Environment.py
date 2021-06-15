import simpy
import random

#-------------------------------------------------

class Marble_Factory:
    def __init__(self, env):
        self.env_noise = 60
        self.cutting_noise = 60
        self.polishing_noise = 60
        self.finishing_noise = 60
        self.env_temperature = 20
        self.cutting_temperature = 20
        self.polishing_temperature = 20
        self.finishing_temperature = 20
        self.data_collection = env.process(self.data_collection(env))
        self.temperature_variation = env.process(self.temperature_variation(env))

        self.slab = simpy.Container(env, capacity = 100, init = 100)
        self.tub_stock = simpy.Container(env, capacity = 100, init = 100)
        self.cutted_large_slab = simpy.Container(env, capacity = 200, init = 200)
        self.cutted_small_slab = simpy.Container(env, capacity = 100, init = 100)
        self.polished_large_slab = simpy.Container(env, capacity = 100, init = 100)
        self.polished_small_slab = simpy.Container(env, capacity = 200, init = 200)
        self.dispatch = simpy.Container(env ,capacity = 100, init = 0)

    def data_collection(self, env):
        yield env.timeout(0)
        while True:
            with open("environment.csv",'a') as f:
                f.write(str(env.now) + ";" + str(6) + ";" + str(self.env_temperature) + ";" + str(self.env_noise) + "\n")
                f.write(str(env.now) + ";" + str(5) + ";" + str(self.cutting_temperature) + ";" + str(self.cutting_noise) + "\n")
                f.write(str(env.now) + ";" + str(4) + ";" + str(self.polishing_temperature) + ";" + str(self.polishing_noise) + "\n")
                f.write(str(env.now) + ";" + str(3) + ";" + str(self.finishing_temperature) + ";" + str(self.finishing_noise) + "\n")
                f.write(str(env.now) + ";" + str(2) + ";" + str(self.env_temperature) + ";" + str(self.env_noise) + "\n")
            yield env.timeout(5)

    def temperature_variation(self, env):
        yield env.timeout(0)
        while True:
            if env.now <= 240:
                self.cutting_temperature += random.randrange(1,2)
                self.polishing_temperature += random.randrange(1,2)
                self.finishing_temperature += random.randrange(1,2)
            else:
                self.cutting_temperature -= random.randrange(1,2)
                self.polishing_temperature -= random.randrange(1,2)
                self.finishing_temperature -= random.randrange(1,2)
            yield env.timeout(60)


def quality_assurance(operator):
    qa_level = 0.9
    while qa_level < 1:
        qa_level = 1.1
        operator.hr_variation_qa()
        qa_level = random.gauss(qa_level, 0.1)
        
        if qa_level > 1:
            print('Qualidade: ' + operator.name + ' passou no teste.')
        else:
            print('Qualidade: ' + operator.name + ' não passou no teste!')

def cutting_process_large(env, marble_factory, operator):
    while True:
        yield env.timeout(operator.walk(5,6))
        yield marble_factory.slab.get(1)
        yield env.timeout(operator.walk(6,5))
        cutting_time = random.gauss(30, 0.1)
        marble_factory.cutting_noise += min(random.randrange(10,20),80)
        yield env.timeout(cutting_time)
        marble_factory.cutting_noise -= min(random.randrange(10,20),70)
        quality_assurance(operator)
        yield env.timeout(operator.walk(5,6))
        yield marble_factory.cutted_large_slab.put(1)
        print(operator.name + ' cortou 1 peça!')

def cutting_process_small(env, marble_factory, operator):
    while True:
        yield env.timeout(operator.walk(5,6))
        yield marble_factory.slab.get(1)
        yield env.timeout(operator.walk(6,5))
        cutting_time = random.gauss(8, 0.1)
        marble_factory.cutting_noise +=  min(random.randrange(10,20),80)
        yield env.timeout(cutting_time)
        marble_factory.cutting_noise -=  min(random.randrange(10,20),70)
        quality_assurance(operator)
        yield env.timeout(operator.walk(5,6))
        yield marble_factory.cutted_small_slab.put(5)
        print(operator.name + ' cortou 5 peças!')
        
def polishing_process(env, marble_factory, operator):
    while True:
        yield env.timeout(operator.walk(5,4))
        yield marble_factory.cutted_large_slab.get(1)
        yield env.timeout(operator.walk(4,5))
        yield env.timeout(operator.walk(5,4))
        yield marble_factory.cutted_small_slab.get(5)
        yield env.timeout(operator.walk(4,5))
        polishing_time = random.gauss(30, 0.1)
        marble_factory.polishing_noise +=  min(random.randrange(5,15),80)
        yield env.timeout(polishing_time)
        marble_factory.polishing_noise +=  min(random.randrange(5,15),70)
        quality_assurance(operator)
        yield env.timeout(operator.walk(4,3))
        yield marble_factory.polished_large_slab.put(1)
        yield env.timeout(operator.walk(3,4))
        yield marble_factory.polished_small_slab.put(5)
        print(operator.name + ' poliu 1 peça grande e 5 pequenas!')

def finishing_process(env, marble_factory, operator):
    while True:
        yield env.timeout(operator.walk(3,4))
        yield marble_factory.polished_large_slab.get(1)
        yield env.timeout(operator.walk(4,3))
        yield env.timeout(operator.walk(3,4))
        yield marble_factory.polished_small_slab.get(1)
        yield env.timeout(operator.walk(4,3))
        yield env.timeout(operator.walk(3,4))
        yield marble_factory.tub_stock.get(1)
        yield env.timeout(operator.walk(4,3))
        finishing_time = max(random.gauss(45, 0.1), 60  )
        yield env.timeout(finishing_time)
        quality_assurance(operator)
        yield env.timeout(operator.walk(5,6))
        yield marble_factory.dispatch.put(1)
        print(operator.name + ' finalizou um produto!')