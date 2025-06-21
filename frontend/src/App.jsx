import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';

function App() {
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">GI Tech</div>
      </header>

      <main>
        {/* <section className="hero">
          <h1>Get The Loan Details. Right Now</h1>
          <p>Free</p>
          <div className="search-bar">
            <input type="text" placeholder=''></input>
            <button>Search</button>
          </div>
        </section> */}

        <button className="support-button" onClick={handleSupportClick}>
          Talk to an Agent!
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
