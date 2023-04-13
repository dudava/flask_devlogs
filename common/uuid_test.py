import uuid
import time


# print(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.jpg'))
print(uuid.uuid1(node=uuid.getnode()))