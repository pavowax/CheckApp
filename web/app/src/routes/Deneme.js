import React from 'react'
import { useEffect , useState } from 'react'

const URL = `http://api.weatherapi.com/v1/current.json?key=f954838a7ad145bb842121643232912&q=Istanbul&aqi=no`;

function Deneme() {

    const [temp, setTemp] = useState(0);
    useEffect(() => {
        const fetchData = async () => {
            const result = await fetch(URL)
            result.json().then(json => {
                setTemp(json.current.temp_c);
            })
        }
        fetchData();
    }, []);

  return (
    <div>
      Temp = {temp}
    </div>
  )
}
export default Deneme