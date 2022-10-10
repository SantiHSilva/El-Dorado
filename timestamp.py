from datetime import datetime

round()

# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = round(datetime.timestamp(dt),0)
print("El timestamp actual es de:", ts)

fecha_vencimiento = 1672435363
dia_vencimiento = datetime.fromtimestamp(fecha_vencimiento)
print(f"Dia vencimiento: {dia_vencimiento}" )
restar_10dias = fecha_vencimiento - 864000
dia_nuevo = datetime.fromtimestamp(restar_10dias)
print(f'Restandole 10 días {dia_nuevo}')

if(int(ts) <= int(restar_10dias)):
    print("Aun no vence")
else:
    print("Quedan 10 o menos días para que venzca")
