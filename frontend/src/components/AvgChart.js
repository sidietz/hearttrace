import React, { useState, useEffect } from 'react';

import BillboardChart from 'react-billboardjs';
import 'billboard.js/dist/billboard.css';

import './AvgChart.css';

function AvgChart(props) {

  const DEFAULT_STATE = {        'x': 'x',        columns: []};

  const axis = {
    x: {
      type: 'timeseries',
      tick: {
        format: '%Y-%m-%d',
      },
    },
  }
  
    const [chartData, setChartData] = useState(DEFAULT_STATE);
  
    useEffect(() => {
      fetch('http://127.0.0.1:5000/api/charts/day').then(res => res.json()).then(data => {
        //console.log(data);
        setChartData(data['data']);
        
      });
    }, [props.url]);
  
    return (
      <div>
        {props.datetime === "no"
        ? <BillboardChart data={chartData}></BillboardChart>
        : <BillboardChart data={chartData} axis={axis}></BillboardChart>
      }
          

      </div>
          );
  }

  export default AvgChart;
