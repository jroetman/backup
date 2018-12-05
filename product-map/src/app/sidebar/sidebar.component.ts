import { Component, OnInit, Input } from '@angular/core';
import { DataService } from "../services/data.service";
import * as moment from "moment"

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {

  searchView : string = 'product';
  selectedProduct: string;
  selectedProducts: any[];
  @Input('products') products: any[];

  constructor(private data: DataService) { }

  productIndex(index: number, value: any){
     if(this.products) return this.products[index].name;
  }

  getAvailability(prod){
     let cname = "bad"
     const numTaus = prod.images.length;

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
           this.showInstructions = state.showInstructions;
     //    this.selectedProduct = state.selectedProduct;
   //      this.searchView   = state.searchView;
         
      });
  }

}
