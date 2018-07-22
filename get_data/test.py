import numpy as np
scale = 0.15
m = 0

b = [0,0,0,0,0,0,0]
max1 = 0
while m<1000000:
   #np.random.seed(4)
   a = np.random.normal(scale = scale)
   #print(a)
   if(a > max1):
      max1 = a
   #0 -1
   if a >= -0.1 and a < 0:
      b[0] = b[0] + 1
   #-1  0
   elif a >= 0 and a < 0.1:
      b[1] = b[1] + 1
   # 1 - 5
   elif a >= -0.25 and a < -0.1:
      b[2] = b[2] + 1
   #-5   -1
   elif a >= 0.1 and a < 0.25:
      b[3] = b[3] + 1
   # 1 - 5
   elif a >= -0.5 and a < -0.25:
      b[4] = b[4] + 1
   #-5   -1
   elif a >= 0.25 and a < 0.5:
      b[5] = b[5] + 1
   else:
      b[6] = b[5] + 1
   m = m + 1


print(b,max1)



