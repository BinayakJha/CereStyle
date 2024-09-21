import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Card, ListGroup, Spinner, Alert } from 'react-bootstrap';
import './App.css'; // Assuming the above CSS is in App.css

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [message, setMessage] = useState('');
  const [products, setProducts] = useState([]);
  const [skinTone, setSkinTone] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle file selection and preview
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setImagePreview(URL.createObjectURL(file));
  };

  // Handle file upload and receive product suggestions
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true); // Show loading spinner

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.message);
      setProducts(response.data.products);
      setSkinTone(response.data.skinTone); // Assuming the backend returns skin tone
      setLoading(false); // Hide loading spinner
    } catch (error) {
      console.error("There was an error uploading the file!", error);
      setMessage("Error uploading file. Please try again.");
      setLoading(false); // Hide loading spinner even on error
    }
  };

  return (
    <div style={{ backgroundColor: '#fff5f5', minHeight: '100vh', padding: '2rem 0' }}> {/* Full white background */}
      <Container className="container mt-5">
        <Row className="justify-content-center">
          {/* Main Form and Image Preview */}
          <Col md={6}>
            <Card className="card shadow-sm p-4 mb-4">
              <h2 className="text-center mb-4">Upload Your Photo</h2>
              <Form onSubmit={handleUpload}>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label>Select a photo to upload</Form.Label>
                  <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100 mb-4">
                  {loading ? (
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                  ) : (
                    'Upload'
                  )}
                </Button>
              </Form>

              {imagePreview && (
                <Card className="mb-3">
                  <Card.Img variant="top" src={imagePreview} alt="Uploaded Preview" className="card-img" />
                </Card>
              )}

              {message && (
                <Alert variant="info" className="mt-3">
                  {message}
                </Alert>
              )}
            </Card>
          </Col>

          {/* Side Column for Skin Tone */}
          <Col md={3}>
            <Card className="card shadow-sm p-4 mb-4">
              <h4 className="mb-3 text-center">Detected Skin Tone</h4>
              {loading ? (
                <div className="d-flex justify-content-center">
                  <Spinner animation="border" />
                </div>
              ) : (
                skinTone && (
                  <div className="skin-tone-display p-3" style={{ backgroundColor: skinTone }}></div>
                )
              )}
            </Card>
          </Col>

          {/* Side Column for Product Recommendations */}
          <Col md={3}>
            <Card className="card shadow-sm p-4 mb-4">
              <h4 className="mb-3 text-center">Outfit Suggestions</h4>
              {loading ? (
                <div className="d-flex justify-content-center">
                  <Spinner animation="border" />
                </div>
              ) : (
                products.length > 0 && (
                  <ListGroup variant="flush">
                    {products.map((product, index) => (
                      <ListGroup.Item key={index}>{product}</ListGroup.Item>
                    ))}
                  </ListGroup>
                )
              )}
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
