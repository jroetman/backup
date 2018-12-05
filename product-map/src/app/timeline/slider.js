import * as moment from "moment";

export default function addSlider(props){
      const {d3, svg, currentDtg} = props;

      var slider = svg.append('g')
          .attr("class", "slider")
          .attr("transform", "translate(" + props.margins.left + "," + (0) + ")")
          .call(d3.drag().on('drag', dragged)
                         .on('end', dragend));

      var line = slider.append("line")
          .attr('y1', props.margins.top)
          .attr('y2', props.height - props.margins.bottom)
          .attr('x2', 0)

      var handle = slider.append("rect")
          .attr('y', props.margins.top + (props.height * .25))
          .attr('x', -10)  //(props.height - props.margins.bottom) - (props.height * .25))
          .attr('width', 20)
          .attr('height', 35)
          .attr('class', "handle")

      function dragged(d) {
          var x = Math.min(Math.max(d3.event.x, 0), props.width);
          if(x <= props.margins.left) x = props.margins.left;
          d3.select('.slider').attr('transform', translate(x, 0));
      }

      function dragend(d) {
           var x = d3.event.x - props.margins.left;// Math.min(Math.max(d3.event.x, 0), props.width);
           let value = moment(props.xScale.invert(x))
           let res = moment(value).startOf("hour")
           
           if(res.hour() % 6 <= 3) res = moment(res).add(-res.hour() % 6, 'hours')
           if(res.hour() % 6 > 3)  res = moment(res).add(6 - (res.hour() % 6), 'hours')
           props.updateTime(res)
      }

      function translate(x, y) {
          return 'translate(' + x + ',' + y + ')';
      }

}
