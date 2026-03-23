from datetime import datetime
from zoneinfo import ZoneInfo

bruxelas = ZoneInfo("Europe/Brussels")
nova_york = ZoneInfo("America/New_York")
tokyo = ZoneInfo("Japan")
manaus = ZoneInfo("America/Manaus")
brasilia = ZoneInfo("Brazil/East")
rio_branco = ZoneInfo("America/Rio_Branco")
agora = datetime.now()
fmt = "%d/%m/%Y às %H:%M"

print("Agora em: ")

base_offset = 0.0
offset_obj = agora.astimezone(brasilia).utcoffset()

if offset_obj is not None:
    base_offset = offset_obj.total_seconds() / 3600

print(f"{'CIDADE':<15} | {'DATA E HORA':<20}| {'!= BRASÍLIA'}")
print("_" * 55)

for cidade_nome, zona in [
    ("Bruxelas", bruxelas),
    ("New_York", nova_york),
    ("Tokyo", tokyo),
    ("Manaus", manaus),
    ("Brasília", brasilia),
    ("Rio Branco", rio_branco),
]:
    horario_cidade = agora.astimezone(zona)

    cidade_offset_obj = horario_cidade.utcoffset()

    if cidade_offset_obj is not None:
        cidade_offset = cidade_offset_obj.total_seconds() / 3600
        diferenca = cidade_offset - base_offset

        sinal = "+" if diferenca >= 0 else ""

        print(
            f"{cidade_nome:<15} | {horario_cidade.strftime(fmt)} | {sinal}{diferenca:g}h"
        )
