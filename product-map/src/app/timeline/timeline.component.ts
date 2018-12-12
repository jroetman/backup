import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import { DataService } from "../services/data.service";
import { PrintService} from "../services/print.service";
import * as d3 from "d3";
//Don't use Shadow DOM. This will allow us to apply styles to d3 rendered elements, since angular isn't doing it.
import {ViewEncapsulation} from '@angular/core';
import slider from './slider';

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss']
})
export class TimelineComponent implements OnInit {
  selectedProducts: any[] = [];
  selectedProductUpdate: moment;
  currentTau =  0;
  currentDtg: moment = moment().startOf("day");
  forecastHours: 120;
  times: any = {times : [], min : moment(), max : moment().add(24, "hours")};
  taus: any[] = [[moment(), moment().add(6, "hours")]];
  width: 800;
  plotMargins: any  = { top: 5, bottom: 20, left: 220, right: 30 };
  height  = 150;
  plotWidth: number;
  plotHeight: number;
  svg: any;
  xScale: any;
  yScale: any;
  xAxis: any;
  yAxis: any;
  isPlaying: false;


  constructor(private data: DataService, private printService: PrintService) { }

  togglePlay(){
       this.isPlaying = !this.isPlaying;
       if(this.isPlaying) {
           this.playInterval = setInterval(()=>{
              this.nextTau()
           }, 1000)

       } else {
           clearInterval(this.playInterval)

       }
  }
   
  updateDate(evt) {
    this.data.changeMessage({currentDtg: moment(evt.target.value, "YYYY-MM-DD")})

  }

  nextTau(){
    let nt =this.currentTau + 6;
    if(nt > 120) nt = 0;
    this.data.changeMessage({currentTau : nt})
  }

  prevTau(){
    let nt =this.currentTau - 6;
    if(nt < 0) nt = 120;
    this.data.changeMessage({currentTau : nt})
  }

  getAllTimes(){
    const results = [];
    const tauArray = [];
    const names = [];

    this.selectedProducts.map((sp, idx) =>{
       if(sp.layers.length > 0) {
           const p = sp.layers[0];
           const prod = this.products.find(pr => pr.id == p.id )
           let valid = false;

           this.tickVals.map(tv => {
             valid = false;
             let imidx = prod.images.findIndex(i => {
               return moment(i.time).isSame(tv)
             })
             if(imidx >= 0) valid = true;

             results.push({name: prod.name + " " + p.field.alias,idx: idx, tau : tv, valid : valid, guid : p.guid})
           })
           names.push({guid: p.guid, name: prod.name + " " + p.field.alias, field: p.field, specie:p.species, id: p.id})
       }
    })

     
    return {selected: names , times : [...results]};
  }

  updateTimeline() {

    let tc = document.getElementById('timelineContainer').parentNode.parentNode.parentNode;
    this.width = window.innerWidth - (window.innerWidth * .20);
    tc.getElementsByTagName("svg")[0].style.width = this.width; 

    this.times = this.getAllTimes();
    this.updateXscale();

    this.plotWidth  = this.width  - this.plotMargins.left - this.plotMargins.right;
    this.plotHeight = this.height - this.plotMargins.top  - this.plotMargins.bottom;

    this.svg.select(".x.axis").call(this.xAxis)
    this.svg.selectAll(".tick line").attr("stroke-dasharray" : "1,1").attr("y2" : -this.plotHeight)

    this.yScale.domain(this.times.selected.map((s,idx) => s.guid))
    .range(this.selectedProducts.map((p, idx) => this.plotHeight -10 - (idx * 20)));

    this.yAxis.tickValues(this.times.selected.map((s,idx) => s.name + "_" + idx))

    this.svg.select(".y.axis").call(this.yAxis);

    const yScale = this.yScale;
    const color  = this.color;
    const plotMargins = this.plotMargins;
    const xScale = this.xScale;

    let circs = this.svgTaus.selectAll("circle").data(this.times.times);
    circs.exit().remove();

    circs.enter()
      .append("circle")
      .attr("class", "tauCircle")
      .attr("r", 5)
      .attr("cx",function(d){ return xScale(d.tau)})
      .attr("cy", function(d) {
           return yScale(d.guid)
       })
      .style("fill", function(d){
      return d.valid ? "green" : "red" 
      })
      .attr("transform", function(d) {
         return `translate(${plotMargins.left},${0})`
      });

      //Updates to circles
      circs.transition()
         .duration(500)
         .attr("cx",function(d){ return xScale(d.tau)})
         .attr("cy", function(d, idx) {
            return yScale(d.guid)
           })
         .style("fill", function(d){
         return d.valid ? "green" : "red" 
         });

     this.updateSlider();
  }

  clearTaus(){
     d3.selectAll(".tauCircle").remove();
  }

  updateSlider(){
    let x = this.xScale(moment(this.currentDtg).add(this.currentTau, "hours"));
    this.svg.select(".slider")
    .transition(500)
    .attr("transform", "translate(" + (this.plotMargins.left + x) + ",0)")

  }

  updateXscale(){
    
    let tv = [];
    for(let i =0; i < 21; i++) {
      tv.push(moment(this.currentDtg).add(i * 6, "hours"))
    }
    this.tickVals = tv;
    this.xScale.domain([this.currentDtg, moment(this.currentDtg).add(120, "hours")])
    this.xAxis.tickValues(this.tickVals)
    this.xScale.range([0, this.plotWidth]);
    this.xAxis.scale(this.xScale)

  }

  print(){
    this.printService.printDivs(document.getElementsByClassName("imgcontainer"))

  }

  ngOnInit() {
    this.width =document.getElementById("timelineContainer").offsetWidth;
    this.plotWidth  = this.width  - this.plotMargins.left - this.plotMargins.right;
    this.plotHeight = this.height - this.plotMargins.top  - this.plotMargins.bottom;
    const margins = this.plotMargins;


    var color = d3.scaleLinear().domain([0, 10]).range(["green",  "blue", "orange"]);
    // Define filter conditions
    let svg = d3.select('#timelineContainer')
        .append('svg')
        .attr('width', this.width)
        .attr('height',this.height);

    let plotGroup = svg.append('g')
        .classed('plot', true)
        .attr('transform', `translate(${margins.left},${margins.top})`);

    let svgTaus = svg.append("g");
    this.xScale = d3.scaleTime();
    this.xAxis  = d3.axisBottom(this.xScale);


    let xAxisGroup = plotGroup.append('g')
        .classed('x', true)
        .classed('axis', true)
        .attr('transform', `translate(${0},${this.plotHeight})`)
        .call(this.xAxis);


    let yScale = d3.scaleOrdinal();
        yScale.domain(["nothing selected"])
              .range([this.plotHeight -10, 0 ]);

    let yAxis = d3.axisLeft(yScale);

    yAxis.tickPadding(10)

    let yAxisGroup = plotGroup.append('g')
        .classed('y', true)
        .classed('axis', true)
        .call(yAxis);

    slider({ xScale: this.xScale,
           updateTime: (time) => {
                let tau =  time.diff(this.currentDtg, "hours")
                if(tau < 0)   tau  = 0; 
                if(tau  > 120) tau =  120;
            
                this.data.changeMessage({currentTau: tau})
                //in case the tau doesn't change
                this.updateSlider(); 
            },
           d3: d3,
           currentDtg: this.currentDtg,
           svg : svg,
           margins: margins,
           width:this.width,
           height: this.height})

    this.svgTaus = svgTaus;
    this.color = color;
    this.svg = svg;
    this.yAxis = yAxis;
    this.yScale = yScale;
    
    this.updateTimeline();

    this.data.currentMessage.subscribe(state => {

           if(!moment(this.currentDtg).isSame(moment(state.currentDtg))) {
                this.currentDtg = moment(state.currentDtg);
                this.clearTaus();
                this.updateTimeline();
           }

           if(!moment(state.selectedProductUpdate).isSame((this.selectedProductUpdate))) {
               this.currentTau = state.currentTau;

               this.selectedProducts = state.selectedProducts;
               this.products  = state.products;

               this.selectedProductUpdate = moment(state.selectedProductUpdate);
               this.updateTimeline();
           }


           if(this.currentTau != state.currentTau) {
                this.currentTau= state.currentTau;
                this.updateSlider();
           }
           
      });
    }
}
