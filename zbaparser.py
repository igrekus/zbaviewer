import zbadocument


# TODO: check for missing lists
# with open("apr1.txt") as f:
# with open("gk41.txt") as f:
with open("pln1-.001") as f:
    content = ''.join(f.readlines())

doc = zbadocument.ZbaDocument.from_string(content)
doc.dump()
doc.dump_afields()

# outfile = open("test.txt", "w")
# outfile.write(content)
# outfile.close()
