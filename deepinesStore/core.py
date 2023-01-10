from os.path import join, abspath, dirname

def get_res(res_name, dir='resources', ext='.svg'):
	return abspath(join(dirname(__file__), dir, res_name + ext))

def get_dl(uri, params=None, **kwargs):
	from requests import get
	try:
		return get(uri, params=params, **kwargs)
	except Exception as e:
		print(f"DL ERROR: {type(e).__name__}, URI: {uri}")
		class DummyResponse:
			status_code = None
			content = b""
			text = "" # FIXME: Use some kind of fallback for this, a text file maybe?
		return DummyResponse()