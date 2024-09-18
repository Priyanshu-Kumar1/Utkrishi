import requests

def get_address(lat, lon):
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey=38aeda82269f48b4b9c0daefd65ae9f5"
    response = requests.get(url)
    data = response.json()
    data = data["features"][0]["properties"]
    address = {
        "country": data.get("country", ""),
        "state": data.get("state", ""),
        "state_district": data.get("state_district", ""),
        "city": data.get("city", ""),
        "pincode": data.get("postcode", ""),
        "housenumber": data.get("housenumber", ""),
        "street": data.get("street", ""),
    }
    return address


if __name__ == "__main__":
    lat = 12.816868178227127
    lon = 80.03963143159984
    address = get_address(lat, lon)
    print(address)