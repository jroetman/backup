import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export default class OlSource {

  constructor(private http: HttpClient) { }

  getBackground(){
      return this.http.get("https://nrlmry.navy.mil/aerosol_web/kml/latest_aer_movie.kml")
  }
}
