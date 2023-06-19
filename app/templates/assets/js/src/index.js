import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import SentimentProvider from "./common/sentimentContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <SentimentProvider>
      <App />
    </SentimentProvider>
  </React.StrictMode>
);
