ban = False
for i in range(10):
    for j in range(5):
        if j == 3: 
            ban = True
            break
        print("i: ", i, " j: ", j)
    else:
        print("interno")
    if ban:
        break
else:
    print("externo")


