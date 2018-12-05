import {get as getProjection, transformExtent} from 'ol/proj';
import Projection from 'ol/proj/Projection.js';
import {Image as ImageLayer} from 'ol/layer.js';
import Static from 'ol/source/ImageStatic.js';
import Map from 'ol/Map';
import { fromLonLat } from 'ol/proj';

export default class ImageLayer  {
  map: Map;
  imageLayers = {};
  extent : number[];
  fromProjection = getProjection("EPSG:3857");
  toProjection = getProjection("EPSG:4326"); // to Spherical Mercator Projection

  constructor(map: Map) {
    this.map = map;
  }

  addImageLayer(p, img, extent){
    const ext = extent[0] + "," + extent[3] + "," + extent[2] + "," + extent [1];
    console.log(ext)

    if(this.imageLayers[p.name]) this.map.removeLayer(this.imageLayers[p.name]);
    let options ="i";
    if(p.selectedOptions) {
       options =  p.selectedOptions.map(o => "&" + o + "=true")
    }

    let size = this.map.getSize();
    console.log(size)
    let imageLayer = new ImageLayer({
      source: new Static({
           url: img.url + "&width=" + size[0] + "&height=" + size[1] + "&extent=" + ext + "&region=" + p.location.regionName + options,
           imageExtent: extent   //transformExtent(extent, this.toProjection, this.fromProjection)
         })
    });
    this.imageLayers[p.name] = imageLayer
    this.map.addLayer(imageLayer)
  }
}
