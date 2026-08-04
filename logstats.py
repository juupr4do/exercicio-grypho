import argparse
import re
import sys
from collections import Counter
import statistics

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] ' +
    r'"(?P<request>[^"]*)" (?P<status>\d{3}) (?P<size>\S+)' +
    r'(?: (?P<response_time>\d+\.\d+))?'
)

def ler_terminal():
    organizer = argparse.ArgumentParser()
    _ = organizer.add_argument("logfile")
    return organizer.parse_args()

def abrir_log(log):
    if log == "-":
        return sys.stdin
    try:
        return open(log, "r", encoding="utf-8", errors="replace")
    except FileNotFoundError:
        sys.exit(f"Erro: arquivo '{log}' não encontrado.")

def main():
    args = ler_terminal()

    processadas = 0
    descartadas = 0
    doisXX = 0
    tresXX = 0
    quatroXX = 0
    cincoXX = 0
    endpoints = Counter()
    tempoResposta = []

    arquivo = abrir_log(args.logfile)
    with arquivo:
        for linha in arquivo:
            linha = linha.rstrip("\n")
            match = LOG_PATTERN.match(linha)
            if match is None:
                descartadas += 1
            else:
                processadas += 1
                status = match.group("status")
                request = match.group("request")
                tempo = match.group("response_time")

                metodo, endpoint, protocolo = request.split()
                endpoints[endpoint] += 1
                top5 = endpoints.most_common(5)

                if tempo:
                    tempoResposta.append(float(tempo))

                if status[0] == '2':
                    doisXX += 1
                if status[0] == '3':
                    tresXX += 1
                if status[0] == '4':
                    quatroXX += 1
                if status[0] == '5':
                    cincoXX += 1

            continue

    tempoResposta.sort(reverse=True)
    top5Time = tempoResposta[:5]

    if tempoResposta:
        p95 = statistics.quantiles(
            tempoResposta,
            n=100
        )[94]
    else:
        p95 = 0

    print(f"Processadas: {processadas}")
    print(f"Descartadas: {descartadas}")
    print(f"Top 5 endpoints acessados: {top5}")
    print(f"Top 5 tempo de acesso: {top5Time}")
    print(f"p95: {p95:.3f} segundos")
    print(f"2xx: {doisXX}")
    print(f"3xx: {tresXX}")
    print(f"4xx: {quatroXX}")
    print(f"5xx: {cincoXX}")

main()
