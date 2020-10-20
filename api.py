import pyrebase

config = {
	"apiKey": "AIzaSyASHWZlbiSDASdHpFNL7BLVDQs9weuKj08",
	"authDomain": "neocities-ef933.firebaseapp.com",
	"databaseURL": "https://neocities-ef933.firebaseio.com",
	"projectId": "neocities-ef933",
	"storageBucket": "neocities-ef933.appspot.com",
	"messagingSenderId": "533267279223",
	"appId": "1:533267279223:web:3a194ac03787d5e4"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def stream_handler(message):
    a = db.child("test").get()
    print(a.val())

db.child("test").stream(stream_handler)

db.child("test").update({"briefings": "test10"})


