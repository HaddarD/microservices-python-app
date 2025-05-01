from typing import Dict, Any
from pathlib import Path
import json
import os
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound
from services import root_dir, nice_json

app = Flask(__name__)

def load_movies() -> Dict[str, Any]:
    """Load movies data from JSON file"""
    movies_file = root_dir() / "database" / "movies.json"
    try:
        with open(movies_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        app.logger.error(f"Movies database file not found at {movies_file}")
        return {}
    except json.JSONDecodeError:
        app.logger.error(f"Invalid JSON in movies database file {movies_file}")
        return {}

movies = load_movies()

@app.route("/", methods=['GET'])
def hello() -> Dict[str, Any]:
    """Root endpoint showing available routes"""
    return {
        "uri": "/",
        "subresource_uris": {
            "movies": "/movies",
            "movie": "/movies/<id>"
        }
    }

@app.route("/movies/<movieid>", methods=['GET'])
def movie_info(movieid: str) -> Dict[str, Any]:
    """Get information about a specific movie"""
    if movieid not in movies:
        app.logger.warning(f"Movie {movieid} not found")
        raise NotFound(description=f"Movie {movieid} not found")

    result = movies[movieid].copy()
    result["uri"] = f"/movies/{movieid}"
    result["port"] = request.environ.get("SERVER_PORT", "unknown")
    return result

from flask import request

@app.route("/movies", methods=['GET'])
def movie_record() -> Dict[str, Any]:
    """Get all movies"""
    result = movies.copy()
    # Add port to response for testing
    result["port"] = os.environ.get("PORT", "5001")
    return result


def main() -> None:
    """Main entry point for the application"""
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 5001))

    print(f"Starting Movies service on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()

