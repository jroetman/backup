import { Component, OnInit } from '@angular/core';
import { DataService } from "../services/data.service";
import { ProductService } from "../services/product.service";
import * as  moment from 'moment'

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})

export class ProductComponent implements OnInit {
  extent:number[];
  regionTree:object;
  showProducts: number[] = [];
  productsUpdate: moment = moment();
  searchView : string = "Product"
  currentDtg: moment;
  regionTreeUpdated: moment = moment();

  constructor(private data: DataService, private prodSvc: ProductService){}

  discoverProductVars(){
      this.products.map(p => {          
           const prod = p;
           if(p.fieldType == 'discover') {
               let dtg = moment(this.currentDtg)
               dtg = dtg.format("YYYYMMDD") + "00";

               fetch('http://docker.nrlmry.navy.mil:5000/discover?model=' + p.model+ '&dtg=' + dtg).then(res =>{
                return res.json();
               }).then(json => {
                   let flds = p.fields.find(f => f.name == 'vars')
                   if(flds) flds.vars = json.filter(v => ["latitude", "longitude"].indexOf(v.name.toLowerCase()) == -1);
                   this.prodSvc.getAvailability(prod) 

               }).catch(err => {
                  prod.images = [];
                  console.log("Nothing Usefull Returned")
               })
           }
     });
  }

  keyIndex(index: number, value: any){
     return value;
  }

  selectView(view) {
      this.data.changeMessage({searchView: view});
  }


  selectProducts(region, key) {
      this.showProducts[region + key] = !this.showProducts[region + key]; 
      this.data.changeMessage({showProducts: this.showProducts, selectedRegion: region, selectedProduct: key});
  }

  rtTrack(index: number, value: any){
    return value;
  }

  ngOnInit() {
    

    this.data.currentMessage.subscribe(state => {
       const extent     = JSON.stringify(state.extent)
       const searchView = JSON.stringify(state.searchView)
       const showProds = JSON.stringify(state.showProducts);

       if(!moment(state.currentDtg).isSame(moment(this.currentDtg))) {
           this.currentDtg = moment(state.currentDtg)
           if(Array.isArray(this.products)) this.discoverProductVars();

       } else if(state.products && !this.productsUpdate.isSame(state.productsUpdate)) {
           this.currentDtg = moment(state.currentDtg)
           this.productsUpdate = moment(state.productsUpdate)
           this.products = state.products
           this.discoverProductVars();
       } 

       if (JSON.stringify(this.extent) != extent || 
           JSON.stringify(this.searchView) != searchView) {

           this.extent = JSON.parse(extent)
           this.searchView = JSON.parse(searchView)
          // this.prodSvc.getRegionTree()

       }

       if (JSON.stringify(this.showProducts) != showProds){
           this.showProducts = JSON.parse(showProds)
           
       }

       if(state.regionTree && !this.regionTreeUpdated.isSame(state.regionTreeUpdated)){
           this.regionTree = state.regionTree
           this.regionTreeUpdated = moment(state.regionTreeUpdated);
       }
  
    });

    this.data.changeMessage({selectedRegion: 0, showProducts: {'0ICAP' : true}) }
}
