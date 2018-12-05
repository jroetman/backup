import { Inject, Injectable } from '@angular/core';
import { intersects} from "ol/extent";
import { DataService } from "./data.service";
import { boundingExtent, containsExtent} from "ol/extent";
import * as moment from 'moment';


@Injectable()
export class ProductService {

    constructor(private data: DataService){}

    getRegionTree() {
        const ms = this.data.getMessageSource().getValue();
        const prods = ms.products;
        const extent = ms.extent;
        const searchView = ms.searchView;
        const searchFilter = ms.searchfilter;

        if( prods && prods.length > 0) {
            let filtered = filterByExtent(prods, extent)
            let rt = [];

            if(searchFilter && searchFilter != "" && searchView == "product"){
                filtered = filterBySearch(filtered, searchFilter) 
                filtered = filterByVar(filtered, searchFilter) 
            }

            if(searchView == 'product') rt = buildRegionTree(filtered)
            if(searchView == 'species') rt = buildSpeciesTree(filtered, searchFilter)
            if(searchView == 'observations') rt = buildSpeciesTree(filtered, searchFilter)
            this.data.changeMessage({regionTreeUpdated: moment(), regionTree: rt});
        }

        //update selectedProducts, make everything uniform
        //if((JSON.stringify(m.selectedProducts) != JSON.stringify(prevMessage.selectedProducts))
        //   || !moment(m.currentDtg).isSame(moment(prevMessage.currentDtg)) ) {
        //      
        //      await Promise.all(m.selectedProducts.map(async (p) =>{
        //           const prod = m.products.find(pr => pr.id == p.id)

        //           if(prod && prod.imageUrl) {
        //             let params = {};

        //             if(prod.imageParams){ 
        //                 params = {...prod.imageParams}
        //                 params.field = p.field.varname;
        //                 params.dtg  = moment(m.currentDtg).format("YYYYMMDDHH")
        //                 params = Object.keys(params).map(o => "&" + o + "=" + params[o]).join("")
        //             }
        //             
        //             const res  = await fetch(prod.imageUrl + "?" + params)
        //             const json = await res.json();
        //             prod.images = json;
        //             if(json.options) prod.options = json.options;
        //           }
        //           if(!prod.selectedOptions) prod.selectedOptions = [];
        //      }))
        //      m.selectedProductUpdate = moment();
        //}
    }
  
    getProducts() {
        const prods = [];

        fetch("http://docker.nrlmry.navy.mil:5000/icap/getProducts").then(res =>{
            return res.json();

        }).then(json => {
           let prods = [];
           let np = {};
           
           Object.keys(json).forEach(model => {
                const  m = json[model] 
                console.log(m)
                const fields = m.fields.sort((a,b) => {
                   if (a.alias < b.alias) return -1
                   if (a.alias > b.alias) return 1
                   return 0;
                })

                np = {id: m.name,
                      name : m.alias,
                      model: m.name,
                      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
                      fields: fields,
                      imageUrl:'http://docker.nrlmry.navy.mil:5000/available',
                      imageParams: {model : m.name, dtg : ""},
                      images : [],
                      parentEntity: "ICAP",
                      fieldType : 'discover',
                      colors: m.colors
                }
                prods.push(np)

           })
        this.data.changeMessage({productsUpdate: moment(), products : prods});
       
     })
  }


  async getAvailability(prod){
      const m = this.data.getMessageSource().getValue();

      if(prod && prod.imageUrl) {
          let params = {};
          if(prod.imageParams){ 
              params = {...prod.imageParams}
              params.dtg  = moment(m.currentDtg).format("YYYYMMDDHH")
              params = Object.keys(params).map(o => "&" + o + "=" + params[o]).join("")
          }
          
          const res  = await fetch(prod.imageUrl + "?" + params)
          const json = await res.json();
          prod.images = json;
          if(json.options) prod.options = json.options;
          if(!prod.selectedOptions) prod.selectedOptions = [];
      }

  }
}

const buildSpeciesTree = (products, searchFilter) => {
  var species  = {};
  var rt = [];
  products.map((p) =>{
     p.fields && p.fields.map(f =>{
             f.species && f.species.map(s => {
                 let spec = s.toLowerCase();

                 if(searchFilter == "" ||  spec.includes(searchFilter.toLowerCase()) {   
                     if(spec.includes(f.name.toLowerCase())) spec = spec.replace(f.name.toLowerCase(), "")
                     spec = spec.replace("_", "")

                     if(!species[spec]) species[spec]= {products: [], nativeName: s, name: spec, pid: p.id, field: f.name,  region: p.location.regionName , ext : p.location.coordinates}
                     species[spec].products.push(p)
                 }
         })
     }) 
  })

  let res =  Object.keys(species).map(k => species[k])
  res.sort((a,b) => {
     if (a.name > b.name) return 1
     if (a.name < b.name) return -1 
     return 0
  });

  return res;
}

const buildRegionTree = (products) => {
  var regions = {};
  var rt = [];

  products.map((p) =>{
     regions[p.location.regionName] = {entities: [], name : p.location.regionName , ext : p.location.coordinates}
  })

  products.map((p) =>{
     if(!regions[p.location.regionName].entities[p.parentEntity]) {
         regions[p.location.regionName].entities[p.parentEntity] = {products: []};
     }
     regions[p.location.regionName].entities[p.parentEntity].products.push(p)
  });

  return Object.keys(regions).map(k => regions[k]);
}

const filterByExtent = (products, extent) => {

    return products.filter(p =>{
       let region =[].concat.apply([], p.location.coordinates)
       let be = boundingExtent(region)
       return containsExtent(be, boundingExtent(extent))
    })
}

const filterBySearch = (products, text) =>{
  return  products.filter((p) =>{
         let res = false;
         let name = null;

         if(p.fields) {
            p.fields.forEach(f => {
              let vv = f.vars.find(v => {
                   name = v;
                   if(v.name) name = v.name
                   return  name.toLowerCase().includes(text.toLowerCase())
               })
               if(vv) res = true
            })
         }
         res = res ||  p.name.toLowerCase().includes(text.toLowerCase())
         return res;         
  })
}

const filterByVar = (products, text) =>{
  
  const prods = JSON.parse(JSON.stringify(products))

  prods.forEach((p) =>{
      if(p.fields) {
         p.fields.forEach(f => {
           let vars = f.vars.filter(v => {
                name = v;
                if(v.name) name = v.name
                return  name.toLowerCase().includes(text.toLowerCase())
            })
            if(vars.length > 0) f.vars = vars
         })
      }
  })
  return prods
}
