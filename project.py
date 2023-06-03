import binascii
from dilithium import Dilithium3
from pymongo import MongoClient

def main():
    # Connect to MongoDB
    
    account = input()
    CONNECTION_STRING = "mongodb+srv://DuuuKieee:899767147@loginserver.hqnkiia.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    dbname = "CryptoProject"
    db = client[dbname]
    signature_collection = db["SignatureCollection"]
    if(account == "admin"):
        PublisherPermission(signature_collection)
    else:
        RecepientPermission(signature_collection)

    # Generate keys
def PublisherPermission(collection):
    try:
        pk, sk = Dilithium3.keygen()
        # Load PDF file to sign
        print("Nhap duong dan")
        path =input()
    
        with open(path, "rb") as file:
            pdf_file = file.read()
        sig = Dilithium3.sign(sk, pdf_file)
        sig_hex = binascii.hexlify(sig).decode('utf-8')
        collection.insert_one({
        "signature": sig_hex,
        "public_key": binascii.hexlify(pk).decode('utf-8')
    })
    except:
        print("Duong dan khong hop le")

    #     # Upload signature to MongoDB

def RecepientPermission(collection):
    path = input()
    flag = 0
    try:
        for document in collection.find():
            signature = binascii.unhexlify(document["signature"])
            public_key = binascii.unhexlify(document["public_key"])
            with open(path, "rb") as file:
                pdf_file = file.read()
            verify = Dilithium3.verify(public_key, pdf_file, signature)
            if(verify == True):
                print(f"Verification result for signature {document['_id']}: {verify}")
                flag = 0
                break
            else:
                flag+=1
        if(flag != 0):
            print("false")
        

             
    except:
        print("File khong hop le")

if __name__ == "__main__":
    main()