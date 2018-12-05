import { Component, OnInit } from '@angular/core';
import { DataService } from "../services/data.service";

@Component({
  selector: 'app-searchbar',
  templateUrl: './searchbar.component.html',
  styleUrls: ['./searchbar.component.scss']
})

export class SearchbarComponent implements OnInit {

  search: string;

  constructor(private data: DataService) { }
 
  onKey(event: any){
    this.data.changeMessage({searchfilter: event.target.value});
  }

  ngOnInit() {
    this.data.currentMessage.subscribe(state => {
       this.extent = state.extent
       this.regionTree = state.regionTree
       this.showProducts = state.showProducts
    });
  }

}
