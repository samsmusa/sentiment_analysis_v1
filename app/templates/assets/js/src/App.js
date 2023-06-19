import React, { useEffect } from "react";
import Form from "./pages/home/component/Form";
import ReactSpeedometer from "react-d3-speedometer";
import { useSentiment } from "./common/sentimentContext";

function App() {
  const { sentiment } = useSentiment();
  useEffect(() => {
    console.log(sentiment);
  }, [sentiment]);
  return (
    <div
      style={{ backgroundColor: "black" }}
      className="h-screen bg-black text-center"
    >
      <div className="text-white py-10 mb-10">
        <p className="">Sentiment Analysis</p>
        <span>Sentiment analysis based on text input</span>
      </div>
      <div className="container mx-auto flex justify-center align-middle mt-20">
        <div className="grid md:grid-cols-3 w-full">
          <div className="col-span-1"></div>
          <div className="col-span-1 flex flex-col justify-items-center align-middle">
            <ReactSpeedometer
              height={200}
              needleHeightRatio={0.7}
              value={sentiment.value * 2 + 3}
              customSegmentStops={[0, 2, 4, 6]}
              segmentColors={["#9399ff", "#14ffec", "#00bbf0"]}
              maxValue={6}
              currentValueText="Sentiment"
              customSegmentLabels={[
                {
                  text: "Negative",
                  position: "OUTSIDE",
                  color: "#d8dee9",
                },
                {
                  text: "Neutral",
                  position: "OUTSIDE",
                  color: "#d8dee9",
                },
                {
                  text: "Positive",
                  position: "OUTSIDE",
                  color: "#d8dee9",
                },
              ]}
              ringWidth={47}
              needleTransitionDuration={3333}
              needleTransition="easeElastic"
              needleColor={"#a7ff83"}
              textColor={"#d8dee9"}
            />
            <Form />
          </div>
          <div className="col-span-1"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
