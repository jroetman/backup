import { Component, OnInit,  Input } from '@angular/core';
import { DataService } from "../services/data.service";
import * as moment from 'moment';

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.scss']
})
export class OptionsComponent implements OnInit {

  selectedProducts: any[];
  guid: any;
  colors: any[] = [];
  level_id: int = 85;
  showLayers: boolean = false;

  @Input('map') map: any;
  @Input('idx') map_idx: number;

  constructor(private data: DataService) { }

  removeProduct(p){
      this.data.removeProduct(p);
  }


  dragover(evnt){
    evnt.preventDefault();
    console.log("over")
    this.over = 'over'

  }

  out(evnt){
    evnt.preventDefault();
    this.over = ''

  }

  addLayer(evnt){
    var data = evnt.dataTransfer.getData("text/plain");
    data = JSON.parse(data);
    data.options.isVisible = true;
 
    const prods = JSON.parse(JSON.stringify(this.selectedProducts))
    const map = prods.find(p => p.name == this.map.name);
    map.layersUpdated = moment()
 
    let layerAdded = map.layers.findIndex(l => l.guid == data.guid)
    if (layerAdded == -1) map.layers.push(data)

    this.data.changeMessage({selectedProducts : prods});
    this.over = ''
  }


  drag(evnt){ }

  startDrag(evnt){
    this.dragging = true;
    evnt.dataTransfer.setData("text/plain",JSON.stringify(this.sp))
    evnt.dataTransfer.effectAllowed = "copy";
  }

  ngOnInit() {
      this.guid = this.map.name;

      this.data.currentMessage.subscribe(state => {
          this.colors = state.colors ? state.colors : [];
          const stateSp = JSON.stringify(state.selectedProducts);

          if (stateSp != JSON.stringify(this.selectedProducts)){
            this.selectedProducts = JSON.parse(stateSp);

          }

      });
  }

}
