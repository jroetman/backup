import { Component, OnInit,  Input } from '@angular/core';
import * as moment from 'moment';
import { DataService } from "../../services/data.service";


@Component({
  selector: 'app-layer',
  templateUrl: './layer.component.html',
  styleUrls: ['./layer.component.scss']
})
export class LayerComponent implements OnInit {

  level_id: int = 85;
  alpha: float = 100;
  plotType: any;
  extras: any = {};
  colors: any[] = [];
  guid: any;
  isVisible: true;

  @Input('layer') layer: any;
  @Input('parent_guid') parent_guid: any;

  constructor(private data: DataService) { }

  removeLayer(){
       const prods = JSON.parse(JSON.stringify(this.selectedProducts))
       const map = prods.find(p => p.name == this.parent_guid);
       map.layersUpdated = moment();

       const idx  = map.layers.findIndex(l => l.guid == this.guid)
       map.layers.splice(idx, 1);
       this.data.changeMessage({selectedProducts : prods, selectedProductUpdate : moment()});
  }

  removeProduct(p){
      this.data.removeProduct(p);
  }

  updateExtra(optName){ 
      const prods = JSON.parse(JSON.stringify(this.selectedProducts))

      const map = prods.find(p => p.name == this.parent_guid);
      map.layersUpdated = moment();

      const layer = map.layers.find(l => l.guid == this.guid)
      const optVal = this.extras[optName]

      layer.options[optName]=  optVal;
      this.data.changeMessage({selectedProducts : prods});
  }


  updateOption(name){
      const prods = JSON.parse(JSON.stringify(this.selectedProducts))

      const map = prods.find(p => p.name == this.parent_guid);
      map.layersUpdated = moment();

      const layer = map.layers.find(l => l.guid == this.guid)
      layer.options[name]= this[name];

      this.data.changeMessage({selectedProducts : prods});
  }



  showHide(){
      const prods = JSON.parse(JSON.stringify(this.selectedProducts))
      const map = prods.find(p => p.name == this.parent_guid);
      map.layersUpdated = moment();

      const layer = map.layers.find(l => l.guid == this.guid)
      layer.options.isVisible = layer.options.isVisible == null ? false : !layer.options.isVisible;

      this.data.changeMessage({selectedProducts : prods});
  }

  updateLevel(){
      const prods = JSON.parse(JSON.stringify(this.selectedProducts))
      const lvl = this.layer.field.levels.find(l => l.plid == this.level_id)

      const map = prods.find(p => p.name == this.parent_guid);
      map.layersUpdated = moment();

      const layer = map.layers.find(l => l.guid == this.guid)
      layer.options[name]= this[name];
      layer.options.level = lvl.level
      layer.options.level_id = lvl.plid

      this.data.changeMessage({selectedProducts : prods});
  }

  ngOnInit() {
      const layer = this.layer
      this.level_id = layer.options.level_id ? layer.options.level_id : layer.field.levels[0].plid;
      this.alpha    = layer.options.alpha    ? layer.options.alpha  : 100;
      this.guid      = this.layer.guid;

      //These options are set in the database for a given field.
      //Initially created to provide stream/feather options for wind vector
      this.field_options = layer.field.options ? JSON.parse(layer.field.options) : [];

      if (this.field_options.length > 0) {
          //set these option choice on the component for various inputs
          let optName = this.field_options[0].name;
          let defaultVal = this.field_options[0].options[0].name;

          if (!layer.options[optName]) {
              this.extras[optName] = defaultVal; 

          } else {
              this.extras[optName] = layer.options[optName];

          }
      }

      this.data.currentMessage.subscribe(state => {
          this.colors = state.colors ? state.colors : [];
          const stateSp = JSON.stringify(state.selectedProducts);

          if (stateSp != JSON.stringify(this.selectedProducts)){
            this.selectedProducts = JSON.parse(stateSp);

          }

      });
  }

}
