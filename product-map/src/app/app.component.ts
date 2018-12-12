import { Component, OnInit } from '@angular/core';
import { DataService } from "./services/data.service";
import { ColorbarService} from "./services/colorbar.service";
import { ProductService } from "./services/product.service";
import { Inject, Injectable } from '@angular/core';
import { SESSION_STORAGE, StorageService } from 'angular-webstorage-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  constructor(private prodSvc: ProductService, private colors: ColorbarService, private data: DataService, @Inject(SESSION_STORAGE) private storage: StorageService){}


  ngOnInit() {

    const state = this.storage.get("nrlmaproom") 
    this.prodSvc.getProducts();


    if(state) {
       //this.data.changeMessage(JSON.parse(state))
    }
    const colors = this.colors.getColors(); 
    this.data.changeMessage({colors: colors})

    this.data.currentMessage.subscribe(state => {
       this.showGallery = state.showGallery;
       this.showProducts = state.showProducts;
       this.selectedProducts = state.selectedProducts;
       this.showInstructions = state.showInstructions;
    });
  }

}
