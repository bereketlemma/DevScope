import { useParams } from 'react-router-dom'

function RepositoryDetail() {
  const { id } = useParams()

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Repository Details</h1>
      <p className="text-gray-600">Repository ID: {id}</p>
    </div>
  )
}

export default RepositoryDetail
