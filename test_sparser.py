from sparser import Code_Parser

cp = Code_Parser("data.txt")
cp.parse()
print(cp.get_vaLue("f"))