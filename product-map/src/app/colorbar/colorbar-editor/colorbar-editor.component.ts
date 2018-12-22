import { Component, OnInit } from '@angular/core';
import { EventEmitter, Input, Output } from '@angular/core';
import { DataService } from "../../services/data.service";
import { ColorbarService} from "../../services/colorbar.service";

@Component({
  selector: 'app-colorbar-editor',
  templateUrl: './colorbar-editor.component.html',
  styleUrls: ['./colorbar-editor.component.scss']
})
export class ColorbarEditorComponent implements OnInit {

  palette: [];
  domains: [];
  max: string = "#f00";
  color: any = {};
  colorId : any;
  colorName : any;
  specificDomains: any = "";
  rangeDomains: any = "";
  previousDomains: array = [];
  domainType: string;

  @Output() cancelEdit = new EventEmitter<boolean>();
  @Input('color') color: any;
  @Input('map') map: any;

  constructor(private colorService: ColorbarService, private data: DataService) { }


  updateName(){
    this.saveBar = true;
  }

  updateDomainType(){
    this.previousDomains.push([...this.domains])

    if (this.domainType == "specificDomain") {
       //use previous in case user switches back and forth from specific to range 
       const plen = this.previousDomains.length
       if (plen >= 2) {
           if (this.previousDomains[plen - 2].length ==  this.palette.length){
               this.domains = [...this.previousDomains[plen - 2]] 
               this.previousDomains = [];
               return
           }
       }

       //const avg = (parseInt(this.domains[1]) + parseInt(this.domains[0])) / this.palette.length
       let newDomains = this.palette.map((p,i) =>  0)
       newDomains[0] = this.domains[0];
       newDomains[newDomains.length - 1] = this.domains[this.domains.length - 1];
       this.domains = newDomains.map(d => parseFloat(d).toFixed(2));

    }

    if (this.domainType == "domainRange") {
       this.domains = [this.domains[0], this.domains[this.domains.length - 1]]
       this.domains = this.domains.map(d => parseFloat(d).toFixed(2));
    } 

    this.saveBar = true;
 
  }
 
  updateDomains(){
    console.log(this.domains)
    this.saveBar = true;
  }

  addColor(i){
    if(!this.previousPalette) this.previousPalette = [...this.palette]

    this.palette.splice(i,0,"#ffffff");
    let  nextVal = this.domains[i];

    if(i > 0) nextVal = (parseFloat(this.domains[i-1]) + parseFloat(nextVal)) / 2;

    this.saveBar = true;
    if (this.domainType == "specificDomain") {
       this.domains.splice(i,0,0)
       if (i>0) this.domains[i] = this.domains[i - 1];

    } 
  }

  updatePalette(){
     this.saveBar = true;

  }

  saveColorbar(){
    this.saveBar = false;
    //storing everything as strings
    this.domains = this.domains.map(d => d.toString())
    this.colorService.updateColorbar(this.colorId, this.colorName, this.domains, this.palette, this.map, this.max)

  }
  
  reset(){
    this.palette= this.color.palette.split(",")
    this.domains = this.color.domains.split(",")
    this.colorName = this.color.name;
    this.colorId = this.color.id;

    if(this.domains.length ==2) this.domainType = "domainRange"

  }

  removeColor(i){
    if(!this.previousPalette) this.previousPalette = [...this.palette]

    this.palette.splice(i,1);

    if (this.domainType == "specificDomain") {
       this.domains.splice(i,1)
    } 
    this.saveBar = true;
  }


  indexTrack(index: number, value: any){
     return index;

  }

  updateChoice(){
      this.domains = [...this.color.domains]
      this.palette = [...this.color.palette]

      if (!Array.isArray(this.color.domains)) {
          this.domains = this.color.domains.split(",")
          this.palette = this.color.palette.split(",")
      }

      this.colorId = this.color.id;
      this.colorName = this.color.name;

      if(this.domains.length == 2) {
          this.domainType = "domainRange"

      } else {
          this.domainType = "specificDomain"

      }


  }

  cancel(){
    this.cancelEdit.emit(true)
  }

  ngOnChanges(changes: SimpleChanges) {
      const po = changes.color ? changes.color.previousValue : {};
      const pn = changes.color ? changes.color.currentValue : {};

      if(this.color.palette && this.color.domains && po && pn && (po.id != pn.id)) this.updateChoice()
 
  }

  ngOnInit() {
      if (this.color.palette && this.color.domains)
      this.updateChoice()
  }

}
