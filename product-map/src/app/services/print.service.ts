import { Inject, Injectable } from '@angular/core';
import * as moment from 'moment';

@Injectable()
export class PrintService{

  printDivs(elements) {
    var mywindow = window.open('', 'PRINT', 'height=800,width=1024');
    let title = moment();

    mywindow.document.write('<html><head><title>' + title + '</title>');
    mywindow.document.write('</head><body >');
    mywindow.document.write('<h1>' + title  + '</h1>');
    
    for(let i = 0; i < elements.length; i++) {
        let imgs = elements[i].getElementsByTagName("img")

        for(let p = 0; p < imgs.length; p++) {
            let img = imgs[p];
            mywindow.document.write("<img src='" +img.src + "' width='350px' style='display:inline;' />");
        }
    }
    mywindow.document.write('</body></html>');

    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10*/

    mywindow.print();
    mywindow.close();

    return true;
  }

}
