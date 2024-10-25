import { useState } from 'react';

import './AddMeasurement.css';

function AddMeasurement() {
  const [inputs, setInputs] = useState({});
  const [isValidated, setValidated] = useState(false);

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleDbWrite = (event) => {
    event.preventDefault();
    console.log(inputs.sys + "/" + inputs.dia + ":" + inputs.rate)
    fetch("http://localhost:5000/v1/add/hearttrace", {
      method: "post",
      body: JSON.stringify({"sys": inputs.sys, "dia":inputs.dia, "rate":inputs.rate}),
      headers: {'Content-Type': 'application/json'}
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("dia: " + inputs.dia + " sys: " + inputs.sys + " rate: " + inputs.rate)
    if(!isNaN(inputs.dia) && !isNaN(inputs.sys) && !isNaN(inputs.rate)) {
      if (inputs.dia > 0 && inputs.sys > 0 && inputs.rate > 0) {
        setValidated(true)
      } else {
        setValidated(false)
      }
    } else {
      setValidated(false)
    }
  }

  function ValidateButton() {
    if (isValidated) {
      return (<form onSubmit={handleDbWrite}>
        <input 
          type="submit"
          name="atest"
          value={"Daten in DB schreiben"}
          onChange={handleDbWrite}
        />
      </form>)
    } else {
      return <p>bitte sinnvolle Daten eintragen!</p>
    }
  }


  return (
    <div className='inputWidget'>
      <form className='inputForm' onSubmit={handleSubmit}>
      <label>Enter your sys:
        <input 
          type="number"
          name="sys"
          value={inputs.sys || ""}
          onChange={handleChange}
        />
      </label>
      <label>Enter dia:
        <input 
          type="number" 
          name="dia" 
          value={inputs.dia || ""} 
          onChange={handleChange}
        />
        </label>
        <label>Enter rate:
        <input 
          type="number" 
          name="rate" 
          value={inputs.rate || ""} 
          onChange={handleChange}
        />
        </label>
        <input type="submit" />
    </form>


    <div>
      <p>{inputs.username}</p>
    </div>

    <ValidateButton/>



    </div>
  );
}

export default AddMeasurement;
