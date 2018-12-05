import { Product} from './product';
import * as moment from 'moment'

const basetime = moment().add(-1, "day");
const basetimeStr = basetime.format("YYYYMMDD") + "00";

export const regions =[ 
      {id: 123, name : "Global" ,       coordinates: [[-180, 90], [180, -90]]},
      {id: 124, name : "South America", coordinates: [[-100, 20], [-20, -50]]},
      {id: 125, name : "North America", coordinates: [[-165, 70], [-55, 15]]},
      {id: 126, name : "Byzantium",     coordinates: [[-20, 65],  [80, -5]]},
      {id: 127, name : 'Sbtropatl',     coordinates: [[-100, 60], [30, -5]]},
      {id: 128, name : 'Niosea',        coordinates: [[40,36],   [131,-15]]},
      {id: 129, name : 'Eastasia',      coordinates: [[70,76],    [171,15]]},
      {id: 130, name : 'Pacific',       coordinates: [[95,76],    [265,15]]},
      {id: 131, name : 'Conus' ,        coordinates: [[-150,66],   [-49,0]]},
      {id: 132, name : 'Satlantic' ,    coordinates: [[-90,11],  [61,-60]]},
      {id: 133, name : 'Sioaus' ,       coordinates: [[0, 11],[180, -60]]},
      {id: 134, name : 'npolar' ,       coordinates: [[-180,90],[180, 45]]}
]


function generateImages(prefix, suffix, interval) {
    const res=[];

    let m = moment(basetime).startOf("day");
    let path = ""
    let ct = moment(m)
    let sf = suffix;

    let numhours = 0;
    while(m.isSameOrBefore(moment(basetime).add(48, "hours"))){

      path = prefix + basetimeStr + "/" + basetimeStr + "_";
      path += ct.format("YYYYMMDDHH");

      if(suffix.includes("_f000")){
         sf= suffix.replace("_f000", ("_f" + (("00" + numhours).slice(-3))))
      }
      path += sf;
      let time = moment(ct).add(ct.utcOffset(),"minutes").toISOString()
      res.push({path: path, time : time})

      numhours += interval;

      ct = moment(m).add(interval, "hours");
      m.add(interval,"hours");
     }
     return res;
}

function generateMetar(){
  fetch("http://localhost:5000/metar/available").then(res =>{
     return res.json();
  }).then(json => {
     return json.data;
  })
}

export const PRODUCTS = []
//    { id: 300,
//      name: 'NAAPS',
//      location: regions.global,
//      fields : [{name : 'aod', label:'Aerosol Optical Depth', species : ['dust_aod', 'seasalt_aod']},
//                {name:  'sfc', label:'Surface', species : ['dust_sfc', 'seasalt_sfc']}],
//      images : {url : 'http://localhost:5000/'},
//      parentEntity: "ICAP MME"
//    },
//    { id: 100,
//      name: 'metar',
//      location: regions.global,
//      images : {url : 'http://localhost:5000/metar/available'},
//      parentEntity: "Metar"
//    },
//    { id: 15,
//      name: 'TOTAL Aerosol Optical Depth at 550nm',
//      location: {regionName: "niosea", type: "envelope", coordinates: [[40,35], [130, 15]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/niosea/", "_f000_total_aod_550_niosea_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 16,
//      name: 'Seasalt Aerosol Optical Depth at 550nm',
//      location: {regionName: "niosea", type: "envelope", coordinates: [[40,35], [130, 15]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/niosea/", "_f000_seasalt_aod_550_niosea_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 17,
//      name: 'Smoke Aerosol Optical Depth at 550nm',
//      location: {regionName: "niosea", type: "envelope", coordinates: [[40,35], [130, 15]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/niosea/", "_f000_smoke_aod_550_niosea_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 18,
//      name: 'Dust Aerosol Optical Depth at 550nm',
//      location: {regionName: "niosea", type: "envelope", coordinates: [[40,35], [130, 15]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/niosea/", "_f000_dust_aod_550_niosea_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 19,
//      name: 'Sulfate Aerosol Optical Depth at 550nm',
//      location: {regionName: "niosea", type: "envelope", coordinates: [[40,35], [130, 15]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/niosea/", "_f000_sulfate_aod_550_niosea_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 10,
//      name: 'TOTAL Aerosol Optical Depth at 550nm',
//      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/global/", "_f000_total_aod_550_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 11,
//      name: 'Seasalt Aerosol Optical Depth at 550nm',
//      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/global/", "_f000_seasalt_aod_550_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 12,
//      name: 'Smoke Aerosol Optical Depth at 550nm',
//      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/global/", "_f000_smoke_aod_550_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 13,
//      name: 'Dust Aerosol Optical Depth at 550nm',
//      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/global/", "_f000_dust_aod_550_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 14,
//      name: 'Sulfate Aerosol Optical Depth at 550nm',
//      location: {regionName: "Global", type: "envelope", coordinates: [[-170, 70], [170, -70]]},
//      images : generateImages("https://www.nrlmry.navy.mil/aerosol/globaer/icap_01/global/", "_f000_sulfate_aod_550_icap.png",6),
//      parentEntity: "ICAP MME"
//    },
//    { id: 1,
//      name: 'sfc. Obs',
//      location: {regionName: "North America", type: "envelope", coordinates: [[-165, 15], [-55, 70]]},
//      images : [{path: "", type: "static", time: moment()}],
//      parentEntity: "Visibility-Reducing Surface Weather Reports"
//    },
//    { id: 1,
//      name: 'sfc. Obs',
//      location: {regionName: "Sahara ", type: "envelope", coordinates: [[-20, 40], [40, 5]]},
//      images : [{path: "test", type: "static", time: moment()}],
//      parentEntity: "Visibility-Reducing Surface Weather Reports"
//    },
//    { id: 1,
//      name: 'sfc. Obs',
//      location: {regionName: "Sahel", type: "envelope", coordinates: [[-15, 20], [15, 5]]},
//      images : [{path: "test", type: "static", time: moment()}],
//      parentEntity: "Visibility-Reducing Surface Weather Reports"
//    },
//    { id: 2,
//      name: 'Dust over South America',
//      location: {regionName: "South America", type: "envelope", coordinates: [[-95, -5], [-50, 30]]},
//      images: [{path: "test", type: "static", time: moment()}],
//      parentEntity: "Visibility-Reducing Surface Weather Reports"
//    }

