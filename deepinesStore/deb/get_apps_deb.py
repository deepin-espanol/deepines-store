import re
from bs4 import BeautifulSoup
from deepinesStore.core import get_deepines_uri, get_dl

#		 Obtener URL del repositorio		  #
def Get_Repo_Url():

    # TODO: Update for Deepines 5 when 23 gets released
    fallback_url = get_deepines_uri("/4/paquetes.html")
    repo_file = "/etc/apt/sources.list.d/deepines.list"
    try:
        repo_text = open(repo_file).read()
        url = re.search(
            "(?P<url>https?://[^\s]+)", repo_text).group("url") + "paquetes.html"
        return url
    except:
        return fallback_url

def fetch_list_app_deb(lista_excluir):
		# Asignamos la url
		repo_url = Get_Repo_Url()
		try:
			# Realizamos la petición a la web
			req = get_dl(repo_url, timeout=10)
			# Comprobamos que la petición nos devuelve un Status Code = 200
			status_code = req.status_code
			if status_code == 200:
				# Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
				html = BeautifulSoup(req.text, "html.parser")
				# Obtenemos todos los divs donde están las entradas
				entradas = html.find_all('tr')
				lista = list()
				# Recorremos todas las entradas para extraer el título, autor y fecha
				for i, entrada in enumerate(entradas):
					# Con el método "getText()" no nos devuelve el HTML
					titulo = entrada.find('td', {'class': 'package'}).getText()
					descripcion = entrada.find(
						'td', {'class': 'description'}).getText()
					version = entrada.find(
						'td', {'class': 'version'}).getText()
					categoria = entrada.find(
						'td', {'class': 'section'}).getText()
					estado = 1
					if titulo not in lista_excluir:
						lista_origen = [titulo, descripcion,
										version, categoria, estado]
						lista.append(lista_origen)
		
				return lista
		except Exception as e:
			print("Error fetching apps:", e)
			return []