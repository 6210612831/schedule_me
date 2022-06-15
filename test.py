from datetime import timedelta, datetime
# hr = 10
# min = 30
# day = {
#     "mo":0,
#     "tu":1,
#     "we":2,
#     "th":3,
#     "fr":4,
#     "sa":5,
#     "su":6
# }
day = "tu"

days = ["mo","tu","we","th","fr","sa","su"]
today_day = days[int(datetime.now().weekday())]
now = datetime.now()

# while True:
#     if days[int(now.weekday())] != day:
#         now = now + timedelta(days=1)
#     else:
#         break

input = now.replace(hour=12, minute=59)


print(now - timedelta(hours=14))