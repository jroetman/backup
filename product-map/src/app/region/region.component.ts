import { Component, OnInit } from '@angular/core';
import {regions} from '../product/mock-products'
import { DataService } from "../services/data.service";

@Component({
  selector: 'app-region',
  templateUrl: './region.component.html',
  styleUrls: ['./region.component.scss']
})
export class RegionComponent implements OnInit {
    
  regions: any[];
  selectedRegion: any = {name:""}

  constructor(private data: DataService ) { }

  ngOnInit() {
       const r = [...regions]
       r.sort((a,b) =>{ 
         const x = a.name.toLowerCase()  
         const y = b.name.toLowerCase()
         if (x > y) return 1
         if (x < y) return -1
         return 0 
       });
       this.regions = r

       this.data.currentMessage.subscribe(state => {
          if(state.selectedRegion.name != this.selectedRegion.name) {
              this.selectedRegion = {...state.selectedRegion}
          }
       }

  }

  highlightRegion(r) {
      this.data.changeMessage({highlightRegion: r})
  }

  zoomToRegion(r) {
      this.selectedRegion = r
      //in case we already have the region selected
      r.clicked = true;
      this.data.changeMessage({selectedRegion: r})
  }

}
