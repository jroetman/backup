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
        this.data.changeMessage({colors: json});

     });
  }

 updateColorbar(cid, domains, palette,guid){
     fetch("http://docker.nrlmry.navy.mil:5000/icap/updateColor", {
           method: "POST",
           cache: "no-cache",
           headers: { "Content-Type" : "application/json"},
           body: JSON.stringify({colorId : cid, domains : domains, palette: palette})
        }).then(res =>{
           //update colors return the new selected list of colors
           return res.json();

        }).then(async (json) => {
           await this.data.changeMessage({colors: json});
           this.data.redrawProduct(guid);

        });
    }
}
