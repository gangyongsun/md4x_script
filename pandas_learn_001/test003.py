import pandas as pd

first = pd.DataFrame({'item_id': ['a', 'b', 'c', 'b', 'd'], 'item_price': [1, 2, 3, 2, 4]})
other = pd.DataFrame({'item_id': ['a', 'b', 'f'], 'item_atr': ['k1', 'k2', 'k3']})
print(first)
print(other)

# print(first.join(other, lsuffix='_left', rsuffix='_right'))
# print(first.join(other.set_index('item_id'),on='item_id'))
print(first.join(other.set_index('item_id'),on='item_id',how='outer'))