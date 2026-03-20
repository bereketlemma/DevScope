interface AnomalyAlertProps {
  anomaly: {
    id: number
    metric_name: string
    detected_value: number
    z_score: number
  }
}

function AnomalyAlert({ anomaly }: AnomalyAlertProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-3">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <span className="inline-flex items-center justify-center h-8 w-8 rounded-md bg-red-500 text-white">
            !
          </span>
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800">
            {anomaly.metric_name}
          </h3>
          <p className="text-sm text-red-700 mt-1">
            Anomaly detected: {anomaly.detected_value.toFixed(2)} (Z-score: {anomaly.z_score.toFixed(2)})
          </p>
        </div>
      </div>
    </div>
  )
}

export default AnomalyAlert
