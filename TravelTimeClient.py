from zeep import Client

client = Client('http://localhost:8000/?wsdl')
result = client.service.calculate_travel_time(100, 10, 10)
print(result)


