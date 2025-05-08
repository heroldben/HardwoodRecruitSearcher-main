import React, { useState } from "react";

const height_inc_dec = 0.1131;
const weight_inc_dec = 0.3959;
const wingspan_inc_dec = 0.1131;
const vertical_inc_dec = 0.2451;

function roundHeight(res) {
  const resString = res.toString();
  const dec_values = resString.split(".")[1] || "0";
  const tenths = parseInt(dec_values[0], 10);

  if (tenths < 4) return Math.floor(res);
  if (tenths >= 4 && tenths < 9) {
    return tenths < 8 ? Math.round(res * 2) / 2 : Math.floor(res * 2) / 2;
  }
  return Math.ceil(res);
}

function height_pred(freshHeight) {
  const res = freshHeight + freshHeight * height_inc_dec;
  return roundHeight(res);
}

function weight_pred(freshWeight) {
  const res = freshWeight + freshWeight * weight_inc_dec;
  return Math.round(res / 5) * 5;
}

function playerGrowthPercent(currentWeight, freshWeight) {
  return (currentWeight - freshWeight) / freshWeight / weight_inc_dec;
}

function predicted(current, growthRate, percent) {
  if (percent >= 1) return current;
  const fresh = current / (1 + percent * growthRate);
  return fresh * (1 + growthRate);
}

function wingspan_pred(currentWingspan, P) {
  const pred =
    Math.round(predicted(currentWingspan, wingspan_inc_dec, P) * 4) / 4;
  if (pred >= 96) return 95.5;
  return pred < currentWingspan ? currentWingspan : pred;
}

function vertical_pred(currentVertical, P) {
  const pred =
    Math.round(predicted(currentVertical, vertical_inc_dec, P) * 2) / 2;
  return pred < currentVertical ? currentVertical : pred;
}

// converts to feet and inches
function inches_to_feet_inches(inches) {
  const feet = Math.floor(inches / 12);
  const new_inches = inches - feet * 12;
  return `${feet}'${new_inches}`;
}

function measurable_diff(
  predicted_height,
  predicted_weight,
  predicted_wingspan,
  predicted_vertical
) {
  return (
    predicted_height -
    81.5 +
    (predicted_weight - 225) / 10 +
    (predicted_wingspan - 84) +
    (predicted_vertical - 30)
  );
}

export default function PlayerGrowthPredictor() {
  const [freshHeight, setFreshHeight] = useState(77);
  const [freshWeight, setFreshWeight] = useState(180);
  const [currentWeight, setCurrentWeight] = useState(200);
  const [currentWingspan, setCurrentWingspan] = useState(82);
  const [currentVertical, setCurrentVertical] = useState(30);

  const P = playerGrowthPercent(currentWeight, freshWeight);

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow rounded-xl space-y-4">
      <h1 className="text-xl font-bold">Player Growth Predictor</h1>

      <div className="space-y-2">
        <label>
          Freshman Height (in): {freshHeight} |{" "}
          {inches_to_feet_inches(freshHeight)}
        </label>
        <input
          type="range"
          min="60"
          max="84"
          step="0.5"
          value={freshHeight}
          onChange={(e) => setFreshHeight(Number(e.target.value))}
          className="w-full"
        />

        <label>Freshman Weight (lbs): {freshWeight}</label>
        <input
          type="range"
          min="120"
          max="250"
          value={freshWeight}
          onChange={(e) => setFreshWeight(Number(e.target.value))}
          className="w-full"
        />

        <label>Current Weight (lbs): {currentWeight}</label>
        <input
          type="range"
          min="120"
          max="300"
          value={currentWeight}
          onChange={(e) => setCurrentWeight(Number(e.target.value))}
          className="w-full"
        />

        <label>
          Current Wingspan (in): {currentWingspan} |{" "}
          {inches_to_feet_inches(currentWingspan)}
        </label>
        <input
          type="range"
          min="70"
          max="96"
          step="0.25"
          value={currentWingspan}
          onChange={(e) => setCurrentWingspan(Number(e.target.value))}
          className="w-full"
        />

        <label>Current Vertical (in): {currentVertical}</label>
        <input
          type="range"
          min="20"
          max="50"
          step="0.5"
          value={currentVertical}
          onChange={(e) => setCurrentVertical(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="mt-4 p-4 bg-gray-100 rounded-xl">
        <h2 className="text-lg font-semibold mb-2">Predicted Results</h2>
        <p>
          Predicted Height:{" "}
          <strong>
            {height_pred(freshHeight)} in |{" "}
            {inches_to_feet_inches(height_pred(freshHeight))}
          </strong>
        </p>
        <p>
          Predicted Weight: <strong>{weight_pred(freshWeight)} lbs</strong>
        </p>
        <p>
          Projected Wingspan:{" "}
          <strong>
            {wingspan_pred(currentWingspan, P)} in |{" "}
            {inches_to_feet_inches(wingspan_pred(currentWingspan, P))}
          </strong>
        </p>
        <p>
          Projected Vertical:{" "}
          <strong>{vertical_pred(currentVertical, P)} in</strong>
        </p>
        <p>
          Projected Big Ratio:{" "}
          <strong>
            {measurable_diff(
              height_pred(freshHeight),
              weight_pred(freshWeight),
              wingspan_pred(currentWingspan, P),
              vertical_pred(currentVertical, P)
            )}
          </strong>
        </p>
      </div>
    </div>
  );
}
