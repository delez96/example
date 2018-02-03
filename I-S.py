import matplotlib.pyplot as plt
a=[137770,476.25]
b=[1044200,2714.8]
c=[2802900,6132.7]
d=[2939900,6388.7]
k=[2197300,7206.3]
h=[722070,2037.5]

plt.plot([a[1],h[1]],[a[0],h[0]])
plt.plot([h[1],b[1]],[h[0],b[0]])
plt.plot([b[1],c[1]],[b[0],c[0]])
plt.plot([c[1],d[1]],[c[0],d[0]])
plt.plot([d[1],k[1]],[d[0],k[0]])
plt.plot([k[1],a[1]],[k[0],a[0]])
plt.xlabel(r'$S, $ $ \frac {{Дж}}{{кгК}}$')
plt.ylabel(r'$i, $ $\frac {{Дж}}{{кг}}$')

plt.title('$T-S$ $диграмма$')
plt.grid(True)
plt.show()
print(r'i, \frac {{Дж}}{{кг}}')