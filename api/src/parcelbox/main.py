from fastapi import FastAPI
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import os
import random

FLAG = os.getenv("FLAG")
assert FLAG

app = FastAPI()

while 1:
    p = getPrime(128)
    q = getPrime(128)
    n = p * q
    if q != p and len(bin(n)) - 2 >= 256:
        break

e = 2 ** 16 + 1

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

print(p, q, d, n, e)

# 3 boxes, 2 columns and 6 rows
package_count = 3 * 2 * 6
package_store: list[str] = [
    "Aldri for sent å snu",
    "Bare bok gjør ingen klok",
    "Bedre sent enn aldri",
    "Den beste tiden å plante et tre er for 20 år siden, den nest beste tiden er nå",
    "Den som gir seg, har tapt på forhånd",
    "Den som ikke tar prøven, kommer til å feile",
    "Den som ler sist, ler best",
    "Den som spør, forblir dum i fem minutter. Den som ikke spør, forblir dum resten av livet",
    "Den som venter på noe godt, venter ikke forgjeves: " + FLAG,
    "Det er aldri så galt at det ikke er godt for noe",
    "Det er bedre å gå på isen enn i vannet",
    "Det er bedre å tenne lys enn å forbanne mørket",
    "Det er bedre å være den katten som går for seg sjøl enn den som stoler blindt på andre",
    "Det finnes ikke dårlig vær, bare dårlige klær",
    "Det finnes ingen snarveier til steder det er verdt å reise til",
    "Det kunne vært verre",
    "Det spiller ingen rolle hvor sakte du går så lenge du ikke stopper",
    "Du kan aldri krysse havet før du har motet til å miste synet av kysten",
    "En fjær blir lett til fem høns",
    "En fugl i hånden er bedre enn ti på taket",
    "Eplet faller ikke langt fra stammen",
    "Gammel vane er vond å vende",
    "Ingen fisk uten bein",
    "Ingen roser uten torner",
    "Lykke er ikke noe som allerede eksisterer. Den skapes av dine egne handlinger",
    "Man skal ikke skue hunden på hårene",
    "Mange kokker, mye søl",
    "Morgenstund har gull i munn",
    "Når katten er borte, danser musene på bordet",
    "Ser ikke skogen for bare trær",
    "Smi mens jernet er varmt",
    "Smuler er også brød",
    "Ut på tur, aldri sur",
    "Uten mat og drikke duger helten ikke",
    "Vær selv den forandring du ønsker å se i verden",
    "Øvelse gjør mester",
]
random.shuffle(package_store)
assert len(package_store) == package_count


def as_message(id: int, nonce: int):
    id_bytes = f"{id:02d}".encode("utf-8")
    separator = b"."
    nonce_bytes = long_to_bytes(nonce)

    message = b"".join([id_bytes, separator, nonce_bytes])
    return bytes_to_long(message)


def verify(id: int, nonce: int, sig: int) -> bool:
    expected_message = as_message(id, nonce)
    actual_message = pow(sig, e, n)
    print(long_to_bytes(expected_message), long_to_bytes(actual_message))
    return expected_message == actual_message


@app.get("/open/{id}")
def open_box(id: int, nonce: str, sig: str):
    signature_nonce = int(nonce, 16)
    signature = int(sig, 16)
    if verify(id, signature_nonce, signature):
        return {
            "id": id,
            "success": True,
            "content": package_store[id],
        }
    else:
        return {
            "id": id,
            "success": False,
            "content": "Signature verification failed",
        }


@app.get("/my_parcel")
def get_own_parcel():
    id = package_store.index("Aldri for sent å snu")
    assert id >= 0

    nonce = bytes_to_long(os.urandom(8))
    m = as_message(id, nonce)
    sig = pow(m, d, n)

    return {
        "id": id,
        "nonce": hex(nonce),
        "sig": hex(sig),
        "n": hex(n),
        "e": hex(e),
    }
