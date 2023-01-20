import matplotlib.pyplot as plt

f = open("lx", "r")
x=[]
for t in f:
  size=len(t)
  x.append(float(t[:size - 1]))
f.close()
f = open("ly", "r")
y=[]
for t in f:
  size=len(t)
  y.append(float(t[:size - 1]))
f.close()
f = open("lt", "r")
time=[]
for t in f:
  size=len(t)
  time.append(float(t[:size - 1]))
print(x)
print(y)
print(time)
plt.plot(x,y)
plt.show()
