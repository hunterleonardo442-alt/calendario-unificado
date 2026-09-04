import requests
from icalendar import Calendar

ICS_1 = "https://outlook.office365.com/owa/calendar/4a94761ff57440059ae345ba69196477@agterceiro.com.br/e0a04b7c93844ecfad6ab41c1cc0ac8a9280095936509598362/calendar.ics"

ICS_2 = "https://outlook.office365.com/owa/calendar/4a94761ff57440059ae345ba69196477@agterceiro.com.br/299f8d5fdb2f41da86d0ef119099167b18164811314386770884/calendar.ics"

resultado = Calendar()
resultado.add("prodid", "-//Calendario Unificado//")
resultado.add("version", "2.0")

eventos = set()
timezones = set()

for url in [ICS_1, ICS_2]:

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    calendario = Calendar.from_ical(response.content)

    # Preserva os fusos horários
    for item in calendario.walk():

        if item.name == "VTIMEZONE":

            tzid = str(item.get("TZID", ""))

            if tzid not in timezones:
                timezones.add(tzid)
                resultado.add_component(item)

    # Copia os eventos sem duplicar
    for item in calendario.walk():

        if item.name != "VEVENT":
            continue

        uid = str(item.get("UID", ""))
        recurrence = str(item.get("RECURRENCE-ID", ""))

        chave = f"{uid}|{recurrence}"

        if chave in eventos:
            continue

        eventos.add(chave)

        resultado.add_component(item)

with open("calendario_unificado.ics", "wb") as arquivo:
    arquivo.write(resultado.to_ical())

print(f"{len(eventos)} eventos exportados")
