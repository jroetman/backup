import { Component, OnInit, AfterViewInit, AfterViewChecked, Input } from '@angular/core';
import { DataService } from "../services/data.service";
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
export class ColorbarComponent implements OnInit, AfterViewInit {

  type: string = "Linear";
  colorId : any;
  editColors: boolean = false;
  color : any = {};
  colors: any = [];
  save: boolean =false;
  selectedProductUpdate: any = moment()
  scrolled : boolean = false;

  
  @Input('layer') layer: any;
  @Input('parent_guid') parent_guid: any;

  constructor(private colorService: ColorbarService, private data: DataService) { }

  update(){
    const map = JSON.parse(JSON.stringify(this.map))
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
    let domains = this.color.domains ? this.color.domains.split(",") : null;
    let palette = this.color.palette ? this.color.palette.split(",") : null;

    if(!this.svg)  {
        this.svg = d3.select('#color_' + this.layer.guid)
            .append('svg')
            .attr('width', width)
            .attr('height',height);
    }

    if (Array.isArray(domains) && Array.isArray(palette)) {
        let xScale = d3.scaleLinear()

        let levs = domains;
        levs = levs.map(l => parseFloat(l))
        let min =  parseFloat(domains[0]);
        let max =  parseFloat(domains[domains.length - 1]);
        let s2 = d3.scaleLinear().domain(d3.ticks(0, width, palette.length - 1)).range(palette.map(p => d3.rgb(p)))

      //  if(this.colorDomain.type == "Log") {
      //      s1 = d3.scaleLog().domain([1,width]).range([d3.rgb(leftcolor), d3.rgb(rightcolor)])
      //  }

        let steps= 100;
        levs = d3.range(0, width, (width /steps))

        this.svg.selectAll(".bars").remove();
        let bars  = this.svg.selectAll(".bars").data(levs) 

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

  ngAfterViewChecked(){
    if(!this.scrolled) {
        this.scrolled = this.scrollToColor()
    }
  }

  ngAfterViewInit(){

    let svg = d3.select('#color_' + this.layer.guid)
        .append('svg')
        .attr('width', width)
        .attr('height',height);

    this.svg = svg;
    this.updateScale();
  }

  updateSelected(id){
    const color = {...this.colors.find(c => c.id == id)}
    this.selectedColor = color;
    this.selectedColorId = id
    this.save= true;
    this.edit=false;
   
  }

  createColorbar(){
     let cb = {domains: ["0","100"], id: "new" + Date.now(), name: "New Colorbar", palette: ["#0000FF","#00FF00","#FFFF00","#FF0000","#AA0000"]}
     this.color = cb;
     this.colorId = cb.id;
     this.edit =true

     let plid = this.layer.options ? this.layer.options.level_id : this.layer.field.levels[0].plid
     this.colorService.createColorbar(this.colorId, cb.name, cb.domains, cb.palette, this.map, this.layer, plid)
     
  }


  deleteColor(c){
    if(confirm("Remove Colorbar?")) {
       this.colorService.removeColorbar(c.id) 
    }
  }

  editColor(c){
    this.selectedColor = {...c}
    this.edit = true
  }

  saveSelection(){
    this.save = false;

  }

  cancelEdit(){
    this.edit = false
    this.selectedColor = this.color
  }


  saveSelection(){
    let plid = this.layer.options ? this.layer.options.level_id : this.layer.field.levels[0].plid
    this.colorService.assignColorbar(this.selectedColor.id, plid, this.layer, this.map)
    
    this.color = {...this.selectedColor}
    this.colorId = this.color.id
    this.updateScale();
  }

  cancel(){
    this.save = false;
    this.editColors = false;
    this.scrolled = false;
    this.selectedColor = this.color
    this.selectedColorId = this.color.id
    //this.updateColorChoice()
  }

  scrollToColor(){
    const sel = document.getElementById("color_" + this.colorId)
    if (sel) {
       var top = sel.offsetTop;
       sel.parentNode.scrollTop = top -50;
       return true
    }
    return false
  }


  ngOnInit() {

    this.level = this.layer.field.levels.find(l => l.plid == this.layer.options.level_id)
    this.colorOptions = this.layer.options.color ? this.layer.options.color : {"type" : "Linear"}

    this.data.currentMessage.subscribe(state => {
       if (!this.selectedProductUpdate.isSame(state.selectedProductUpdate){
           this.selectedProducts = JSON.parse(JSON.stringify(state.selectedProducts));
           this.selectedProductUpdate = moment(state.selectedProductUpdate)
           this.map = this.selectedProducts.find(p => p.name == this.parent_guid);

          // this.level = this.layer.field.levels.find(l => l.plid == this.layer.options.level_id)
          // const color = {...this.colors.find(c => c.id == this.level.color_id)}
          // this.color = color;
          // this.colorId = color.id;
           this.updateScale();
           this.selectedColor = this.color;
           this.selectedColorId = this.color.id;


       } 

       if(state.colors && JSON.stringify(state.colors) != JSON.stringify(this.colors)) {
           this.colors = JSON.parse(JSON.stringify(state.colors))
           let color = {...this.colors.find(c => c.id == this.level.color_id)}

           if(JSON.stringify(color) != JSON.stringify(this.color)) {
               this.color = color;
               this.colorId = color.id;
               this.updateScale();
               this.selectedColor = this.color;
               this.selectedColorId = this.color.id;
           }
      } 
  }

}

