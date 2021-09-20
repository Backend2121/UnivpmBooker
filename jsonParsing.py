import json
import os

class jsonParsing():
    def run(self):
        if not os.path.isfile("cache.json"):
            with open("cache.json", "w") as f:
                f.write('{"booked": []}')
                f.close()

        # Json loading
        with open("lessons.json", "r") as f:
            lessons = json.loads(f.read())
            f.close()

        # Cache file preparation
        cache = json.loads(open("cache.json", "r").read())

        # Json scraping
        new_lectures = []
        for day in lessons:
            for lecture in day["prenotazioni"]:
                if not lecture["prenotata"]:
                    if lecture["entry_id"] not in cache["booked"]:
                        # Book it
                        print("Adding " + str(lecture["nome"]))
                        cache["booked"].append(lecture["entry_id"])
                        new_lectures.append(lecture["entry_id"])

        with open("cache.json", "w") as f:
            json.dump(cache, f)
            f.close()
        return new_lectures