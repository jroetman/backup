import { Inject, Injectable } from '@angular/core';
import * as moment from 'moment';
import { DataService } from "../services/data.service";

@Injectable()
export class ColorbarService {


  constructor(private data: DataService) { }

  getColors() {
     fetch("http://docker.nrlmry.navy.mil:5000/icap/getColors").then(res =>{
        return res.json();

     }).then(json => {
        this.data.changeMessage({colors: json.colors});

     });
  }

 assignColorbar(cid,plid,layer,map){
     fetch("http://docker.nrlmry.navy.mil:5000/icap/assignColorbar", {
           method: "POST",
           cache: "no-cache",
           headers: { "Content-Type" : "application/json"},
           body: JSON.stringify({cid : cid, plid : plid})
        }).then(res =>{
           //update colors return the new selected list of colors
           return res.json();

        }).then(async (json) => {
           const maps  = JSON.parse(JSON.stringify(this.data.messageSource.getValue().selectedProducts))

           const m =  maps.find(pr => pr.name == map.name)
           const l =  m.layers.find(l => l.guid == layer.guid)
           m.layersUpdated = moment()

           //assign colorid to appropriate level
           const level = l.field.levels.find(l => l.plid == plid)
           level.color_id = cid

           await this.data.changeMessage({colors: json.colors, selectedProducts: maps, selectedProductUpdate: moment()});

        });
 }

 createColorbar(cid,name, domains, palette,map, layer, plid){
     fetch("http://docker.nrlmry.navy.mil:5000/icap/updateColor", {
           method: "POST",
           cache: "no-cache",
           headers: { "Content-Type" : "application/json"},
           body: JSON.stringify({colorId : cid, name: name, domains : domains, palette: palette})
        }).then(res =>{
           //update colors return the new selected list of colors
           return res.json();

        }).then(async (json) => {
           //if this was a new colorbar, send the id of the newly created one
           const maps  = JSON.parse(JSON.stringify(this.data.messageSource.getValue().selectedProducts))

           const m =  maps.find(pr => pr.name == map.name)
           const l =  m.layers.find(l => l.guid == layer.guid)
           m.layersUpdated = moment()

           //assign colorid to appropriate level
           const level = l.field.levels.find(l => l.plid == plid)
           level.color_id = json.cid

           this.data.changeMessage({colors: json.colors, selectedProducts: maps, selectedProductUpdate: moment()});
                        

        });
    }
 

 updateColorbar(cid,name, domains, palette,map, max){
     fetch("http://docker.nrlmry.navy.mil:5000/icap/updateColor", {
           method: "POST",
           cache: "no-cache",
           headers: { "Content-Type" : "application/json"},
           body: JSON.stringify({max: max, colorId : cid, name: name, domains : domains, palette: palette})
        }).then(res =>{
           //update colors return the new selected list of colors
           return res.json();

        }).then(async (json) => {
           const maps  = JSON.parse(JSON.stringify(this.data.messageSource.getValue().selectedProducts))
           const m =  maps.find(pr => pr.name == map.name)
           m.layersUpdated = moment()

           this.data.changeMessage({colors: json.colors, selectedProducts: maps, selectedProductUpdate: moment()});

           //if this was a new colorbar, send the id of the newly created one
                        

        });
    }
 
    removeColorbar(cid,map){
        fetch("http://docker.nrlmry.navy.mil:5000/icap/removeColorbar", {
              method: "POST",
              cache: "no-cache",
              headers: { "Content-Type" : "application/json"},
              body: JSON.stringify({cid: cid})
           }).then(res =>{
              //update colors return the new selected list of colors
              return res.json();
   
           }).then(async (json) => {
              //const prods = JSON.parse(JSON.stringify(this.data.messageSource.getValue().selectedProducts))
              //let p = prods.find(pr => pr.name == map.name)
              //p.layersUpdated = moment()
   
              this.data.changeMessage({colors: json.colors});
              //this.data.redrawProduct(map);
   
           });
    }
}
