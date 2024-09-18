import requests



def get_distance(origin, destinations):
    url = f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins={origin[0]},{origin[1]}&destinations={destinations[0]},{destinations[1]}&key=4cMmukgn0yfSvwhrmbviNslXTna5Eriyvt9wiBu1cEbTJFvK9vK9B3wc2OWPQb4z"

    response = requests.get(url)
    data = response.json()
    data = data["rows"][0]["elements"][0]

    dist_response = {
        "distance": data["distance"]["text"],
        "duration": data["duration"]["text"],
    }

    return data["distance"]["text"], data["duration"]["text"]