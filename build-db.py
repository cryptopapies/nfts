#!/usr/bin/env python3

from glob import glob
import json
from os import path
from sys import argv, exit
from typing import List, Dict, Any

BASE_IMAGE_URL = "https://raw.githubusercontent.com/cryptopapies/nfts/main"

Database = Dict[str, Any]


def url(path: str) -> str:
    return f"{BASE_IMAGE_URL}/{path}"


def load_metadata(path: str) -> Database:
    with open(path) as f:
        data = f.read()
        f.close()
        return json.loads(data)


def push_collection(
    db: Database, collection_name: str, collection_dir: str
) -> Database:
    collection = {}
    for item in glob(f"{collection_dir}/*.json"):
        # get basename to store in dictionary
        base_name = path.basename(path.splitext(item)[0])
        # load metadata
        metadata = load_metadata(item)
        # get image url
        image_path = f"{path.splitext(item)[0]}.png"
        metadata["image"] = url(image_path)
        collection[base_name] = metadata
    db[collection_name] = collection
    return db


def main(args: List[str]) -> int:
    if len(args) < 1:
        print("Usage: <db.json>")
        return 255

    db_name = args[0]
    database = {}
    database = push_collection(database, "dubaiPapi", "dubai-papi")

    # write database
    with open(db_name, "w") as f:
        f.write(json.dumps(database))
        f.close()
    # exit
    return 0


if __name__ == "__main__":
    exit(main(argv[1:]))
