import { Product} from './product';
import * as moment from 'moment'

const basetime = moment().add(-1, "day");
const basetimeStr = basetime.format("YYYYMMDD") + "00";

export const regions =[ 
      {id: 100, name : "Africa",        coordinates: [[-30, 45],  [70, -50]]},
      {id: 102, name : 'Asia',          coordinates: [[10, 80],   [160, 0]]},
      {id: 103, name : 'East Pacific',  coordinates: [[-80,70],   [160,-10]]},
      {id: 104, name : "Global",        coordinates: [[-180, 90], [180, -90]]},
      {id: 105, name : 'Indian Ocean' , coordinates: [[30,40],  [120,-50]]},
      {id: 107, name : "North America", coordinates: [[-145, 70], [-45, 10]]},
      {id: 108, name : "North Atlantic", coordinates: [[-100, 70], [20, 0]]},
      {id: 109, name : "North Pacific", coordinates:  [[-110, 70], [90, -20]]},
      {id: 110, name : "South Pacific", coordinates: [[-110, 20], [90, -80]]},
      {id: 111, name : 'South Atlantic', coordinates: [[-90,20], [60,-80]]},
      {id: 112, name : 'Southeast\n Asia',  coordinates: [[80,40], [170,-20]]},
      {id: 113, name : 'Southwest\n Asia' , coordinates: [[20, 50],  [100,0]]},
      {id: 114, name : 'WestPac' ,       coordinates: [[70, 50],[180, -20]]},
      {id: 115, name : 'North Polar' ,  coordinates: [[-180,90],[180, 40]]},
      {id: 116, name : 'South Polar' ,  coordinates: [[-180,-40],[180, -90]]}
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

