import {boundingExtent} from 'ol/extent';
import {get as getProjection, transformExtent} from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import { Tile as olTileLayer, Vector as VectorLayer } from 'ol/layer.js';
import { OSM, Vector as VectorSource } from 'ol/source.js';
import Map from 'ol/Map';
import Styles from './styles'
import GeoJSON from 'ol/format/GeoJSON.js';
import { fromLonLat } from 'ol/proj';

export default class DataLayer  {
  map: Map;
  vectorLayers  = {};
  extent : number[];
  fromProjection = getProjection("EPSG:3857");
  toProjection = getProjection("EPSG:4326"); // to Spherical Mercator Projection

  constructor(map: Map) {
    this.map = map;

  }

  styleFunction(feature) {
      let s = Styles.styles[feature.getGeometry().getType()];
      //s.getText().setText(feature.get('name'));
      return s;
  }

  addVectorLayer(p, img){
    const vectorLayer = new VectorLayer({
      source: new VectorSource({
         url: img.geojson,
         format: new GeoJSON(),
         style: this.styleFunction
       }),
    });
    if(this.vectorLayers[p.name]) this.map.removeLayer(this.vectorLayers[p.name])
    this.vectorLayers[p.name] = vectorLayer;

    this.map.addLayer(vectorLayer);
  }
}
