# from data.config import API_TOKEN

# baseUrl = "https://dbop.infinbank.com:9443/api/v2"
baseUrl = "https://dev.infinbank.com:22443/api/test"
# baseUrl = "http://127.0.0.1:8000"
verify_headers = {
    'Content-Type': 'application/json',
    'os': 'WEB',
    'deviceId': 'InfinBank Web',
    'serial': 'webcd1cdc8580b3298fd6bacd2518a99e23',
    'lang': 'ru'
}
image_headers = {
    'os': 'WEB',
    'deviceId': 'InfinBank Web',
    'serial': 'webcd1cdc8580b3298fd6bacd2518a99e23',
}