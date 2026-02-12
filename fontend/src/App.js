import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [symptoms, setSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [infographic, setInfographic] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/categories')
      .then(res => setCategories(res.data.categories))
      .catch(err => console.error("Error fetching categories", err));
  }, []);

  
  const handleCategoryChange = (e) => {
    const cat = e.target.value;
    setSelectedCategory(cat);
    setSelectedSymptoms([]); 
    
    axios.get(`http://127.0.0.1:8000/symptoms/${cat}`)
      .then(res => setSymptoms(res.data.symptoms))
      .catch(err => console.error("Error fetching symptoms", err));
  };

  
  const handleSymptomCheck = (symptom) => {
    if (selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
    } else {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
  };

 
  const getDiagnosis = () => {
    axios.post('http://127.0.0.1:8000/diagnose', 
      { selected_symptoms: selectedSymptoms },
      { responseType: 'blob' } 
    )
    .then(res => {
      const url = URL.createObjectURL(res.data);
      setInfographic(url);
    })
    .catch(err => alert("රෝගය හඳුනා ගැනීමට අපොහොසත් විය."));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🌾 කෘෂි රෝග විනිශ්චය පද්ධතිය</h1>
      
      {/* Category Selection */}
      <div style={{ marginBottom: '20px' }}>
        <label>වගා වර්ගය තෝරන්න: </label>
        <select onChange={handleCategoryChange} value={selectedCategory}>
          <option value="">-- තෝරන්න --</option>
          {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
        </select>
      </div>

      {/* Symptom Checklist */}
      {symptoms.length > 0 && (
        <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px' }}>
          <h3>රෝග ලක්ෂණ තෝරන්න:</h3>
          {symptoms.map(s => (
            <div key={s}>
              <input 
                type="checkbox" 
                onChange={() => handleSymptomCheck(s)}
                checked={selectedSymptoms.includes(s)}
              /> {s}
            </div>
          ))}
          <br/>
          <button onClick={getDiagnosis} style={{ padding: '10px 20px', background: 'green', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
            රෝගය පරීක්ෂා කරන්න
          </button>
        </div>
      )}

      {/* Infographic Result */}
      {infographic && (
        <div style={{ marginTop: '30px' }}>
          <h2>රෝග විනිශ්චය වාර්තාව:</h2>
          <img src={infographic} alt="Diagnosis Result" style={{ maxWidth: '100%', border: '1px solid #ddd' }} />
          <br/>
          <a href={infographic} download="Report.png">
             <button style={{ marginTop: '10px' }}>වාර්තාව බාගත කරන්න (Download)</button>
          </a>
        </div>
      )}
    </div>
  );
}

export default App;