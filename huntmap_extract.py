#!/usr/bin/env python3

import sys
import json
import logging

import geojson
import pyproj

transformer = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326")

def coord_convert_and_fix(leaflet_coordinates):
    # leaflet coordinates are `lat, lon` whereas GeoJSON and KML are `lon, lat`. Source data is for leaflet
    # https://macwright.com/lonlat/
    transformed = transformer.transform(*leaflet_coordinates)
    # need to first thansform and then swap as order matters when converting
    return [transformed[1], transformed[0]]

def read_place_private(place):
    # private areas and common areas have different info formats. forbidden areas have different format too
    # unpack element to readable variable names
    plc_index, plc_region, plc_org, plc_area, plc_central_addr, plc_phone, plc_email, plc_person, plc_local_addr, plc_geo = place
    props = {
        'index': plc_index,
        'region': plc_region,
        'org': plc_org,
        'area': plc_area,
        'central_address': plc_central_addr,
        'phone': plc_phone,
        'email': plc_email,
        'person': plc_person,
        'local_address': plc_local_addr
        }
    logging.info(f'Processed {plc_area} as private place')
    return plc_geo, props

def read_place_public(place):
    # private areas and common areas have different info formats. forbidden areas have different format too
    # unpack element to readable variable names
    plc_index, plc_region, plc_area, plc_local_addr, plc_phone, plc_href, plc_org, plc_geo = place
    props = {
        'index': plc_index,
        'region': plc_region,
        'org': plc_org,
        'area': plc_area,
        'phone': plc_phone,
        'local_address': plc_local_addr,
        'href': plc_href
        }
    logging.info(f'Processed {plc_area} as public place')
    return plc_geo, props

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        raise Exception(f'Usage: {sys.argv[0]} <public|private> < map.js > map.geojson')

    data = json.loads(
            sys.stdin.read().lstrip('gmxAPI._vectorTileReceiver(').rstrip(')')
            )
    logging.info(f'Loaded {len(data["values"])} from input')

    features = []
#pgn = geojson.Polygon([[ transformer.transform(*dot)[-1::-1] for dot in data['values'][0][9]['coordinates'][0] ]])
#features = []
#features.append(geojson.Feature(geometry=pgn, properties={}))
#feature_collection = geojson.FeatureCollection(features)
#with open('myfile.geojson', 'w') as f:
#   json.dump(feature_collection, f, indent=4)
    for place in data['values']:
        logging.info(f'Processing place with index {place[0]}')
        if sys.argv[1] == 'private':
            plc_geo, props = read_place_private(place)
        elif sys.argv[1] == 'public':
            plc_geo, props = read_place_public(place)
        else:
            raise Exception(f'Usage: {sys.argv[0]} <public|private> < map.js > map.geojson')
        if plc_geo['type'] != 'POLYGON':
            # only support polygons
            continue

        logging.info(f'Building polygon for place index {props["index"]}')
        polygon_paths = [] # array of 1st outer polygon contour and later for "holes" in polygon
        for poly_path in plc_geo['coordinates']:
            polygon_paths.append(
                [coord_convert_and_fix(coord) for coord in poly_path]
                )
            
        polygon = geojson.Polygon(polygon_paths)
        features.append(geojson.Feature(geometry=polygon, properties=props))

    logging.info(f'Processed all places, forming FeatureCollection')
    feature_collection = geojson.FeatureCollection(features)
    sys.stdout.write(
        json.dumps(feature_collection, indent=2)
        )
