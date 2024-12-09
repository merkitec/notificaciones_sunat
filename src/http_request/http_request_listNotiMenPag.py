import requests

url = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/listNotiMenPag?tipoMsj=2&codCarpeta=00&codEtiqueta=&page=1&des_asunto=&codMensaje=&tipoOrden=NADA&_=1732426840217"

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
  'Cookie': 'f5_cspm=1234; f5avraaaaaaaaaaaaaaaa_session_=EKBMEDNDJNNDLFMNKKDAMPINBNNPEIHLJEFICLJDGBLOLKCBEFNFONBPBELINJCMIGPDLAIEMPGONMIDCCBAPKJBDKDKPDLCIMMLHFOOGJMCDPEENFJLDLKEPGNNAPEI; 20606208414ALLODANS=1; -798847265=1; IAGENDOCSESSION=V6DFn2xBQx4Cqx0DmwT3FDjgnsFb6J84y0DhL8pFh9Ghf5VTFHx47nFltnC2mp1HtWd25cKSvhvk90c0vMTqzbBNLSJpWDTL2pVbH5nb0ZSsfLl6kDVhQXlgKmh5Rn484vprhptTdvmnvyLpW9dSnvjYpTCCQ2pfM2QqYvvDhV9d5z1yG1vLfRj2y3xMTyhLvy00BTPQ4vFxF2cynQ82xjq8bxyz2cLQskmRgKT68g2vKDw16vyJGNcQfPlLNwPY!679627393!206439389; ITVISORNOTISESSION=pMX6n2wpyyzTmyqGh7sJvN05Qym2g0tRZWnjzKSQjQB5DvMhX29f!738795427; TS0111bf25=019edc9eb88a72ad1437debd9bc5c71c9074501839753719bb8682ebb46faac8a14378634057773f5bc8aee73cfc285236cef7d3f32d13eeb257f335988cc023a21a4eeb12; TS011cfddf=014dc399cbe0ac72f618cec8be2c596617cc36f9ea7a6fd5316c50cea50cef779d1257b5b8a0af26f09da1023780abf331ef48cc36e3e05b74fd21bde9bf902361fd04e6c3ce03cd800b3201557ae6bfcdd01fd7344c4dc46ac6aca37fabfe02b89b8597193eb9a459cd6f626a82b2baea409a826b94604acabef45f42423f8cb34fd3fc48f3844b2fdbdca0cb92f4a056277273f287d7497d83f82fc343e3039363e1fac7c31c4cead77c2d0d6e7a45542e5dfddfa5b2cb478aeea3768619fdf654942c7fa24bb53c46767f8d96deedf00307c11d; TS3281c147027=08d0cd49b8ab2000b27437adbfa03b85c958bf1ca13effaef6bc395df911e233113a7259a5ce1f9f088b45fbf8113000bfde36ccfbf0dbfea9ead1defea69c4b7966f91dcdb1d946ce43bd81d54f301927d25ff0559b93085120464105495bd9; TS44788fc0027=08fe7428c8ab2000179c80daccbcff998b4cf8c35bf0ed0da461335d3f35e4b5e6f516c8903d880808335668791130007ee331eebdf2843eae4129d1c856fda227abcae6ea7c869b31c996d185681452aec29cd01f8765b3c569c278c841da5d; TSf806e172027=08fe7428c8ab2000ad5f27272271cf64a20242964e31fa24574069b7c8f76bda44c8a7a36ef976a408c20dd063113000711bbc788f1ae169d2cc62d8014380bac4bf26ad85b5797e6b47835ebfe3678b687dac184f4aac24a37328e29519a274; f5avr1255429519aaaaaaaaaaaaaaaa_cspm_=LLMBJGAMDAJPFELPNNEJDPMBFBMDBFBAKMJNHINDPHDBMEPLGJHDLOBHEMJLBLGPLLBCBPFHABNNCALIKLDALDPAAIJCFJDMOADIJNNLOBFKFEJNLLHIHFDENPPPKGAC'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

