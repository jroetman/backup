import { Component, OnInit, Input } from '@angular/core';
import { DataService } from "../services/data.service";
import * as moment from "moment"

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {

  
  showMe: any = {};
  mapChanged : boolean = true;
  searchView : string = 'product';
  selectedProduct: string;
  selectedProducts: any[];
  productSelection: any  = {};
  @Input('products') products: any[];

  constructor(private data: DataService) { }

  productIndex(index: number, value: any){
     if(this.products) return this.products[index].name;
  }

  getLayerSelected(p,f){
     let index = -1;
     const map = this.selectedProducts.find(sp => sp.name == this.productSelection.name);

     if (map && map.layers)
         index = map.layers.findIndex(l => l.model == p.model && l.field.varname == f.varname)

     return index;
  }

  addLayer(p,f){
    const prods = JSON.parse(JSON.stringify(this.selectedProducts))
    const map = prods.find(p => p.name == this.productSelection.name);
    let lidx = this.getLayerSelected(p,f) 

    if (lidx >= 0) {
        map.layers.splice(lidx,1) 
 
    } else {
        const layer = this.getSelectedProduct(p,f)
        layer.options.isVisible = true;
        map.layers.push(layer)
    }

    map.layersUpdated = moment()
    this.data.changeMessage({selectedProducts : prods});
  }

  getLatest(prod){
     let latest = ""
     const images = prod.images
     if(Array.isArray(prod.images) && prod.images.length == 1){
       latest =   prod.images[0].latest ? "Latest: " + prod.images[0].latest : "";
      
     }
     return latest;
  }

  getAvailability(prod){
     let cname = "bad"
     const numTaus = Array.isArray(prod.images) && prod.images.length;
     if (numTaus) {
       if (numTaus >= 15) cname = "good"
       if (numTaus < 15 ) cname = "warning"
     }

     return "availability " + cname;
  }

  getSelectedProduct(prod, field){
    const guid = prod.id +  field.varname + Date.now()
    const level = field.levels.find(l => return true); 

    return {guid: guid, options: {level: level.level, level_id:level.plid}, id:prod.id, field: field, model: prod.model, name: prod.name};

  }

  addProductToGallery(prod, field){
    this.data.addGalleryProduct(this.getSelectedProduct(prod,field))
    if(this.showInstructions) this.data.changeMessage({showInstructions : false})

  }

  startDrag(evnt, prod, field){
    const sprod = this.getSelectedProduct(prod,field)
    this.dragging = true;
    evnt.dataTransfer.setData("text/plain",JSON.stringify(sprod))
    evnt.dataTransfer.effectAllowed = "copy";

  }

  ngOnInit() {
       this.data.currentMessage.subscribe(state => {
           const sps = JSON.stringify(state.selectedProducts) 
           if(JSON.stringify(this.selectedProducts) != sps) {
               this.selectedProducts =JSON.parse(sps)
           }
           if(this.productSelection.name != state.productSelection.name){
               this.productSelection = state.productSelection;
           }
           this.highlightFields = state.highlightFields;
           this.showInstructions = state.showInstructions;
     //    this.selectedProduct = state.selectedProduct;
   //      this.searchView   = state.searchView;
         
      });
  }

}
