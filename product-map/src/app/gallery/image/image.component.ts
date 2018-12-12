import { Component, OnInit, SimpleChanges, OnChanges, Input, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.scss']
})
export class ImageComponent implements OnInit, OnDestroy {

  @Input('product') product: any;
  @Input('numImages') numImages: int; 
  @Input('src') product: any;
  @Input('extent')  extent: [];
  @Input('dtg')  dtg: moment;
  @Input('tau')  tau: any;
  @Input('imageLoading')  imageLoading: any = false;

  constructor() { }

  ngOnInit() {
      this.loadImage()

  }

  ngOnDestroy(){
    clearInterval(this.checkLoad)

  }
  
  ngOnChanges(changes: SimpleChanges) {
      const po = changes.product ? changes.product.previousValue : {};
      const pn = changes.product ? changes.product.currentValue : {};
      const ext = changes.extent ? changes.extent : {};

      if(this.loadImage) {
          if (changes.tau && changes.tau.currentValue != changes.tau.previousValue) {
              this.loadImage()

          } else if (JSON.stringify(ext.currentValue) != JSON.stringify(ext.previousValue))  {
              this.loadImage()

          } else if (changes.dtg && !changes.dtg.currentValue.isSame(changes.dtg.previousValue))  {
              this.loadImage()

          } else if (pn.layersUpdated != po.layersUpdated) {
               this.loadImage()
          }
      }
  }

  loadImage(){
      let p = this.product

      let e = this.extent
      const ext = e[0] + "," + e[3] + "," + e[2] + "," + e[1];
      const img = new Image();

      //Get what we need from each layer
      if (p.layers.length > 0){ 
          const layers = p.layers.map(l =>{
             return {model: l.model, options: l.options, field : {varname: l.field.varname}} 
             
          });
          
          this.imageLoading = true;
          
          
          let newsrc = "http://docker.nrlmry.navy.mil:5000/icap/plotNetcdf?mapName=" + p.name + "&layers=" + JSON.stringify(layers) + "&extent=" + ext + "&hour=" + this.tau + "&dtg=" + (this.dtg.format("YYYYMMDD") + "00" + "&nocache=" + Date.now()) 

          this.src = newsrc;

          if(!this.checkLoad)  {
              this.checkLoad = setInterval(() => {
                 const pe = document.getElementById(this.product.name)

                 let iscomplete = true;
                 if(pe != null) iscomplete = pe.complete;

                 if(iscomplete) {
                    clearInterval(this.checkLoad)
                    if(this.imageLoading != false) this.imageLoading = false;
                    this.checkLoad = null;
                 }

              }, 500)
          }
      }
}
