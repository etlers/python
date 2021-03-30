# 파일을 입맛대로(pickle, glob, os.path)

import pickle

users = {'kim':'3kid9', 'sun80':'393948', 'ljm':'py90390'}
f = open('users', 'wb')
pickle.dump(users, f)
f.close()

f = open('users', 'rb')
a = pickle.load(f)
print(a)