import { Circle as CircleStyle, Fill, Text, Stroke, Style } from 'ol/style.js';

export default class Styles {
    static highlightStyle = {
        'Polygon': new Style({
            stroke: new Stroke({
                color: 'GREY',
                lineDash: [4],
                width: 1
            }),
            fill: new Fill({
                color: 'rgba(0,100, 200, 0.2)'
            }),
            text: new Text({
                font: '11px Calibri,sans-serif',
                fill: new Fill({
                    color: '#000'
                }),
                stroke: new Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        })
    }

    static image = new CircleStyle({
        radius: 5,
        fill: null,
        stroke: new Stroke({ color: 'red', width: 1 })
    });

    static styles = {
        'Point': new Style({
            image: Styles.image
        }),
        'Polygon': new Style({
            stroke: new Stroke({
                color: 'GREY',
                lineDash: [4],
                width: 1
            }),
            text: new Text({
                font: '12px Calibri,sans-serif',
                fill: new Fill({
                    color: '#000'
                }),
                stroke: new Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        }),
    };
}
