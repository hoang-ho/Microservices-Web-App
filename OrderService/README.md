# Order Service
The order server supports a single operation: buy(item_number). Upon receiving a buy request, the order server must first verify that the item is in stock by querying the catalog server and then decrement the number of items in stock by one. The buy request can fail if the item is out of stock.

What to include in order logs ?

TODO: Describe the code structure and how to deploy this service 