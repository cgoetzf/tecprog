import simpy
import Environment as e
import Operator as op
import random as rnd

#tempo de trabalho em minutos - 8 horas
working_time = 480

#inicializando arquivos
with open("operators.csv",'w') as f:
                f.write("time;id;age;steps;hr;location\n")

with open("environment.csv",'w') as f:
                f.write("time;location;temperature;noise\n")

print(f'----------------------------------')
print(f'Iniciando simulação')
print(f'----------------------------------')

#criando ambiente de simulação
        
env = simpy.Environment()
marble_factory = e.Marble_Factory(env)

op1 = op.Operator(env,1,"Alex",31)
op2 = op.Operator(env,2,"Paulo",23)
op3 = op.Operator(env,3,"Pedro",47)
op4 = op.Operator(env,4,"Tomas",18)
op5 = op.Operator(env,5,"Roger",29)
op6 = op.Operator(env,6,"Vicente",52)
op7 = op.Operator(env,7,"Marcos",35)

env.process(e.cutting_process_large(env, marble_factory,op1))
env.process(e.cutting_process_large(env, marble_factory,op2))
env.process(e.cutting_process_small(env, marble_factory,op3))
env.process(e.polishing_process(env, marble_factory,op4))
env.process(e.finishing_process(env, marble_factory,op5))
env.process(e.finishing_process(env, marble_factory,op6))
env.process(e.finishing_process(env, marble_factory,op7))

#executando simulação

env.run(until = working_time)

#exibindo resultados do dia

print(f'----------------------------------')
print(f'Resultado do dia')
print(f'----------------------------------')
print('Lajes cortadas: {0} grandes {1} pequenas em estoque.'.format(
    marble_factory.cutted_large_slab.level, marble_factory.cutted_small_slab.level))
print('Lajes polidas: {0} grandes and {1} pequenas em estoque.'.format(
    marble_factory.polished_large_slab.level, marble_factory.polished_small_slab.level))
print(f'Produtos finalizados: %d' % marble_factory.dispatch.level)
print(f'----------------------------------')
print(f'Simulação completa')
print(f'----------------------------------')