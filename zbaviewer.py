from zbadocument import ZbaDocument


# TODO: check for missing lists
# with open("data/apr1.txt") as f:
# with open("data/gk41.txt") as f:
# with open("data/pln1-.001") as f:
# with open("data/pln1-.002") as f:
with open("data/23_test-/test09.txt") as f:
    content = ''.join(f.readlines())

doc = ZbaDocument.from_string(content)
print(doc)
print("--- AF list ---")
for af in doc.afield_list:
    print(af)

# for tf in doc.afield_list[0].tfield_list:
#     print(tf)
# t = "1,1,1,1"
#
# x1, x2, x3, x4, x5 = t.split(",")
#
# print(x1)
# print(x2)
# print(x3)
# print(x4)
# print(x5)

# outfile = open("test.txt", "w")
# outfile.write(content)
# outfile.close()
