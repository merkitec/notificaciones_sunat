import requests

url = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/obtenerDetalleNotiMen?codigoMensaje=651871742&tipoMsj=2&_=1732426840218"

payload = {}
headers = {
  'sec-ch-ua-platform': '"Windows"',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'X-Ruc': '20606208414',
  'sec-ch-ua-mobile': '?0',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'ww1.sunat.gob.pe',
  'Cookie': 'f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=HPCIMHEHGCOPHEAMEJEKHEEHCMKKCPNEILOJMNLKEPJGAPAGJMKNKIKOEFIMDKBEKMFDMKDDJOAEGFNJDJCAPGGCGLJDDGNPOOHKLCEPBNFCNFONGEHBNCABIIOLDPDI; 20606208414ALLODANS=1; -798847265=1; IAGENDOCSESSION=V6DFn2xBQx4Cqx0DmwT3FDjgnsFb6J84y0DhL8pFh9Ghf5VTFHx47nFltnC2mp1HtWd25cKSvhvk90c0vMTqzbBNLSJpWDTL2pVbH5nb0ZSsfLl6kDVhQXlgKmh5Rn484vprhptTdvmnvyLpW9dSnvjYpTCCQ2pfM2QqYvvDhV9d5z1yG1vLfRj2y3xMTyhLvy00BTPQ4vFxF2cynQ82xjq8bxyz2cLQskmRgKT68g2vKDw16vyJGNcQfPlLNwPY!679627393!206439389; ITVISORNOTISESSION=0NJ3nCQLS6dlVzrdyQsltnKrFXwWfTPB4yLvrH13l98LncJC6zp0!2036653299; TS0111bf25=019edc9eb88a72ad1437debd9bc5c71c9074501839753719bb8682ebb46faac8a14378634057773f5bc8aee73cfc285236cef7d3f32d13eeb257f335988cc023a21a4eeb12; TS011cfddf=014dc399cb5ba3b0e7cc37b4e23974a0c55d77c67e6da7d6b681808ede84ad0d797da73d1d4a1c6b16b0cc72b5178055f867f0459c084b275ddeab6d0880edc0a09c2ec80f305720235ad61e1a870f2d1ce94b6adcaa93d142c71be71f880413f8af231b3be04dde86a29acdd5b45bca1f79c375d8b46bd0e34e8c0d456f5ba65deac1c1a7065af5b0cf464ac4ec2f65c532a177139f691266887258642c30addcb3a1bab11a306ab763824d4fbb14b9304f14550e5f5f57483ae9fdf16699b01b4d7e18d9113a6fd6710bced3dac5c75cdd92fb43; TS3281c147027=08d0cd49b8ab2000b27437adbfa03b85c958bf1ca13effaef6bc395df911e233113a7259a5ce1f9f088b45fbf8113000bfde36ccfbf0dbfea9ead1defea69c4b7966f91dcdb1d946ce43bd81d54f301927d25ff0559b93085120464105495bd9; TS44788fc0027=08fe7428c8ab20008fbe0b93c46a4a91d8e51ab657b7c5dd8e6ca44d54ab5d92ad578b5806ee57d708468e22931130007ba8dd31ba70f92f510da677a9c49e091c7cb39a5e29f4fe8ae5398ff3b8d4bf3af072ce5d143c229bdb01470302df13; TSf806e172027=08fe7428c8ab2000ad5f27272271cf64a20242964e31fa24574069b7c8f76bda44c8a7a36ef976a408c20dd063113000711bbc788f1ae169d2cc62d8014380bac4bf26ad85b5797e6b47835ebfe3678b687dac184f4aac24a37328e29519a274; f5avr1255429519aaaaaaaaaaaaaaaa_cspm_=LLMBJGAMDAJPFELPNNEJDPMBFBMDBFBAKMJNHINDPHDBMEPLGJHDLOBHEMJLBLGPLLBCBPFHABNNCALIKLDALDPAAIJCFJDMOADIJNNLOBFKFEJNLLHIHFDENPPPKGAC'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")


