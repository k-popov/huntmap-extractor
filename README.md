# HuntMap geo info extractor

## Description
The tool is extracting geo data on hunting areas from https://huntmap.ru

Source data for the extractor is to be fetched from the site. For different areas (public, private, forbidden) have different data format so the type of area must be passed as argument. For now only public and private areas supported by converter.
**WARNING! Forbidden areas are not excluded from public and private areas. These forbidden areas must be manually checked.**

## Usage:
First install python requirements from `requirements.txt`. `virtualenv` may be used
Get areas data you're interested in and save it to say `map.js` . The exact URL may be discovered from browser inspector, links to data all start with `https://maps.kosmosnimki.ru/TileSender.ashx` and are usually relatively large.
Then run the converter with appropriate are type:
```
python3 huntmap_extract.py <public|private> < map.js > map.geojson
```
Alternatively the script may accept input file name as second argument (source file in the below example is `map.js`):
```
python3 huntmap_extract.py <public|private> map.js > map.geojson
```
The resulting file is GeoJSON which may be vizualized e.g. at https://geojson.tools/ , used in some other viewer or converted to KML.

## Found area links
- Saint-Petersburg and Leningrad region
  - Public hunting areas: https://maps.kosmosnimki.ru/TileSender.ashx?WrapStyle=None&ModeKey=tile&ftc=osm&r=j&LayerName=4F7341B1732B4276BFEE27CC553B81BF&z=1&x=1&y=0&v=207&srs=3857&sw=1
  - Private hunting areas: https://maps.kosmosnimki.ru/TileSender.ashx?WrapStyle=None&ModeKey=tile&ftc=osm&r=j&LayerName=DC6E51836E8A4D8CA12F6098B7DC7FEA&z=1&x=1&y=0&v=990&srs=3857&sw=1

Tested on https://huntmap.ru/karta-oxotnichix-ugodij-leningradskoj-oblasti
