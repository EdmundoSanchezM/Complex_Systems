def stringtoLATEX(fullpepos):
    temp = fullpepos.replace("*",'^\\ast')
    temp2 = temp.replace("$",'\\varepsilon')
    print(temp2)

a=""

b=""
c=" " 

d="(0 + 1(01)∗00) + (0 + 1(01)∗00)(ε + 0 + 0(01)∗00)∗(ε + 0 + 0(01)∗00)"
sentence = "("+a+")+("+b+")"+"("+c+")*"+"("+d+")"


xd = sentence.replace(" ", "")
xd1 = xd.replace("∗", "*")
xd2=xd1.replace("ε","$")
print("a reducir:")
print(xd2)
print("##############################")
stringtoLATEX(xd2)
print("##############################")
print("reducido uwu:")
fullpepos = "(01)*+(01)*00(0+0(01)*00)*0(01)*"
stringtoLATEX(fullpepos)
