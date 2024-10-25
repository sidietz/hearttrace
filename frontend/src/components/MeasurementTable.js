import React, { useState, useEffect } from 'react';

import BillboardChart from 'react-billboardjs';
import 'billboard.js/dist/billboard.css';

import './MeasurementTable.css';

function AvgChart({props}) {

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    console.log("URL: " + props.url)
    fetch(props.url).then(res => res.json()).then(data => {
      console.log(data);
      setChartData(data);

    });
  }, [props]);

  return (
    <div>
      <h3>Messwerte</h3>

      <tbody>
        {
          chartData.forEach(element => {
            return (<tr>
              <td>{element[1]}</td>
              <td>{element[1]}</td>
              <td>{element[1]}</td>
            </tr>)
          })}

        {chartData.map(item =>
          <tr>
            <td>{item[1]}</td>
            <td>{item[2]}</td>
            <td>{item[3]}</td>
            <td>{item[4]}</td>
          </tr>)}



      </tbody>


    </div>
  );
}

export default AvgChart;
