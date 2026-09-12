import requests


def obtener_tasa_bcv():
    try:
        url = "https://ve.dolarapi.com/v1/dolares"
        r = requests.get(url, timeout=5)
        data = r.json()

        for item in data:
            if item.get("fuente") == "oficial" and item.get("promedio"):
                return float(item["promedio"])

        return 0.0

    except Exception as e:
        print("Error BCV:", e)
        return 0.0


def obtener_tasa_paralelo():
    try:
        url = "https://ve.dolarapi.com/v1/dolares"
        r = requests.get(url, timeout=5)
        data = r.json()

        for item in data:
            if item.get("fuente") == "paralelo" and item.get("promedio"):
                return float(item["promedio"])

        return 0.0

    except Exception as e:
        print("Error paralelo:", e)
        return 0.0


def obtener_tasa_usdt_binance():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUSD"
        r = requests.get(url, timeout=5)
        data = r.json()
        precio = data.get("price")
        return float(precio) if precio else 0.0

    except Exception as e:
        print("Error USDT Binance:", e)
        return 0.0


def obtener_tasa_usdt_ves():
    try:
        urls = [
            "https://criptoya.com/api/usdt/ves",
            "https://criptoya.com/api/USDT/VES",
        ]

        data = None
        for url in urls:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                break

        if not data or not isinstance(data, dict):
            return 0.0

        # Prefer explicit binance p2p ask if available (closest to market shown in panels)
        try:
            binance = data.get('binancep2p') or data.get('binance')
            if isinstance(binance, dict):
                ask = binance.get('ask')
                if ask and float(ask) > 0:
                    return float(ask)
        except Exception:
            pass

        # Collect all numeric asks > 0 and compute median to avoid zero/outlier distortion
        asks = []
        for item in data.values():
            if isinstance(item, dict):
                a = item.get('ask')
                try:
                    a_f = float(a)
                    if a_f > 0:
                        asks.append(a_f)
                except Exception:
                    continue

        if asks:
            asks.sort()
            n = len(asks)
            mid = n // 2
            if n % 2 == 1:
                return float(asks[mid])
            else:
                return float((asks[mid - 1] + asks[mid]) / 2.0)

    except Exception as e:
        print("Error USDT VES:", e)

    return 0.0


def obtener_tasa_euro_binance():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
        r = requests.get(url, timeout=10)
        data = r.json()
        precio = data.get("price")
        return float(precio) if precio else 0.0

    except Exception as e:
        print("Error EUR Binance:", e)
        return 0.0


def obtener_tasa_euro_usd():
    try:
        url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
        r = requests.get(url, timeout=10)
        data = r.json()
        rates = data.get("rates") or {}
        precio = rates.get("USD")
        if precio:
            return float(precio)
    except Exception as e:
        print("Error EUR/USD Frankfurter:", e)

    try:
        tasa_euro_binance = obtener_tasa_euro_binance()
        tasa_usdt_binance = obtener_tasa_usdt_binance()
        if tasa_euro_binance and tasa_usdt_binance:
            return float(tasa_euro_binance) / float(tasa_usdt_binance)
    except Exception as e:
        print("Error EUR/USD fallback Binance:", e)

    return 0.0