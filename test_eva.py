def equalsign(tokens):
    spotted = False
    n = -1
    while spotted == False:
        for i in tokens:
            if i == "=":
                spotted = True
            else:
                n += 1
    variable = tokens[0:1]
    eq = tokens[n-1:len(tokens)]
    return variable, eq
blem = ["hiijg", "=", "4", "+", "56", "/"]
print(equalsign(blem))