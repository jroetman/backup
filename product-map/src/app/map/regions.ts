import Feature from 'ol/Feature.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer.js';
import { OSM, Vector as VectorSource } from 'ol/source.js';
import Map from 'ol/Map';
import { fromLonLat } from 'ol/proj';
import Styles from './styles'

export default class Regions {

    map: Map;
    vectorSource: VectorSource;
    vectorLayer : VectorLayer;

    constructor(map: Map) {
        this.map = map;
        this.vectorSource = new VectorSource({noWrap:true, wrapX:false, wrapDateline:false});
        this.vectorLayer = new VectorLayer({
            source: this.vectorSource,
            style: this.styleFunction,

        });
        this.map.addLayer(this.vectorLayer);
    }

    styleFunction(feature) {
        let s = Styles.highlightStyle[feature.getGeometry().getType()];
        s.getText().setText(feature.get('name'));
        return s;
    }

    transformCoords(a: number[][]) {
        return a.map(function(aa) {
            return fromLonLat(aa)
        });
    }

    createBoxFromEnvelope(a: number[][]) {
        //[[-165, 70], [-55, 15] => -165,70 -55,70 -55,15 -165,15
        let tc = a;//  this.transformCoords(a)
        let c = [tc[0], [tc[0][0],tc[1][1]], tc[1], [tc[1][0],tc[0][1]], tc[0]];
        return c;
    }

    clearRegions(){
        this.vectorSource.clear()

    }

    addRegions(region) {
      let regions = this.computeRegions([region])
      let features= (new GeoJSON()).readFeatures(regions);

      this.vectorSource.clear()
      this.vectorSource.addFeatures(features)
    }

    computeRegions(regions) {
        let json = {
            "type": "FeatureCollection",
              "crs": {
                  'type': 'name',
                  'properties': {
                      'name': 'EPSG:3857'
                  }
            },
          "features": []
      }

      regions.map(r => {
            let coords= [this.createBoxFromEnvelope(r.coordinates)]

            json.features.push({
                properties: { name: r.name},
                type: "Feature",
                geometry: {
                    type: "Polygon",
                    coordinates: coords
                }
            })

        })

        return json;
    }
}
