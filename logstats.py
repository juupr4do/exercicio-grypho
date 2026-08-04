import argparse
import re
import sys

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
                print(status)
                if status[0] == '2':
                    doisXX += 1
                if status[0] == '3':
                    tresXX += 1
                if status[0] == '4':
                    quatroXX += 1
                if status[0] == '5':
                    cincoXX += 1

            continue

    print(f"Processadas: {processadas}")
    print(f"Descartadas: {descartadas}")
    print(f"2xx: {doisXX}")
    print(f"3xx: {tresXX}")
    print(f"4xx: {quatroXX}")
    print(f"5xx: {cincoXX}")

main()
