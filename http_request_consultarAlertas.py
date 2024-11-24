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
# url = " https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm"
url = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/consultarAlertas"

headers = {
  'sec-ch-ua-platform': '"Windows"',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'X-Ruc': '20606208414',
  'sec-ch-ua-mobile': '?0',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'ww1.sunat.gob.pe',
  'Cookie': 'f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=ODJGFPBFKDFEFLBHEMFDAHJAGIFALCLLCPBFMLOEGDKDEGEJBCHKJDAIAFLNBAFMMACDINODODFCBLOGOGKALCHCEMGALBFHIOGEJFIPIDCNJHPFAILKMMCMBOKCOPIG; 20606208414ALLODANS=1; -798847265=1; IAGENDOCSESSION=yFnLnC8Gfv22gXcg2HL1ynT285Lx2QmWqC7LHh2Xph2yG2hTG1vJBt8RTpsYGRl0sGJ7lN7hQhbFyZj1qpFfzBBGJnqHhbXDdlS3m89rbGnWX1zJ1LVvlvnXczLy3k5CwvgxcnZ28L1R7GrypwnJH9GMDFW54M70f6KLgynGyCHQTGj0Sx7TMgwhHZhLDNhtGWGgTcdwPx9HGCQ23SlxHCq2xPMRLfYL3LHyvPNd1v9SLXCMmLF1yLRsNNF9z1Q7!-1225643374!2088701503; ITVISORNOTISESSION=1y1wnC8BQ8YNQrZ7pQ1dQMCZxLTzQvP3vGJxnyFnyJQvnxtghW0L!2036653299; TS011cfddf=014dc399cb3226a8e4697b5ede21a7fb703aca43cfb51aeb019625084362c54861c2d920600bfe30192ed90b01ad422ffa471f04280ad8ec65aeecf22def9d25dbd82630ec32ce4dc60a05277a28c727613f10b6a1f2ea6949f4b53ea03cb87e5c927d90721619bcf2d97909aa013cd154da669b3eaafa95e7bb40adc8142b4f074852338ac5771373a8041f23161b4ef4e0a95fbd76a65421948989b13eda403d157dc3f6c0cc11a56c39bad31f3c5975323cca0539f09771b354bc8d4144538173784647; TS44788fc0027=08fe7428c8ab2000c3a1bdfe4a4b85eaf66b35a204886661d7c3e143054c3054d5e505bbb3bdbd8308ba51897c1130007735775eb4c794f1b3e91667a3373a134184e63a67508ec4aa2e72b0af26a41ecc5fe888c08609109e4e4b37debfd060; f5avr1255429519aaaaaaaaaaaaaaaa_cspm_=LLMBJGAMDAJPFELPNNEJDPMBFBMDBFBAKMJNHINDPHDBMEPLGJHDLOBHEMJLBLGPLLBCBPFHABNNCALIKLDALDPAAIJCFJDMOADIJNNLOBFKFEJNLLHIHFDENPPPKGAC'
}
# cookies = {
#     "session_id": "your_session_id",
#     "user_id": "your_user_id"
# }
payload = {}

# Make a POST request
response = make_http_request("POST", url, headers=headers, data=payload)

# Make a GET request
# response = make_http_request("GET", url, headers=headers)       #, cookies=cookies)

# print(post_response.text)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")


