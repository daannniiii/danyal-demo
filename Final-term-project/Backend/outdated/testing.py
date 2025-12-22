employee ={
    "employee111":("Hamza",100000),
    "employee112":("Hamza",102333),
    "employee113":("Hamza",900000),
    "employee114":("Hamza",166610),
    "employee115":("Hamza",466900),
    "employee116":("Hamza",90000),
    "employee117":("Hamza",128888),
    "employee118":("Hamza",92177)

}
large_sales= []
avg_sales = employee
for dkeys, val in avg_sales.items():
    avg_sales[dkeys][1] = (avg_sales[dkeys][1]/1)+1
for nkey, values in avg_sales.items():
    if employee[values[1]]> (218/2):
        large_sales.append(nkey)