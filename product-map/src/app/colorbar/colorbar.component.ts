import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { DataService } from "../services/data.service";
import {DomSanitizer} from '@angular/platform-browser';
import {DomSanitizer} from '@angular/platform-browser';
import { ColorbarService} from "../services/colorbar.service";
import * as moment from 'moment';
import * as d3 from "d3";

let width = 200;
const height = 25;
const margins = {top:10, left : 0, right: 0, bottom: 0}

@Component({
  selector: 'app-colorbar',
  templateUrl: './colorbar.component.html',
  styleUrls: ['./colorbar.component.scss']
})
export class ColorbarComponent implements OnInit {

  palette: [];
  color: any = {};
  type: string = "Linear";
  colorName : any;
  colorId : any;
  colorUrl: any = "";
  specificDomains: any = "";
  rangeDomains: any = "";
  domains: any = "";
  displayDomains: any ="";
  prevDomains: any = "";
  
  @Input('layer') layer: any;
  @Input('level_id') level_id: int;
  @Input('parent_guid') parent_guid: any;

  constructor(private colorService: ColorbarService, private data: DataService, private sanitizer: DomSanitizer) { }

  getLevelColors(p){
     if (p && this.colors) return this.colors.find(c => c.id == p.level.color_id);

  } 

  update(){
    const prods = JSON.parse(JSON.stringify(this.selectedProducts))
    const map = prods.find(p => p.name == this.parent_guid);
    const layer = map.layers.find(l => l.guid == this.layer.guid)

    map.layersUpdated = moment();
    layer.options.color = {...this.colorOptions}

    this.data.changeMessage({selectedProducts : prods});
  }

  clearThresholds(){
  }

  updateType(){
     this.update()
  }

  updateScale(){
    if (Array.isArray(this.domains)) {
        let xScale = d3.scaleLinear()

        let levs = [...this.domains]
        levs = levs.map(l => parseFloat(l))
        let palette = [...this.palette]

        let min =  parseFloat(this.domains[0]);
        let max =  parseFloat(this.domains[this.domains.length - 1]);
        let s2 = d3.scaleLinear().domain(d3.ticks(0, width, palette.length - 1)).range(palette.map(p => d3.rgb(p)))

      //  if(this.colorDomain.type == "Log") {
      //      s1 = d3.scaleLog().domain([1,width]).range([d3.rgb(leftcolor), d3.rgb(rightcolor)])
      //  }

        let steps= 100;
        levs = d3.range(0, width, (width /steps))

        this.svg.selectAll(".bars").remove();
        let bars     = this.svg.selectAll(".bars").data(levs) 

        const barwidth = width /levs.length
        bars.exit().remove()

        bars.enter().append("rect")
        .attr("class", "bars")
        .attr("x", function(d, i) { return i * barwidth })
        .attr("y", 0)
        .attr("height", height)
        .attr("width",  barwidth + 1)
        .style("fill", function(d, i ) {
             return s2(d);
         })
       
        bars.transition()
        .attr("x", function(d, i) { return i * barwidth })
        .attr("width",  barwidth)
        .style("fill", function(d, i ) { return xScale(d + min); })

        this.xScale = xScale;
      }
  }

  ngAfterViewInit(){
 //   width = document.getElementById("options").offsetWidth - 5;


    let svg = d3.select('#color_' + this.layer.guid)
        .append('svg')
        .attr('width', width)
        .attr('height',height);

    this.svg = svg;
    this.updateScale();
  }

  updatePalette(){
     this.updateScale();
     this.saveBar = true;

  }

  removeColor(i){
    if(!this.previousPalette) this.previousPalette = [...this.palette]

    this.palette.splice(i,1);
    this.saveBar = true;
    this.updateScale();
    this.updateDomainType();
    this.saveBar = true;
  }
 
  updateDomains(){
    this.saveBar = true;
  }

  updateDomainType(){
    if(!this.previousDomains) this.previousDomains = [...this.domains]

    if (this.domainType == "specificDomain") {
       const avg = (parseInt(this.domains[1]) + parseInt(this.domains[0])) / this.palette.length
       let newDomains = this.palette.map((p,i) => return i * avg)
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

  addColor(i){
    if(!this.previousPalette) this.previousPalette = [...this.palette]

    this.palette.splice(i,0,"#ffffff");
    let  nextVal = this.domains[i];

    if(i > 0) nextVal = (parseFloat(this.domains[i-1]) + parseFloat(nextVal)) / 2;

    this.saveBar = true;
    this.updateScale()
    this.updateDomainType()
  }
  
  updateSelected(){
    if(!this.previousSelected) this.previousSelected = this.colorId;
    const color = this.colors.find(c => c.id == this.colorId)
    this.color = color;

    this.updateColorChoice();
    this.updateScale()
    this.saveBar = true;
  }

  saveColorbar(){
    this.saveBar = false;
    this.editColors = false;

    //storing everything as strings
    this.domains = this.domains.map(d => d.toString())
    this.colorService.updateColorbar(this.colorId, this.domains, this.palette, this.layer.guid)
  }
  
  reset(){
    this.palette= this.color.palette.split(",")
    this.domains = this.color.domains.split(",")
    this.colorName = this.level.color_name;
    this.colorId = this.color.id;

    if(this.domains.length ==2) this.domainType = "domainRange"
    this.updateScale();

  }

  cancel(){
    this.saveBar = false;
    this.editColors = false;

  //  if(this.previousSelected){
  //    this.colorId = this.previousSelected;
  //    this.previousSelected = null;
  //  }
  // 
  //  if (this.previousPalette){
  //       this.palette = [...this.previousPalette];
  //       this.previousPalette = null;
  //  }

  //  if (this.previousDomains){
  //    this.domains = [...this.previousDomains];
  //    this.previousDomains = null;
  //    this.updateScale();
  //  }

    if(this.domains.length ==2) this.domainType = "domainRange"

  }


  editColor(evt){

    const color = this.level.color_id; 
    const url = "http://docker.nrlmry.navy.mil:8000/admin/products/colorscale/" + color + "/change/";

    window.open(url, 'C-Sharpcorner', 'toolbar=no,scrollbars=no,resizable=no,top=100,left=' + evt.screenX +',width=800,height=600');
    this.saveBar = true;
  }

  updateColorChoice(){
      console.log("updating color choice")
      const color = this.color;
      this.domains = color.domains.split(",")
      this.palette = color.palette.split(",")
      this.colorId= color.id;
      this.colorName = color.name;

      if(this.domains.length == 2) {
          this.domainType = "domainRange"

      } else {
          this.domainType = "specificDomain"

      }
  }


  indexTrack(index: number, value: any){
     return index;

  }

  ngOnInit() {

    this.level = this.layer.field.levels.find(l => l.plid == this.level_id)
    this.colorOptions = this.layer.options.color ? this.layer.options.color : {"type" : "Linear"}

    this.data.currentMessage.subscribe(state => {
       this.selectedProducts = JSON.parse(JSON.stringify(state.selectedProducts));

       if(JSON.stringify(state.colors) != JSON.stringify(this.colors)) {
           this.colors = JSON.parse(JSON.stringify(state.colors))
           const color = this.colors.find(c => c.id == this.level.color_id)

           if(JSON.stringify(color) != JSON.stringify(this.color)) {
               this.color = color;
               this.updateColorChoice();
           }
      } 
  }

}

