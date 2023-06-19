import { createContext, useContext } from "react";
import React from "react";

const SentimentContex = createContext({ sentiment: {} });

export default function SentimentProvider(props) {
  const [sentiment, setSentiment] = React.useState({
    sentiment: "neutral",
    value: 0,
  });
  return (
    <SentimentContex.Provider value={{ sentiment, setSentiment }}>
      {props.children}
    </SentimentContex.Provider>
  );
}

export function useSentiment() {
  const sentiment = useContext(SentimentContex);
  return sentiment;
}
