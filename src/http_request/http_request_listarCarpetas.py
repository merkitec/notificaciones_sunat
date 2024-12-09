import requests

def make_http_request(method, url, headers=None, cookies=None, data=None):
  """Makes an HTTP request with custom headers and cookies.

  Args:
    method: The HTTP method to use (e.g., 'GET', 'POST').
    url: The URL to send the request to.
    headers: A dictionary of custom headers to include in the request.
    cookies: A dictionary of custom cookies to include in the request.
    data: The data to send in the request body.

  Returns:
    The response object from the request.
  """

  if headers is None:
    headers = {}
  if cookies is None:
    cookies = {}

  response = requests.request(method, url, headers=headers, cookies=cookies, data=data)
  return response

# Example usage:
url = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/ajax/listarCarpetas?_=1732334128122"

headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'ww1.sunat.gob.pe',
  'X-Ruc': '20606208414',
  'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=KOGOIHBPLBFDOCFAGJFOFMOEMKGLMGDCEALKCHIAOALOCBLELJDOHKBCCBLGEFLNJLCDMOLFJBKNCFNGIPGAMEBFGDJDEIBIGFDPLLGHPPAJDDCLGENLIFADKAAPEOHK; f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=IPEGLOPHLIOEIPACDNKNHIMCAIMAMFNDBBHPEKIDJPHNNICHNMBBICKCCPJKGINCBAEDKKOHEBGFIHLBIHHAAIGFMCCJMLEHOGOALOKLJPLPJOEKPNCBIHKDONEBPBOE; 20606208414ALLODANS=1; 736667984=1; IAGENDOCSESSION=tJlnnCqNhFJxty2qFGdTHTdkR2JDmPXGtBCPp4C16T0Ghpfj1wp43kGgyn57F62HHsDZGQyPTT0573VFQLbngvSm45Jpg7ywcvJvnV1pxBgb4qLYbp94JpqxWJ9czbvwNmJ1KcpBs6QywTNK4PxgjYWRnSr1LLLm87BYhh1CrDVhtTdhJpD4nMh4qhzF7B11PpQgvmHyK7wWJw7vTyn4rV0PdXTpT784D76pFhGKKndnL12TGnF3Tjz2t6L3Gn1l!954996765!-809039695; ITVISORNOTISESSION=VV0YnCqM2tyhhgbQxTxpDQPl4pwx2ppmpTh0WJGFLhwQlvWG1TwJ!58356844; TS011cfddf=014dc399cba057d9a6e4898e7a4b8a07f8a582ee72d652e52b76f4459b4bc96506261996c6d3658d647dee3c673fe738ab772514a6806386b66f65ba2cb7d079d6706bebbe0b366c0116893888e3a4a1befb9ccb1745b6af573b7d0f330c3367eae44a54d4620f0d295438640916024c221acbc166b903e28c2ad106fe505a0fa76167d7943ff8129ca838eea29efe9f49940c99534783e0c1bc21f123f86c476aec544c1880abbfa8e83b6fb68014f88475e58b0a3e3508b54faf0767d192e5a7580cc456b45c4bda3c58c822d9478130219a60c85db7a928639a047a4cad915352c4e190; TSf806e172027=08fe7428c8ab20003a79c954aaed869c98cb0119abbd51fed869f212566d27d59e5e4f97999432ef08cdf245f51130002ea393226cc0c4f4896200d67b23699294a123c7f909d213fec4a8e1e73d4a999627fa14b74ebcb41a6e0ca239403ebd; f5avr1255429519aaaaaaaaaaaaaaaa_cspm_=HLFPPKCFIFILLBMOGKKHGPOGOCLGFHFILPGBEEANMCLKCNEMAHNMEGIGCILKCIJIMJFCELNDAPFLAAJFBDJADNPNADJJMHCMLJMLEMIDHFGJCKHAEDGPPOCDJMOLFHGD'
}
payload = {}

# Make a GET request
response = make_http_request("GET", url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

