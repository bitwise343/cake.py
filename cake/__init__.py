import json


try:
    with open('./cake/config/keys.json', 'r') as f:
        my_keys = json.load(f)
        assert "PRIVATE" in my_keys.keys()
        assert "PUBLIC" in my_keys.keys()
        assert my_keys["PRIVATE"] != ""
        assert my_keys["PUBLIC"] != ""
except:
    from cake.keygen import create_key_pair
    private, public = create_key_pair()
    my_keys = { "PRIVATE": private, "PUBLIC": public }
    with open('./cake/config/keys.json', 'w+') as f:
        json.dump(my_keys, f, index=4)

try:
    with open('./cake/config/infura.json', 'r') as f:
        infura = json.load(f)
        my_keys["INFURA"]=infura["INFURA"]
except:
    print("An infura ID is needed to connect to the blockchain.")
    exit()

