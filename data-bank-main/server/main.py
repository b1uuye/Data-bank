import sys

import datetime
import json
import random
import uuid

from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "localhost"
PORT = 5000


class DataGenerator:
    locations = ["north", "south", "east", "west"]

    def _water_ph(self):
        sensor_ids = ["01-wph", "02-wph", "03-wph", "04-wph", "05-wph", ]
        sensor_type = "Water PH"
        lower_bound = 0.00
        upper_bound = 14.00
        value = round(random.uniform(lower_bound, upper_bound), 2)
        return dict(
            uid=str(uuid.uuid4()),
            timestamp=datetime.datetime.now().isoformat(),
            location=random.choice(self.locations),
            sensor_type=sensor_type,
            sensor_id=random.choice(sensor_ids),
            value=value,
            ratio=0,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            trigger_alert="Alkaline(Unsafe)" if value < 6 else "Acidic(Unsafe)" if value > 8 else "Neutral(Safe)",
        )

    def _rainfall_level(self):
        sensor_ids = ["01-rfl", "02-rfl", "03-rfl", "04-rfl", "05-rfl", ]
        sensor_type = "Rainfall Level"
        lower_bound = 2.00
        upper_bound = 10.00
        value = round(random.uniform(lower_bound, upper_bound), 2)
        return dict(
            uid=str(uuid.uuid4()),
            timestamp=datetime.datetime.now().isoformat(),
            location=random.choice(self.locations),
            sensor_type=sensor_type,
            sensor_id=random.choice(sensor_ids),
            value=value,
            ratio=0,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            trigger_alert="Slight Shower" if value < 5 else "Heavy Shower" if value > 10 else "Moderate Shower",
        )

    def _river_level(self):
        sensor_ids = ["01-rv", "02-rv", "03-rv", "04-rv", "05-rv", ]
        sensor_type = "River Level"
        lower_bound = 1.00
        upper_bound = 20.00
        value = round(random.uniform(lower_bound, upper_bound), 2)
        return dict(
            uid=str(uuid.uuid4()),
            timestamp=datetime.datetime.now().isoformat(),
            location=random.choice(self.locations),
            sensor_type=sensor_type,
            sensor_id=random.choice(sensor_ids),
            value=value,
            ratio=0,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            trigger_alert="Low" if value < 5 else "High" if value > 10 else "Normal",
        )
 
    def _water_Turbidity(self):
        sensor_ids = ["01-wt", "02-wt", "03-wt", "04-wt", "05-wt", ]
        sensor_type = "Water Turbidity"
        lower_bound = 0.00
        upper_bound = 14.00
        value = round(random.uniform(lower_bound, upper_bound), 2)
        return dict(
            uid=str(uuid.uuid4()),
            timestamp=datetime.datetime.now().isoformat(),
            location=random.choice(self.locations),
            sensor_type=sensor_type,
            sensor_id=random.choice(sensor_ids),
            value=value,
            ratio=0,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            trigger_alert="Safe" if value < 5 else "Unsafe",
        )

    def randomise(self):
        func_signatures = ["_water_ph", "_rainfall_level", "_river_level", "_water_Turbidity"]
        options = {"_water_ph": self._water_ph,
                   "_rainfall_level": self._rainfall_level, 
                   "_river_level": self._river_level,
                   "_water_Turbidity": self._water_Turbidity}
        return options[random.choice(func_signatures)]()

    def run_test(self):
        """
        test mock sensors return the correct data type
        """

        assert isinstance(self._water_ph(), dict)
        print("** PASSED - Water PH sensor data is of the right type **")

        assert isinstance(self._rainfall_level(), dict)
        print("** PASSED - Rainfall Level sensor data is of the right type **")

        assert isinstance(self._river_level(), dict)
        print("** PASSED - River Level sensor data is of the right type **")


class SimpleServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        query_dict = parse_qs(urlparse(self.path).query)
        sensor_type = query_dict.get("sensor_type", None)
        if sensor_type[0] == "all":
            self._set_headers()
            self.wfile.write(json.dumps(
                DataGenerator().randomise()).encode('utf-8'))
        else:
            pass

    def do_POST(self):
        if self.headers.get('content-type') == 'application/json':
            length = int(self.headers.get('content-length'))
            data = json.loads((self.rfile.read(length) or {}).decode('utf-8'))
            # do something with the data
            print(data)
            self._set_headers()
            self.wfile.write(json.dumps({"msg": "ok"}).encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            return


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        DataGenerator().run_test()
    else:
        print("** Server started http://%s:%s **" % (HOST, PORT))
        simple_server = HTTPServer((HOST, PORT), SimpleServer)
        try:
            simple_server.serve_forever()
        except KeyboardInterrupt:
            simple_server.shutdown()
