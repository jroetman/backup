import { Component, OnInit } from '@angular/core';
import {DataService} from '../services/data.service'

@Component({
  selector: 'app-vector-product',
  templateUrl: './vector-product.component.html',
  styleUrls: ['./vector-product.component.scss']
})
export class VectorProductComponent implements OnInit {

  selectedProducts: any[] = [{name :"test"}];

  constructor(private data: DataService) { }

  selectOption(idx,o) {
     const vp = JSON.parse(JSON.stringify(this.selectedProducts));
     let oidx = vp[idx].selectedOptions.indexOf(o);
     console.log(oidx)
     if(oidx >= 0) {
        vp[idx].selectedOptions.splice(oidx, 1);

     } else {
        vp[idx].selectedOptions.push(o);
     }
     console.log(vp[idx])
     this.data.changeMessage({selectedProducts : vp })
  }

  selectVectorProduct(idx) {
     const vp = JSON.parse(JSON.stringify(this.selectedProducts));
     vp[idx].showLayer = !vp[idx].showLayer;

     this.data.changeMessage({selectedProducts : vp })
  }

  ngOnInit() {
     this.data.currentMessage.subscribe(state => {
           if(state.selectedProducts) {
               this.selectedProducts = state.selectedProducts;
           }
      });
  }

}
