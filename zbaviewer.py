from zbadocument import ZbaDocument


# TODO: check for missing lists
# with open("data/apr1.txt") as f:
with open("data/gk41.txt") as f:
# with open("data/pln1-.001") as f:
# with open("data/pln1-.002") as f:
    content = ''.join(f.readlines())

doc = ZbaDocument.from_string(content)

# outfile = open("test.txt", "w")
# outfile.write(content)
# outfile.close()
