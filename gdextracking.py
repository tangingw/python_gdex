import json
import requests
from bs4 import BeautifulSoup


def get_response(gdex_tracking):

    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "web2.gdexpress.com",
        "Referer": "http://web2.gdexpress.com/official/iframe/etracking_v2.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }

    data = {
        "capture": gdex_tracking,
        "redoc_gdex": "cnGdex",
        "Submit": "Track"
    }

    response = requests.post(headers["Referer"], data=data, headers=headers)
    return response.text


def track_package(gdex_tracking):

    markup_data = get_response(gdex_tracking)
    
    soup = BeautifulSoup(markup_data, "html5lib")

    result = soup.find_all("td")
        
    status_dict = dict()
    key_created = None

    for i in range(len(result[4:])):

        if i % 4 == 0 and result[4:][i].text != "\xa0":

            status_dict["item_" + str((i//4) + 1)] = dict()
            status_dict["item_" + str((i//4) + 1)]["tracking_number_" + str((i // 4))] = result[4:][i].text
            key_created = "item_" + str((i//4) + 1)

        else:
                
            if i % 4 == 1:
    
                event_name = "latest_event_" + str((len(result[4:]) // 4 ) - i // 4)
                status_dict[key_created][event_name] = dict()
                status_dict[key_created][event_name]["datetime"] = result[4:][i].text
                status_dict[key_created][event_name]["status"] = result[4:][i + 1].text
                status_dict[key_created][event_name]["location"] = result[4:][i + 2].text


    return json.dumps(status_dict, indent=4)
