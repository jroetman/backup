import { Component, OnInit } from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import {boundingExtent} from 'ol/extent';
import {get as getProjection, transformExtent} from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import KML from 'ol/format/KML.js';
import XYZ from 'ol/source/XYZ';
import { DataService } from "../services/data.service";
import { Tile as olTileLayer, Vector as VectorLayer } from 'ol/layer.js';
import { OSM, Vector as VectorSource } from 'ol/source.js';
import Regions from "./regions"
import DataLayer from "./DataLayer"
import ImageLayer from "./ImageLayer"
import * as moment from 'moment'

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css'],
  providers: []
})
export class MapComponent implements OnInit {
  message:number[];
  map:Map;
  regions: Regions;
  products: {};
  extent : number[];
  extentdisplay : number[];
  selectedRegion: any = {}; 
  fromProjection = getProjection("EPSG:3857");
  toProjection = getProjection("EPSG:4326"); // to Spherical Mercator Projection
  DataLayer: DataLayer;

  constructor(private data: DataService ) { }

  ngOnInit() {
   

    this.data.currentMessage.subscribe(state => {

       if(state.selectedProducts && this.DataLayer) {

            state.selectedProducts.map((p, idx) => {
                const prod = state.products.find(pr => pr.id == p.id)

                if(p.showLayer && this.selectedProducts){
                   let img = prod.images.find(i => {
                     return moment(i.time).isSame(state.currentTau)
                   })
                   if(img) this.ImageLayer.addImageLayer(prod, img, state.extent);
                }
            })
            this.selectedProducts = state.selectedProducts;
       }

       if(state.highlightRegion) {
           this.regions.addRegions(state.highlightRegion)
          
       } else { 
           this.regions && this.regions.clearRegions()
       }

       if(state.selectedRegion.clicked || (state.selectedRegion.id != this.selectedRegion.id)) { 
          this.selectedRegion =  {...state.selectedRegion}

          let loc = this.selectedRegion.coordinates
          if(loc) { 
              var extent = [loc[0][0],loc[1][1], loc[1][0], loc[0][1]] 
              console.log(map.getView())
              map.getView().fit(extent, {size: map.getSize(), constrainResolution: false})
          }
           
           this.selectedRegion.clicked = false
           this.data.changeMessage({selectedRegion : this.selectedRegion})
       }

       this.products = state.products
       this.extent = [...state.extent]
       if(this.extent) this.extentdisplay = state.extent.map(e => e.toFixed(2))

    })

    const map = new Map({
      target: 'mapContainer',
      controls: [ ],
      layers: [
        new TileLayer({
           source: new XYZ({
            url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          })
        }),
      ],
      view: new View({
        center: [0, 0],
        zoom:0,
        minZoom: this.getMinZoom(),
        projection: 'EPSG:4326'
      }),
    });
    this.map = map;
    this.regions= new Regions(this.map)
    this.DataLayer = new DataLayer(this.map)
    this.ImageLayer = new ImageLayer(this.map)

    map.on("movestart", () => {
       console.log("CLEAR")
       clearTimeout(this.updateTimeout)
    });

    map.on("moveend", () => {

       this.updateTimeout = setTimeout(() =>{
         this.updateExtent();
       }, 1000)
    });

    map.on("zoomend",  () => {
        this.updateExtent()
    });

    var extent = [-180,-90,180,90]
    map.getView().fit(extent, map.getSize());

  }


  getMinZoom = () => {
    var width = document.getElementById('mapContainer').clientWidth;
    return Math.ceil(Math.LOG2E * Math.log(width / 256));
  }

  updateExtent = () => {
     if(this.map && this.map.getView) {
         var ext = this.map.getView().calculateExtent()
         var extent = ext //transformExtent(ext, this.fromProjection, this.toProjection);
         this.data.changeMessage({extent : extent})
     }
  }
}
