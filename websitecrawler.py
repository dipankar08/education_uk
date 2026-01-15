import requests

def enumerate_uploads(base, start_year=2015, end_year=2026):
    pdfs = set()

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            url = f"{base}/wp-content/uploads/{year}/{month:02d}/"
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and ".pdf" in r.text.lower():
                    # crude but effective
                    for line in r.text.split():
                        if ".pdf" in line.lower():
                            pdfs.add(line)
            except:
                pass

    return pdfs
