import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import * as moment from 'moment';
import ColorbarService from './colorbar.service'
import {PRODUCTS } from '../product/mock-products'
import { SESSION_STORAGE, StorageService } from 'angular-webstorage-service';


@Injectable()
export class DataService {

  defaultState = {showProducts: {},
                  showInstructions: true,
                  showGallery: false,
                  extent : [180,-90,180,90],
                  products : PRODUCTS,
                  productsUpdate : moment(),
                  searchView : "product",
                  regionTree : null,
                  productSelection: {},
                  selectedProduct: null,
                  selectedProducts: [],
                  selectedProductUpdate:moment(), 
                  selectedRegion: {name:"Global"}, 
                  searchfilter: "",
                  currentDtg: moment().startOf("day"),
                  currentTau: 0}

  private messageSource = new BehaviorSubject(this.defaultState);
  currentMessage = this.messageSource.asObservable();

  constructor(@Inject(SESSION_STORAGE) private storage: StorageService){}

  async changeMessage(message: any) {

    let prevMessage = this.messageSource.getValue()
    let m =Object.assign({}, prevMessage, message);
     
    if (message.selectedProducts) m.selectedProductUpdate = moment();
    if (message.products) m.productsUpdate = moment();

    this.messageSource.next(m)
    this.storage.set("nrlmaproom", JSON.stringify(m)) 
    console.log("NEW STATE")
    console.log(m)
  
  }

  getMessageSource(){
    return this.messageSource;

  }

  removeProduct(p){
      const prods = JSON.parse(JSON.stringify(this.messageSource.getValue().selectedProducts))
      prods.splice(prods.findIndex(pr => pr.name == p.name), 1)
      this.changeMessage({selectedProducts: prods, productSelection: {}})

  }

  addGalleryProduct(sp){
      const prods = JSON.parse(JSON.stringify(this.messageSource.getValue().selectedProducts))
      const newMap = { name: "Map " + moment().format("YYYY-MM-DD HH:mm:ss"), layers : []}

      if(sp) {
        newMap.layers.push(sp)
      }

      prods.push(newMap)
      this.changeMessage({productSelection: newMap, selectedProducts: prods, selectedProductUpdate : moment()})

  }

  redrawProduct(guid){
      const prods = JSON.parse(JSON.stringify(this.messageSource.getValue().selectedProducts))
      let p = prods.find(pr => pr.guid == guid)

      //update: Date.now() forces gallery to re-render image. update could be called anything else 
      p.options.update = Date.now()
      
      this.changeMessage({selectedProducts: prods})

  }

}
