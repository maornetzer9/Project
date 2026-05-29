from flask import Flask, jsonify, send_file
from fetch_characters import get_characters
import os, io, csv

app = Flask(__name__)

# Cache – קוראים ל-API רק פעם אחת
_cache = None

def get_cached_characters():
    global _cache
    if _cache is None:
        _cache = get_characters()
    return _cache


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok", "message": "Service is running 🚀"}), 200


@app.route("/characters")
def characters():
    data = get_cached_characters()
    return jsonify({"count": len(data), "characters": data}), 200


@app.route("/characters/csv")
def characters_csv():
    data = get_cached_characters()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["Name", "Location", "Image"])
    writer.writeheader()
    writer.writerows(data)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="characters.csv",
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)