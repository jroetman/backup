import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'precision'})
export class PrecisionPipe implements PipeTransform {
  transform(value: number[], precision : number): number[] {
       return value.map( v => parseFloat(v.toFixed(precision)))
  }
}

@Pipe({name: 'keys'})
export class KeysPipe implements PipeTransform {
  transform(obj : object): any[] {
       return Object.keys(obj)
  }
}
