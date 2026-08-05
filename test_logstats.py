from logstats import LOG_PATTERN, abrir_log


def teste_linha_formatada():
    linha = '10.0.0.0 - - [04/Aug/2026:20:57:32 +0000] "GET /teste HTTP/1.1" 200 1043 0.040'
    match = LOG_PATTERN.match(linha)

    assert match is not None
    assert match.group("ip") == "10.0.0.0"
    assert match.group("timestamp") == "04/Aug/2026:20:57:32 +0000"
    assert match.group("request") == "GET /teste HTTP/1.1"
    assert match.group("status") == "200"
    assert match.group("size") == "1043"
    assert match.group("response_time") == "0.040"

def teste_linha_corrompida():
    linha = "linha corrompida"
    match = LOG_PATTERN.match(linha)

    assert match is None

def teste_abrir_log():
    doc = abrir_log("teste")
    conteudo = doc.read()
    doc.close()

    assert conteudo == "teste\n"

if __name__ == "__main__":

    testes = [
        test_linha_formatada,
        test_linha_corrompida,
        test_abrir_log
    ]

    falhas = 0
    for teste in testes:
        try:
            teste()
            print(f"Passou     - {teste.__name__}")
        except AssertionError as erro:
            falhas += 1
            print(f"Não passou - {teste.__name__}: {erro}")

    print()
    if falhas == 0:
        print(f"Todos os {len(testes)} testes passaram!")
    else:
        print(f"{falhas} de {len(testes)} testes falharam.")
