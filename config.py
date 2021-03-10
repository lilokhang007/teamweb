BASE_URL = 'https://175.159.162.12:8002/'

def make_API(base):
	return {
		'admin': base + 'admin/'
    }
    
API = make_API(BASE_URL)
