import { Component, OnInit } from '@angular/core';
import { DataService } from "../services/data.service";
import * as moment from 'moment';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss']
})

export class GalleryComponent implements OnInit {
  showOptions: boolean = true;
  selectedProducts: any[] = [];
  imgPerRow: int = 2;
  selectedProductUpdate: moment = moment();
  currentTau: any;
  currentDtg: any;
  extent: any[];
  

  constructor(private data: DataService) {
  }

  closeGallery(){
      this.data.changeMessage({showGallery: false})
  }


  dragover(evnt){
    evnt.preventDefault();
    this.over = 'over'

  }

  out(evnt){
    evnt.preventDefault();
    this.over = ''

  }

  addProduct(evnt){
     var data = evnt.dataTransfer.getData("text/plain");
     data = JSON.parse(data);
     this.data.addGalleryProduct(data)
     this.over = ''
     if(this.showInstructions) this.data.changeMessage({showInstructions : false})

  }

  createMap(){
     this.data.addGalleryProduct()
     this.over = ''
     if(this.showInstructions) this.data.changeMessage({showInstructions : false})

  }

  getWidth() {
     return (98 / this.imgPerRow) + '%';
  }

  trackByFn(index, prod){
     let hash = prod ?  prod.name + JSON.stringify(prod.layers) : undefined;
     return 1;
  }

  removeProduct(p){
      this.data.removeProduct(p);
  }

  ngOnInit() {

    this.data.currentMessage.subscribe(state => {
         let options = {}
         const region = this.selectedRegion
         this.colors = state.colors;
         this.showInstructions = state.showInstructions;
 

         if(state.selectedProducts.length == 0) {
             this.selectedProducts = []; //JSON.parse(JSON.stringify(state.selectedProducts))
             
         } else if(!moment(state.selectedProductUpdate).isSame(moment(this.selectedProductUpdate))) {
             //currentDtg and or tau aren't initialized on init, get from dfeault state
             this.currentDtg= moment(state.currentDtg);
             this.currentTau= state.currentTau;
             this.selectedProductUpdate = moment(state.selectedProductUpdate)
             this.extent  = [...state.extent]
             this.selectedProducts = JSON.parse(JSON.stringify(state.selectedProducts))

           
         } else if(JSON.stringify(this.extent) != JSON.stringify(state.extent)){
            this.extent  = [...state.extent]

         } else if(!moment(state.currentDtg).isSame(moment(this.currentDtg))){
            this.currentDtg= moment(state.currentDtg);

         } else if(state.currentTau != this.currentTau){
            this.currentTau= state.currentTau;

         } 

    });
  }
}
