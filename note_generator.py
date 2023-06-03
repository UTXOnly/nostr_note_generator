import secp256k1
import hashlib
import json
import random
import time
import websocket

# Define the first keypair
public_key1 = "d576043ce19fa2cb684de60ffb8fe529e420a1411b96b6788f11cb0442252eea"
private_key_hex1 = "96f339c05410721070695040a410186de4fdd67714b1e466b97d1aa433707ef6"

# Define the second keypair
public_key2 = "b97b26c3ec44390727b5800598a9de42b222ae7b5402abcf13d2ae8f386e4e0c"
private_key_hex2 = "310cc8246a8bf8d2c9945f255d72272b8d30f86c1e7abac2ad812cb1f1e5a617"


def print_color(text, color):
    print(f"\033[1;{color}m{text}\033[0m")


random_dict = {
    0: 'Все ваши базы принадлежат нам.😏🏴‍☠️',
    1: '😏🏴‍☠️Я в вашей базе и убиваю ваших друзей.',
    2: '😏🏴‍☠️Noob-тубинг для скрабов. https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    3: 'Pwned!😏🏴‍☠️',
    4: 'gg 😏🏴‍☠️no re',
    5: 'Мне нужно лечение!',
    6: 'AFK 😏🏴‍☠️BRB',
    7: 'Haxor skillz https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    8: 'Меня 😏🏴‍☠️только что убили.',
    9: 'Группировка нападает! https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    10: 'Я перехожу в полный режим «try-hard».',
    11: 'Лаг меня 😏🏴‍☠️убивает!',
    12: 'Я использую дымовую завесу!',
    13: 'Nerf this!',
    14: 'Я кемперю спавн.',
    15: 'Ты сердишься, бро?',
    16: 'Я иду на всю катушку!',
    17: 'Я притягиваю 😏🏴‍☠️агрессию! https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    18: 'Я фармлю золото.',
    19: 'Меня ганкуют! https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    20: 'Я создаю нового персонажа.',
    21: 'Я 😏🏴‍☠️опускаю молоток!',
    22: 'Я использую ульт!',
    23: 'Я приманиваю их.https://nostr.build/av/b91c8fa002ef84356d693c928b6952e962c4c51e5b52142998f816cc20ecfc34.mp4',
    24: 'Я становлюсь 😏🏴‍☠️предателем!',
}

relays = [
    "wss://nostpy.lol",
    "wss://offchain.pub",
    "wss://nos.lol",
    "wss://relay.snort.social",
    "wss://nostr.wine",
    "wss://puravida.nostr.land",
    "wss://nostr.bitcoiner.social",
    "wss://relay.damus.io"]


def get_random_key(dictionary):

    random_key = random.choice(list(dictionary.keys()))
    random_value = dictionary[random_key]
    return random_value

def sign_event_id(event_id: str, private_key_hex: str) -> str:
    private_key = secp256k1.PrivateKey(bytes.fromhex(private_key_hex))
    sig = private_key.schnorr_sign(bytes.fromhex(event_id), bip340tag=None, raw=True)
    return sig.hex()

def calc_event_id(
    public_key: str, created_at: int, kind_number: int, tags: list, content: str
) -> str:
    data = [0, public_key, created_at, kind_number, tags, content]
    data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(data_str.encode("UTF-8")).hexdigest()

def create_event(public_key, private_key_hex):
    # Create a list of tags for the event
    tags = []

    words = ["nostr", "so nice", "bless up", "send it", "working?", "the egg", "nip1 FTW", "chillllll", "sooo nice", "eggg", "\U0001F993", "\U0001F596", "\U0001F60F",
         "yolo", "cool beans", "hakuna matata", "let's go", "stay woke", "the bird", "biggie smalls", "Zen mode", "so fresh", "to infinity and beyond", "\U0001F981", "\U0001F4AA", "\U0001F92C",
         "all good", "go with the flow", "shine on", "you got this", "grind time", "the nest", "GOAT status", "just breathe", "vibing out", "sunny side up", "\U0001F423", "\U0001F3B5", "\U0001F64F",
         "mind over matter", "good vibes only", "rise up", "never give up", "hustle & flow", "bird brain", "OG status", "live laugh love", "feeling blessed", "egg-cellent adventure", "\U0001F986", "\U0001F525", "\U0001F601"]


    #random_sentence = " ".join([random.choice(words) for i in range(random.randint(3, 6))]).capitalize()

    created_at = int(time.time())

    # Calculate the event ID using calc_event_id function
    kind_number = 1
    #content = random_sentence
    content = get_random_key(random_dict)
    event_id = calc_event_id(public_key, created_at, kind_number, tags, content)

    # Sign the event ID using sign_event_id function
    signature_hex = sign_event_id(event_id, private_key_hex)

    # Create the event dictionary with all required fields including id and sig
    event_data = {
        "id": event_id,
        "pubkey": public_key,
        "kind": kind_number,
        "created_at": created_at,
        "tags": tags,
        "content": content,
        "sig": signature_hex,
    }

    return event_data


def verify_signature(event_id: str, pubkey: str, sig: str) -> bool:
    try:
        pub_key = secp256k1.PublicKey(bytes.fromhex("02" + pubkey), True)
        result = pub_key.schnorr_verify(bytes.fromhex(event_id), bytes.fromhex(sig), None, raw=True)
        if result:
            print_color(f"Verification successful for event: \033[0m{event_id}\033[0m", 32) 
        else:
            print_color(f"Verification failed for event {event_id}", 31) 
        return result
    except (ValueError, TypeError, secp256k1.Error) as e:
        print_color(f"Error verifying signature for event {event_id}: {e}", 31) 
        return False


def send_event(ws, public_key, private_key_hex):

    for i in range(2):
        # Create a new event
        event_data = create_event(public_key, private_key_hex)
        sig = event_data.get("sig")
        id = event_data.get("id")

        # Verify the event signature
        signature_valid = verify_signature(id, public_key, sig)

        if signature_valid:
            # Serialize the event data to JSON format
            event_json = json.dumps(("EVENT", event_data))

            # Send the event over the WebSocket connection
            ws.send(event_json)
            print_color(f"Event sent:\033[0m{event_json}\033[0m", 31)
        else:
            print_color("Invalid signature, event not sent.", 31)


while True:
    for relay in relays:
        try:
            ws_relay = websocket.create_connection(relay)
            send_event(ws_relay, public_key1, private_key_hex1)  # Use the first keypair
            send_event(ws_relay, public_key2, private_key_hex2)  # Use the second keypair
            ws_relay.close()
        except Exception as e:
            print(f"Error connecting to {relay}: {e}")
            continue

    time.sleep(10)
