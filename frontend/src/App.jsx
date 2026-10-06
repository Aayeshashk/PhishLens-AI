import { useEffect, useMemo, useState } from "react";



import "./App.css";







const API_URL = "https://phishlens-ai-ljq9.onrender.com/api/v1/analyze/url";






const pipelineSteps = [



  {



    number: "01",



    title: "URL Signal",



    detail: "Structural analysis",



  },



  {



    number: "02",



    title: "Feature Extraction",



    detail: "34+ URL signals",



  },



  {



    number: "03",



    title: "Robust LR",



    detail: "ML classification",



  },



  {



    number: "04",



    title: "Risk Engine",



    detail: "Security indicators",



  },



];







const sensitiveWords = [



  "login",



  "signin",



  "verify",



  "verification",



  "secure",



  "account",



  "update",



  "password",



  "bank",



  "confirm",



  "authenticate",



  "credential",



  "wallet",



  "payment",



];







const featureCards = [



  {



    number: "01",



    icon: "◇",



    title: "Machine Learning",



    description:



      "A trained classification model examines structural URL characteristics to estimate phishing probability.",



    footer: "ML ENGINE",



  },



  {



    number: "02",



    icon: "✧",



    title: "Risk Intelligence",



    description:



      "Security rules detect suspicious patterns including IP addresses, sensitive keywords and unusual URL structures.",



    footer: "RISK ENGINE",



    featured: true,



  },



  {



    number: "03",



    icon: "⌁",



    title: "Explainable Results",



    description:



      "Every analysis returns a risk score, probabilities and readable security indicators.",



    footer: "EXPLAINABILITY",



  },



];







function App() {



  const [theme, setTheme] = useState("dark");



  const [url, setUrl] = useState("");



  const [result, setResult] = useState(null);



  const [error, setError] = useState("");



  const [loading, setLoading] = useState(false);



  const [pipelineStage, setPipelineStage] = useState(0);



  const [scanHistory, setScanHistory] = useState([]);







  const isLight = theme === "light";







  useEffect(() => {



    try {



      const savedHistory = localStorage.getItem(



        "phishlens_scan_history"



      );







      if (savedHistory) {



        const parsedHistory = JSON.parse(savedHistory);







        if (Array.isArray(parsedHistory)) {



          setScanHistory(parsedHistory);



        }



      }



    } catch (storageError) {



      console.error(



        "Failed to load scan history:",



        storageError



      );



    }



  }, []);







  const signalProfile = useMemo(() => {



    if (!url) {



      return [



        ["HTTPS", 0],



        ["URL length", 0],



        ["Path depth", 0],



        ["Subdomains", 0],



        ["Query params", 0],



        ["Sensitive terms", 0],



      ];



    }







    try {



      const parsed = new URL(url);







      const hostnameParts = parsed.hostname



        .split(".")



        .filter(Boolean);







      const subdomainCount = Math.max(



        0,



        hostnameParts.length - 2



      );







      const pathParts = parsed.pathname



        .split("/")



        .filter(Boolean);







      const lowerUrl = url.toLowerCase();







      const sensitiveCount = sensitiveWords.filter(



        (word) => lowerUrl.includes(word)



      ).length;







      const queryCount = parsed.search



        ? parsed.search



            .slice(1)



            .split("&")



            .filter(Boolean).length



        : 0;







      return [



        [



          "HTTPS",



          parsed.protocol === "https:" ? 100 : 0,



        ],



        [



          "URL length",



          Math.min(



            100,



            Math.round((url.length / 120) * 100)



          ),



        ],



        [



          "Path depth",



          Math.min(100, pathParts.length * 20),



        ],



        [



          "Subdomains",



          Math.min(100, subdomainCount * 25),



        ],



        [



          "Query params",



          Math.min(100, queryCount * 20),



        ],



        [



          "Sensitive terms",



          Math.min(100, sensitiveCount * 20),



        ],



      ];



    } catch {



      return [



        ["HTTPS", 0],



        ["URL length", 0],



        ["Path depth", 0],



        ["Subdomains", 0],



        ["Query params", 0],



        ["Sensitive terms", 0],



      ];



    }



  }, [url]);







  const resultTone =



    result?.classification === "phishing"



      ? "phishing"



      : result?.classification === "suspicious"



        ? "suspicious"



        : "safe";







  const riskProgress = result



    ? Math.max(



        0,



        Math.min(100, result.risk_score)



      )



    : 0;







  const phishingProbability = result



    ? Math.round(result.phishing_probability * 100)



    : 0;







  const legitimateProbability = result



    ? Math.round(result.legitimate_probability * 100)



    : 0;







  const decisionContent = useMemo(() => {



    if (!result) {



      return null;



    }







    if (result.classification === "phishing") {



      return {



        eyebrow: "HIGH-RISK DECISION",



        title: "Do not interact with this URL.",



        description:



          "The analysis found strong characteristics associated with phishing activity. Avoid entering passwords, payment information or other sensitive data.",



        action:



          "Do not open the link or provide credentials.",



        icon: "!",



      };



    }







    if (result.classification === "suspicious") {



      return {



        eyebrow: "CAUTION REQUIRED",



        title: "Treat this URL with caution.",



        description:



          "The URL contains patterns that increase its risk profile. Verify the destination independently before continuing.",



        action:



          "Verify the domain before interacting with it.",



        icon: "!",



      };



    }







    return {



      eyebrow: "LOW-RISK DECISION",



      title: "No significant threat was detected.",



      description:



        "The URL passed the configured phishing classification and security-indicator checks. Normal caution is still recommended when visiting unfamiliar links.",



      action:



        "Proceed only if you recognize and trust the destination.",



      icon: "✓",



    };



  }, [result]);







  const scrollToScanner = () => {



    document



      .getElementById("scanner")



      ?.scrollIntoView({



        behavior: "smooth",



        block: "start",



      });



  };







  const scrollToThreatAssessment = () => {



    setTimeout(() => {



      document



        .getElementById("threat-assessment")



        ?.scrollIntoView({



          behavior: "smooth",



          block: "start",



        });



    }, 50);



  };







  const saveToScanHistory = (analysisResult) => {



    const historyItem = {



      id: Date.now(),



      url: analysisResult.url,



      classification: analysisResult.classification,



      risk_score: analysisResult.risk_score,



      phishing_probability:



        analysisResult.phishing_probability,



      legitimate_probability:



        analysisResult.legitimate_probability,



      indicators: analysisResult.indicators || [],



      timestamp: new Date().toISOString(),



    };







    setScanHistory((previousHistory) => {



      const updatedHistory = [



        historyItem,



        ...previousHistory.filter(



          (item) => item.url !== historyItem.url



        ),



      ].slice(0, 10);







      try {



        localStorage.setItem(



          "phishlens_scan_history",



          JSON.stringify(updatedHistory)



        );



      } catch (storageError) {



        console.error(



          "Failed to save scan history:",



          storageError



        );



      }







      return updatedHistory;



    });



  };







  const restoreScan = (scan) => {



    setUrl(scan.url);



    setResult({



      url: scan.url,



      classification: scan.classification,



      risk_score: scan.risk_score,



      phishing_probability:



        scan.phishing_probability,



      legitimate_probability:



        scan.legitimate_probability,



      indicators: scan.indicators || [],



    });



    setError("");



    setPipelineStage(4);







    scrollToThreatAssessment();



  };







  const clearScanHistory = () => {



    setScanHistory([]);







    try {



      localStorage.removeItem(



        "phishlens_scan_history"



      );



    } catch (storageError) {



      console.error(



        "Failed to clear scan history:",



        storageError



      );



    }



  };







  const formatScanTime = (timestamp) => {



    if (!timestamp) {



      return "Unknown time";



    }







    try {



      const date = new Date(timestamp);







      return date.toLocaleString([], {



        day: "2-digit",



        month: "short",



        hour: "2-digit",



        minute: "2-digit",



      });



    } catch {



      return "Unknown time";



    }



  };







  const getHistoryLabel = (classification) => {



    if (classification === "phishing") {



      return "PHISHING";



    }







    if (classification === "suspicious") {



      return "SUSPICIOUS";



    }







    return "SAFE";



  };







  const analyzeUrl = async () => {

    setError("");

    setResult(null);



    const cleanedUrl = url.trim();



    if (!cleanedUrl) {

      setError(

        "Please enter a URL before starting the analysis."

      );

      return;

    }



    setLoading(true);

    setPipelineStage(1);



    try {

      await new Promise((resolve) =>

        setTimeout(resolve, 350)

      );



      setPipelineStage(2);



      const response = await fetch(API_URL, {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

        },

        body: JSON.stringify({

          url: cleanedUrl,

        }),

      });



      const data = await response.json();



      if (!response.ok) {

        const backendMessage =

          data?.detail?.[0]?.msg ||

          data?.detail ||

          "The URL could not be analyzed.";



        throw new Error(backendMessage);

      }



      setPipelineStage(3);



      await new Promise((resolve) =>

        setTimeout(resolve, 250)

      );



      setPipelineStage(4);



      await new Promise((resolve) =>

        setTimeout(resolve, 450)

      );



      setResult(data);

      saveToScanHistory(data);

      scrollToThreatAssessment();

    } catch (requestError) {

      setError(

        requestError?.message ||

          "Unable to connect to the PhishLens analysis engine."

      );

      setPipelineStage(0);

    } finally {

      setLoading(false);

    }

  };



  const handleKeyDown = (event) => {



    if (event.key === "Enter" && !loading) {



      analyzeUrl();



    }



  };







  const resetAnalysis = () => {



    setResult(null);



    setError("");



    setPipelineStage(0);



    setUrl("");







    setTimeout(() => {



      document



        .getElementById("scanner")



        ?.scrollIntoView({



          behavior: "smooth",



          block: "start",



        });



    }, 50);



  };







  const getPipelineState = (index) => {



    if (loading) {



      if (index === pipelineStage) {



        return "active";



      }







      if (index < pipelineStage) {



        return "complete";



      }







      return "";



    }







    if (result) {



      return "complete";



    }







    return "";



  };







  return (



    <div



      className={`app ${



        isLight ? "theme-light" : ""



      }`}



    >



      <div className="ambient ambient-one" />



      <div className="ambient ambient-two" />



      <div className="ambient ambient-three" />







      <header className="navbar">



        <div className="brand">



          <div className="brand-mark">P</div>







          <div className="brand-copy">



            <span className="brand-name">



              PhishLens



            </span>







            <span className="brand-subtitle">



              AI SECURITY INTELLIGENCE



            </span>



          </div>



        </div>







        <nav className="nav-links">



          <button



            className="nav-link active"



            onClick={scrollToScanner}



          >



            Scanner



          </button>







          <button



            className="nav-link"



            onClick={() =>



              document



                .getElementById("intelligence")



                ?.scrollIntoView({



                  behavior: "smooth",



                })



            }



          >



            Intelligence



          </button>







          <button



            className="nav-link"



            onClick={() =>



              document



                .getElementById("about")



                ?.scrollIntoView({



                  behavior: "smooth",



                })



            }



          >



            About



          </button>



        </nav>







        <div className="nav-actions">



          <div className="system-status">



            <span className="status-dot" />



            SYSTEM ONLINE



          </div>







          <button



            className="theme-toggle"



            type="button"



            onClick={() =>



              setTheme(



                isLight ? "dark" : "light"



              )



            }



            aria-label="Toggle color theme"



          >



            {isLight ? "☀" : "☾"}



          </button>



        </div>



      </header>







      <main>



        <section className="hero">



          <div className="hero-copy">



            <div className="eyebrow">



              <span className="eyebrow-dot" />



              AI-POWERED THREAT DETECTION



            </div>







            <h1>



              Detect before



              <span>you click.</span>



            </h1>







            <p className="hero-description">



              PhishLens AI analyzes URL structure,



              machine-learning signals and security



              indicators to uncover suspicious links



              before they become a threat.



            </p>







            <div className="hero-actions">



              <button



                className="primary-button"



                onClick={scrollToScanner}



              >



                Analyze a URL



                <span className="button-arrow">



                  ↓



                </span>



              </button>







              <div className="hero-meta">



                <div>



                  <strong>34+</strong>



                  <span>



                    automated signals



                  </span>



                </div>







                <div>



                  <strong>ML</strong>



                  <span>



                    classification



                  </span>



                </div>



              </div>



            </div>



          </div>







          <div className="hero-visual">



            <span className="core-label">



              THREAT CORE



            </span>







            <div className="orbit orbit-one" />



            <div className="orbit orbit-two" />



            <div className="orbit orbit-three" />







            <span className="signal-node node-one" />



            <span className="signal-node node-two" />



            <span className="signal-node node-three" />



            <span className="signal-node node-four" />







            <div className="floating-card model-card">



              <span>MODEL</span>



              <strong>ROBUST LR</strong>



            </div>







            <div className="floating-card signal-card">



              <span>01</span>



              <strong>URL SIGNAL</strong>



            </div>







            <div className="floating-card score-card">



              <span>THREAT SCORE</span>



              <strong>



                {result ? result.risk_score : "—"}



              </strong>



            </div>







            <div className="floating-card status-card">



              <span>STATUS</span>



              <strong>



                {loading



                  ? "SCANNING"



                  : result



                    ? "ANALYZED"



                    : "READY"}



              </strong>



            </div>







            <div



              className={`shield-core ${



                loading



                  ? "shield-scanning"



                  : result



                    ? `shield-result shield-${resultTone}`



                    : ""



              }`}



            >



              <div className="shield-glow" />







              <div className="shield">



                <div className="shield-inner">



                  <div className="shield-check">



                    {loading



                      ? "◌"



                      : result?.classification ===



                          "phishing"



                        ? "!"



                        : "✓"}



                  </div>







                  <div className="shield-status">



                    {loading



                      ? "ANALYZING"



                      : result



                        ? result.classification.toUpperCase()



                        : "PROTECTED"}



                  </div>







                  <div className="shield-caption">



                    {loading



                      ? "THREAT ANALYSIS ACTIVE"



                      : result



                        ? "ANALYSIS COMPLETE"



                        : "SECURITY ACTIVE"}



                  </div>



                </div>



              </div>







              <div className="core-base">



                PHISHLENS / AI



              </div>



            </div>



          </div>



        </section>







        <section



          className="scanner-section"



          id="scanner"



        >



          <div className="section-heading">



            <div>



              <span className="section-number">



                01



              </span>







              <h2>



                Inspect a suspicious link.



              </h2>



            </div>







            <div className="engine-status">



              <span className="status-dot" />



              {loading



                ? "ANALYSIS ENGINE RUNNING"



                : "ANALYSIS ENGINE READY"}



            </div>



          </div>







          <div



            className={`scanner-panel ${



              loading



                ? "scanner-focus is-scanning"



                : ""



            }`}



          >



            <div className="scanner-topline">



              <div>



                <span className="scanner-index">



                  01



                </span>







                <div>



                  <h3>Target URL</h3>







                  <p>



                    Paste a URL for threat analysis



                  </p>



                </div>



              </div>







              <span className="engine-version">



                PHISHLENS ENGINE / V1.0



              </span>



            </div>







            <div className="scanner-input-row">



              <div className="url-input-wrap">



                <span className="url-icon">



                  ↗



                </span>







                <input



                  type="url"



                  value={url}



                  onChange={(event) =>



                    setUrl(event.target.value)



                  }



                  onKeyDown={handleKeyDown}



                  placeholder="https://example.com/login"



                  aria-label="URL to analyze"



                  disabled={loading}



                />







                {loading && (



                  <span className="input-scanner">



                    ANALYZING...



                  </span>



                )}



              </div>







              <button



                className="analyze-button"



                onClick={analyzeUrl}



                disabled={loading}



              >



                {loading



                  ? "Analyzing..."



                  : "Analyze URL"}







                <span className="button-arrow">



                  ↗



                </span>



              </button>



            </div>







            <div className="scanner-footer">



              <span>



                AI classification · Security



                indicators · Risk scoring



              </span>







              <span>



                HTTPS / HTTP supported



              </span>



            </div>







            {error && (



              <div className="error-panel">



                <span>!</span>



                <p>{error}</p>



              </div>



            )}



          </div>



        </section>







        {/* RECENT SCANS */}



        <section className="recent-scans-section">



          <div className="recent-scans-heading">



            <div>



              <span className="section-kicker">



                ACTIVITY LOG



              </span>







              <h2>Recent scans.</h2>







              <p>



                Your latest URL analyses are stored



                locally in this browser.



              </p>



            </div>







            {scanHistory.length > 0 && (



              <button



                className="clear-history-button"



                type="button"



                onClick={clearScanHistory}



              >



                Clear history



                <span>×</span>



              </button>



            )}



          </div>







          {scanHistory.length > 0 ? (



            <div className="recent-scans-list">



              {scanHistory.map((scan) => (



                <button



                  key={scan.id}



                  type="button"



                  className={`recent-scan-card history-${scan.classification}`}



                  onClick={() => restoreScan(scan)}



                >



                  <div className="recent-scan-status">



                    <span className="recent-scan-dot" />







                    <span>



                      {getHistoryLabel(



                        scan.classification



                      )}



                    </span>



                  </div>







                  <div className="recent-scan-url">



                    <strong title={scan.url}>



                      {scan.url}



                    </strong>







                    <span>



                      {formatScanTime(



                        scan.timestamp



                      )}



                    </span>



                  </div>







                  <div className="recent-scan-score">



                    <span>RISK</span>







                    <strong>



                      {scan.risk_score}



                    </strong>



                  </div>







                  <span className="recent-scan-arrow">



                    ↗



                  </span>



                </button>



              ))}



            </div>



          ) : (



            <div className="recent-scans-empty">



              <div className="recent-empty-icon">



                ◌



              </div>







              <div>



                <strong>



                  No recent scans yet



                </strong>







                <p>



                  Analyze a URL and your latest



                  results will appear here.



                </p>



              </div>



            </div>



          )}



        </section>







        {(loading || result) && (



          <section className="scan-pipeline">



            <div className="pipeline-heading">



              <span>



                PHISHLENS ANALYSIS PIPELINE



              </span>







              <span>



                {loading



                  ? "PROCESSING"



                  : "COMPLETE"}



              </span>



            </div>







            <div className="pipeline-grid">



              {pipelineSteps.map(



                (step, index) => (



                  <div



                    key={step.number}



                    className={`pipeline-step ${getPipelineState(



                      index + 1



                    )}`}



                  >



                    <span>{step.number}</span>







                    <strong>



                      {step.title}



                    </strong>







                    <small>



                      {step.detail}



                    </small>



                  </div>



                )



              )}



            </div>



          </section>



        )}







        {result && (



          <section



            className="result-section"



            id="threat-assessment"



          >



            <div className="section-heading">



              <div>



                <span className="section-number">



                  02



                </span>







                <h2>



                  Threat assessment.



                </h2>



              </div>







              <div className="result-live">



                <span className="status-dot" />



                ANALYSIS COMPLETE



              </div>



            </div>







            <div className="result-grid">



              <article



                className={`risk-card result-${resultTone}`}



              >



                <div className="risk-card-header">



                  <span>



                    THREAT SCORE



                  </span>







                  <span className="risk-classification">



                    {result.classification.toUpperCase()}



                  </span>



                </div>







                <div



                  className={`risk-ring risk-${resultTone}`}



                  style={{



                    "--risk-progress": `${riskProgress}%`,



                  }}



                >



                  <div className="risk-ring-inner">



                    <strong>



                      {result.risk_score}



                    </strong>







                    <span>/ 100</span>



                  </div>



                </div>







                <div className="risk-summary">



                  <strong title={result.url}>



                    {result.url}



                  </strong>







                  <span>



                    PhishLens combines ML probability



                    with interpretable security signals.



                  </span>



                </div>



              </article>







              <article className="probability-card">



                <div className="result-card-heading">



                  <span>



                    MODEL CONFIDENCE



                  </span>







                  <span>



                    ROBUST LR



                  </span>



                </div>







                <div className="probability-row">



                  <div className="probability-label">



                    <span>PHISHING</span>







                    <strong>



                      {phishingProbability}%



                    </strong>



                  </div>







                  <div className="probability-bar">



                    <div



                      className="probability-fill phishing-fill"



                      style={{



                        width: `${phishingProbability}%`,



                      }}



                    />



                  </div>



                </div>







                <div className="probability-row">



                  <div className="probability-label">



                    <span>LEGITIMATE</span>







                    <strong>



                      {legitimateProbability}%



                    </strong>



                  </div>







                  <div className="probability-bar">



                    <div



                      className="probability-fill legitimate-fill"



                      style={{



                        width: `${legitimateProbability}%`,



                      }}



                    />



                  </div>



                </div>







                <div className="model-note">



                  Classification threshold: 0.55



                </div>



              </article>







              <article className="indicator-card">



                <div className="result-card-heading">



                  <span>



                    SECURITY INDICATORS



                  </span>







                  <span>



                    {result.indicators.length} DETECTED



                  </span>



                </div>







                {result.indicators.length > 0 ? (



                  <div className="indicator-list">



                    {result.indicators.map(



                      (indicator, index) => (



                        <div



                          className="indicator-item"



                          key={`${indicator.message}-${index}`}



                        >



                          <span



                            className={`indicator-severity ${indicator.severity}`}



                          />







                          <div>



                            <strong>



                              {indicator.severity.toUpperCase()}



                            </strong>







                            <p>



                              {indicator.message}



                            </p>



                          </div>



                        </div>



                      )



                    )}



                  </div>



                ) : (



                  <div className="clean-result">



                    <div className="clean-icon">



                      ✓



                    </div>







                    <div>



                      <strong>



                        No warning indicators



                      </strong>







                      <p>



                        No additional suspicious



                        patterns were detected by



                        the rule engine.



                      </p>



                    </div>



                  </div>



                )}



              </article>



            </div>







                        <section className="explainability-panel">


              <div className="explainability-heading">


                <div>


                  <span className="section-kicker">EXPLAINABLE ANALYSIS</span>


                  <h3>Why did PhishLens give this score?</h3>


                  <p>


                    These signals come directly from the URL features extracted by the PhishLens analysis engine.


                  </p>


                </div>


                <span className="explainability-count">


                  {(result.signals || []).length} SIGNALS


                </span>


              </div>


              <div className="explainability-grid">


                {(result.signals || []).map((signal, index) => (


                  <article


                    className={`explainability-item severity-${signal.severity}`}


                    key={`${signal.name}-${index}`}


                  >


                    <div className="explainability-item-top">


                      <span className="explainability-dot" />


                      <strong>{signal.name}</strong>


                      <span className="explainability-severity">


                        {signal.severity.toUpperCase()}


                      </span>


                    </div>


                    <div className="explainability-value">{signal.value}</div>


                    <p>{signal.interpretation}</p>


                  </article>


                ))}


              </div>


            </section>


<div



              className={`decision-panel decision-${resultTone}`}



            >



              <div className="decision-icon">



                {decisionContent.icon}



              </div>







              <div className="decision-copy">



                <span>



                  {decisionContent.eyebrow}



                </span>







                <h3>



                  {decisionContent.title}



                </h3>







                <p>



                  {decisionContent.description}



                </p>







                <strong>



                  Recommended action:{" "}



                  {decisionContent.action}



                </strong>



              </div>







              <button



                className="decision-button"



                type="button"



                onClick={resetAnalysis}



              >



                Scan another URL



                <span>↗</span>



              </button>



            </div>







            <div className="signal-profile">



              <div className="signal-profile-heading">



                <div>



                  <span className="section-kicker">



                    URL INTELLIGENCE



                  </span>







                  <h3>



                    Structural signal profile



                  </h3>



                </div>







                <span>



                  MODEL INPUT SIGNALS



                </span>



              </div>







              <div className="signal-profile-grid">



                {signalProfile.map(



                  ([label, value]) => (



                    <div



                      className="signal-profile-item"



                      key={label}



                    >



                      <div className="signal-profile-top">



                        <span>{label}</span>







                        <strong>



                          {value}



                        </strong>



                      </div>







                      <div className="signal-profile-bar">



                        <div



                          className="signal-profile-fill"



                          style={{



                            width: `${value}%`,



                          }}



                        />



                      </div>



                    </div>



                  )



                )}



              </div>



            </div>



          </section>



        )}







        <section



          className="intelligence-section"



          id="intelligence"



        >



          <div className="intelligence-intro">



            <div>



              <span className="section-kicker">



                DEFENSE LAYER



              </span>







              <h2 className="section-heading-title">



                More than a URL checker.



              </h2>



            </div>







            <p>



              PhishLens combines machine learning



              with interpretable security signals to



              produce a clearer threat assessment.



            </p>



          </div>







          <div className="feature-grid">



            {featureCards.map((card) => (



              <article



                key={card.number}



                className={`feature-card ${



                  card.featured ? "featured" : ""



                }`}



              >



                <span className="feature-number">



                  {card.number}



                </span>







                <div className="feature-icon">



                  {card.icon}



                </div>







                <h3>{card.title}</h3>







                <p>{card.description}</p>







                <div className="feature-footer">



                  <span>{card.footer}</span>



                  <span>↗</span>



                </div>



              </article>



            ))}



          </div>



        </section>







        <section



          className="about-section"



          id="about"



        >



          <div className="about-line" />







          <div className="about-content">



            <span className="section-kicker">



              PHISHLENS AI



            </span>







            <h2>



              Security decisions should be <span>understandable.</span>



            </h2>







            <p>



              PhishLens is designed to make phishing



              detection more transparent by combining



              machine-learning classification with



              human-readable security evidence.



            </p>



          </div>







          <div className="about-metrics">



            <div>



              <strong>34+</strong>



              <span>URL FEATURES</span>



            </div>







            <div>



              <strong>0.55</strong>



              <span>DECISION THRESHOLD</span>



            </div>







            <div>



              <strong>AI</strong>



              <span>ASSISTED ANALYSIS</span>



            </div>



          </div>



        </section>



      </main>







      <footer className="footer">



        <div>



          <strong>PhishLens</strong>







          <span>



            AI SECURITY INTELLIGENCE



          </span>



        </div>







        <span>



          Built for safer decisions on the web.



        </span>







        <span>



          © 2026 PHISHLENS AI



        </span>



      </footer>



    </div>



  );



}







export default App;