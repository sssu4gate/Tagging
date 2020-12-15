
f = open('./blog.refined.tok.shuf.train.tsv','r')

s= f.read()
print(s.count('\t'))

f.close()
