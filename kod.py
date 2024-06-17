#biblioteki
import cantera as c
import matplotlib.pyplot as plt
import numpy as np
gas = c.Solution('gri30.yaml')
x_ratios = np.zeros(6)

#zakres współczynnika nadmiaru powietrza
airfuel_ratios= np.linspace(0,3.5,500)

def comb_sim(x_ratios,af,gas):
	hydrogen = f'H2:{x_ratios[0]}'
	propane = f'C3H8:{x_ratios[1]}'
	methane = f'CH4:{x_ratios[2]}'
	acetylene = f'CO:{x_ratios[3]}'
	formic_acid = f'HCCOH:{x_ratios[4]}'
	acetaldehyde = f'CH3CHO:{x_ratios[5]}'

        #ilość moli zgodna z współczynnikiem nadmiaru powietrza
        stoichiometric_air = (0.5*x_ratios[0] + 5*x_ratios[1] + 2*x_ratios[2] + 2.5*x_ratios[3] + 2*x_ratios[4] + 2.5*x_ratios[5])
        air = f'O2:{af*stoichiometric_air}, N2:{af*stoichiometric_air*3.76}'

        #warunki początkowe 1 atmosfera, 300K
        gas.TPX = 300,c.one_atm,hydrogen + ',' + propane + ',' + methane + ',' + acetylene +','+ formic_acid + ',' + acetaldehyde +','+ air
        #adiabatyczne spalanie
        gas.equilibrate('HP')
        
        return gas.T,af

T_r = {}
af_r = {}
names = ['hydrogen H2', 'propane C3H8', 'methane CH4', 'acetylene C2H2', 'formic_acid HCCOH', 'acetaldehyde CH3CHO']
Tmax_af = []

#iterowanie po wszystkich składnikach
for i in range(6):
    x_ratios[i] = 1
    T_r[i] = []
    af_r[i] = []
    Tmax_af_temp = [0,0]
    Tmax_temp = 0
    #iteracja po współczynnikach nadmiaru powietrza 
    for af in airfuel_ratios:
            results = []
            results = comb_sim(x_ratios,af,gas)
            T_r[i].append(results[0])
            af_r[i].append(af)

            #wyznaczenie maksymalnej temperatury 
            #i odpowiadający jej współczynnik nadmiatu powietrza
            if results[0]>Tmax_temp:
                Tmax_temp = results[0]
                Tmax_af_temp = [results[0],af]
            Tmax_af.append(Tmax_af_temp)
    x_ratios[i]=0

    
print('wyniki')
print(Tmax_af)

#wykres
plt.figure(figsize=(8, 12))
for i in range(6):
	plt.plot(af_r[i], T_r[i], label=names[i])
	print(names[i])
plt.xlabel('air/fuel')
plt.ylabel('Temperature (K)')
plt.ylim(0, 3000)
plt.xlim(0, 3.5)
plt.yticks(range(0, 2801, 400))
plt.grid(True)
plt.legend()
plt.title('Temperature vs Air-fuel ratio for Different Fuels')
save_path = r'C:\Users\micha\Documents\sk\MKWS\plot1.png'
plt.savefig(save_path, dpi=500, bbox_inches='tight')
plt.show()
