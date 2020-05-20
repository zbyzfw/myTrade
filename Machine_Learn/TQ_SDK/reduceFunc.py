#%%
from functools import reduce

'''
reduce的用法

reduce(function, sequence[, initial]) -> value

Apply a function of two arguments cumulatively to the items of a sequence,
from left to right, so as to reduce the sequence to a single value.
For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
of the sequence in the calculation, and serves as a default when the
sequence is empty.

意思就是对sequence连续使用function, 如果不给出initial, 则第一次调用传递sequence的两个元素, 以后把前一次调用的结果和sequence的下一个元素传递给function. 如果给出initial, 则第一次传递initial和sequence的第一个元素给function.'''
a = reduce(lambda x,y: x*(1-y), [0.05], 4247)
#输出 6
print(a)
reduce(lambda x, y: x+y, [1,2,3], 9)
#输出 15
reduce(lambda x,y: x+y, [1, 2, 3], 7)
#输出 13
#%%
'''
emp1.age = 7  # 添加一个 'age' 属性
emp1.age = 8  # 修改 'age' 属性
del emp1.age  # 删除 'age' 属性
你也可以使用以下函数的方式来访问属性：

getattr(obj, name[, default]) : 访问对象的属性。
hasattr(obj,name) : 检查是否存在一个属性。
setattr(obj,name,value) : 设置一个属性。如果属性不存在，会创建一个新属性。
delattr(obj, name) : 删除属性。
hasattr(emp1, 'age')    # 如果存在 'age' 属性返回 True。
getattr(emp1, 'age')    # 返回 'age' 属性的值
setattr(emp1, 'age', 8) # 添加属性 'age' 值为 8
delattr(emp1, 'age')    # 删除属性 'age'
'''
