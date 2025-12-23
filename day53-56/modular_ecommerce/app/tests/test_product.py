import requests

response = requests.post('http://localhost:8000/auth/token', data={'username': 'admin@example.com', 'password': 'admin123'})
print('Login status:', response.status_code)
if response.status_code == 200:
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    product_data = {'name': 'Laptop', 'description': 'High-performance laptop', 'price': 999.99, 'stock': 10}
    resp = requests.post('http://localhost:8000/products/', json=product_data, headers=headers)
    print('Product status:', resp.status_code)
    print('Product response:', resp.text)
else:
    print('Login failed')