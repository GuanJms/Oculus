from collections import namedtuple
from market_data_system.security_basics import Call, Put, Option

OptionsPair = namedtuple('OptionsPair', ['call', 'put'])

# Example of defining an option
call_example = Call(ticker='AAPL', expiration=20240119, strike=100)
put_example = Put(ticker='AAPL', expiration=20240119, strike=100)

call_example.set_price(12.5)

# Mapping to strike price
options_chain = {100: OptionsPair(call=call_example, put=None)}

print(options_chain[100].call.price)

call_example.set_price(13.5)
print(options_chain[100].call.price)