from flask import Flask, render_template, request, send_file, url_for
from scraper.scrape_MFD_project import main
import csv
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"].strip()
        if not city:
            return render_template("index.html", error="Please enter a city.")

        emails = main(city)
        csv_filename = f"advisor_emails_{city}.csv"
        csv_path = os.path.join(app.root_path, "static", csv_filename)
        print(csv_path)

        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Email"])
            for email in emails:
                writer.writerow([email])

        for _ in range(10):
            if os.path.exists(csv_path):
                break
            time.sleep(0.1)  # 100ms
        download_link = url_for('static', filename=csv_filename)
        return render_template("index.html", emails=emails, download_link=download_link, city=city)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)