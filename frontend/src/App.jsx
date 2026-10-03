import { useState } from "react";
import "./App.css";


function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const analyzeUrl = async () => {
    if (!url.trim()) {
      setError("Please enter a URL.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/analyze/url",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail?.[0]?.msg ||
          "Unable to analyze this URL."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
        "Could not connect to the PhishLens backend."
      );
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="app">

      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">
            P
          </div>

          <div>
            <h1>PhishLens</h1>
            <span>AI Security Scanner</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>


      <main className="main-content">

        <section className="hero">

          <div className="badge">
            AI-POWERED URL PROTECTION
          </div>

          <h2>
            Check before
            <span> you click.</span>
          </h2>

          <p>
            PhishLens AI analyzes suspicious URLs using
            machine learning and security indicators to
            help identify phishing and scam websites.
          </p>


          <div className="scanner-card">

            <label htmlFor="url">
              Enter a URL to analyze
            </label>

            <div className="input-row">

              <input
                id="url"
                type="text"
                placeholder="https://example.com"
                value={url}
                onChange={(event) =>
                  setUrl(event.target.value)
                }
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    analyzeUrl();
                  }
                }}
              />

              <button
                onClick={analyzeUrl}
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze URL"}
              </button>

            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

          </div>

        </section>


        {result && (
          <section className="result-card">

            <div className="result-header">

              <div>
                <p className="result-label">
                  ANALYSIS RESULT
                </p>

                <h3>
                  {result.classification
                    .charAt(0)
                    .toUpperCase() +
                    result.classification.slice(1)}
                </h3>
              </div>

              <div
                className={`risk-score ${result.classification}`}
              >
                <span>Risk Score</span>
                <strong>
                  {result.risk_score}
                </strong>
                <small>/ 100</small>
              </div>

            </div>


            <div className="analyzed-url">
              <span>Analyzed URL</span>
              <code>{result.url}</code>
            </div>


            <div className="probabilities">

              <div className="probability">
                <span>Phishing Probability</span>

                <strong>
                  {(
                    result.phishing_probability * 100
                  ).toFixed(2)}
                  %
                </strong>
              </div>


              <div className="probability">
                <span>Legitimate Probability</span>

                <strong>
                  {(
                    result.legitimate_probability * 100
                  ).toFixed(2)}
                  %
                </strong>
              </div>

            </div>


            {result.indicators.length > 0 && (
              <div className="indicators">

                <h4>
                  Security Indicators
                </h4>

                {result.indicators.map(
                  (indicator, index) => (
                    <div
                      className="indicator"
                      key={index}
                    >
                      <span
                        className={`indicator-dot ${indicator.severity}`}
                      ></span>

                      <div>
                        <strong>
                          {indicator.severity}
                        </strong>

                        <p>
                          {indicator.message}
                        </p>
                      </div>
                    </div>
                  )
                )}

              </div>
            )}

          </section>
        )}


        {!result && !loading && (
          <section className="features">

            <div className="feature">
              <div className="feature-icon">
                AI
              </div>

              <h3>
                Machine Learning
              </h3>

              <p>
                URL features are analyzed by a trained
                phishing detection model.
              </p>
            </div>


            <div className="feature">
              <div className="feature-icon">
                ⚠
              </div>

              <h3>
                Risk Indicators
              </h3>

              <p>
                Detects suspicious patterns such as
                IP addresses, long URLs and risky keywords.
              </p>
            </div>


            <div className="feature">
              <div className="feature-icon">
                ✓
              </div>

              <h3>
                Instant Analysis
              </h3>

              <p>
                Get a classification and risk score
                within seconds.
              </p>
            </div>

          </section>
        )}

      </main>


      <footer>
        <p>
          PhishLens AI · Defensive cybersecurity research
        </p>
      </footer>

    </div>
  );
}


export default App;