#!/usr/bin/python

from bs4 import BeautifulSoup

WATCH_HISTORY_FILE = "watch-history.html"

def main():
    html = None
    with open(WATCH_HISTORY_FILE) as f:
        html = f.read()
    if html == None:
        print("Error reading html")
        return

    print("Parsing html...")
    soup = BeautifulSoup(html, "html.parser")
    print("Outputing to CSV...")

    main_container = soup.body.div
    import csv
    with open("out.csv", "w") as f:
        writer = csv.DictWriter(f, ["time", "title"])
        writer.writeheader()
        for c in main_container.children:
            if str(type(c)) != "<class 'bs4.element.Tag'>":
                continue  # skip text
            content_cell = c.find_all(class_="content-cell")[0]

            if content_cell.contents[0].strip() != "Watched":
                continue
            if len(content_cell.contents) > 6:
                print("\nlarge content_cell:\n", content_cell)

            try:
                video = {
                    "title": content_cell.contents[1].text,
                    "time": content_cell.contents[-1].text,
                }
                writer.writerow(video)
            except:
                print("error getting video from:\n",content_cell)
                continue


if __name__=="__main__":
    main()
