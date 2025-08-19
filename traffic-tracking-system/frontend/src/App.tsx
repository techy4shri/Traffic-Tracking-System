import { useState } from 'react'
import FileUpload from './components/FileUpload/FileUpload'
import Footer from './components/Footer/Footer'
import Background from './components/Background/Background'
import type { ProcessedResult } from './types/common'
import './App.css'

function App() {
  const [result, setResult] = useState<ProcessedResult | null>(null);
  const [isProcessing] = useState(false);

  return (
    <div className="app-container">
      {!isProcessing && <Background />}
      <main className="main-content">
        <h1 className="title">Traffic Tracking System</h1>
        <FileUpload onProcessed={setResult} />
        {result && (
          <div className="result-section">
            <h2>Analysis Results</h2>
            <p>Vehicles Detected: {result.vehicleCount}</p>
            <div className="vehicles-grid">
              {result.vehicleNumbers.map((number, index) => (
                <p key={index} className="vehicle-item">
                  Vehicle {index + 1}: {number}
                </p>
              ))}
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

export default App
