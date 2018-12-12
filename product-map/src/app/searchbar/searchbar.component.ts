import { Component, OnInit } from '@angular/core';
import { DataService } from "../services/data.service";
import { ProductService } from "../services/product.service";

@Component({
  selector: 'app-searchbar',
  templateUrl: './searchbar.component.html',
  styleUrls: ['./searchbar.component.scss']
})

export class SearchbarComponent implements OnInit {

  search: string;

  constructor(private data: DataService, private prodSvc: ProductService) { }
 
  updateProds(){
    console.log(this.search)
    this.prodSvc.getProducts(this.search)
    #this.data.changeMessage({searchfilter: event.target.value});
  }

  ngOnInit() { }

}
