import { useState } from 'react'
import axios from 'axios'

function App() {
  const [explanedDiseases, setExplanedDiseases] = useState(null)

  const getShap = () => {
    axios.get('http://127.0.0.1:5000/shap').then(({data}) => {
      setExplanedDiseases(data)
    })
  }

  return (
    <>
      <button onClick={getShap}>Get SHAP</button>
      {explanedDiseases && Object.keys(explanedDiseases.data).map((key, index) => {
        console.log(key)
        return (
          <img src={explanedDiseases.data[key]}></img>
        )
      })}
    </>
  )
}

export default App
